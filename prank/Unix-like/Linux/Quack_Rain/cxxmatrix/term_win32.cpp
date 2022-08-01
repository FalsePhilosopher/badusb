#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <sstream>
#include <string>
#include <algorithm>
#include <windows.h>
#include "cxxmatrix.hpp"

namespace cxxmatrix {

  static int default_cols = 80;
  static int default_rows = 25;

  static void print_error_message(const char* title) {
    LPSTR lpMsgBuf;
    FormatMessageA(
      FORMAT_MESSAGE_ALLOCATE_BUFFER |
      FORMAT_MESSAGE_FROM_SYSTEM |
      FORMAT_MESSAGE_IGNORE_INSERTS,
      NULL, GetLastError(),
      //MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
      MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US),
      (LPSTR) &lpMsgBuf, 0, NULL);
    std::fprintf(stderr, "cxxmatrix: %s: Win32Error %lu\n%s\n", title, GetLastError(), lpMsgBuf);
    LocalFree(lpMsgBuf);
  }


  static bool conpty_enabled = false;
  static HANDLE conpty_hStdOutput = INVALID_HANDLE_VALUE;
  static bool conpty_internal = false;
  static DWORD conpty_input_mode_save = 0;
  static DWORD conpty_output_mode_save = 0;
  static UINT conpty_input_cp_save = 0;
  static UINT conpty_output_cp_save = 0;

  static bool conpty_winsize(int& cols, int& rows) {
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut == INVALID_HANDLE_VALUE) {
      print_error_message("GetStdHandle");
      return false;
    }

    CONSOLE_SCREEN_BUFFER_INFO csbi;
    if (GetConsoleScreenBufferInfo(hOut, &csbi) == 0) {
      print_error_message("GetConsoleScreenBufferInfo");
      return false;
    }

    cols = csbi.srWindow.Right - csbi.srWindow.Left + 1;
    rows = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
    return true;
  }

  static bool conpty_init(HANDLE hIn) {
    conpty_hStdOutput = hIn;
    conpty_enabled = conpty_winsize(default_cols, default_rows);
    return conpty_enabled;
  }

  static void conpty_enter() {
    if (conpty_internal) return;
    conpty_internal = true;

    if (HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE); hIn == INVALID_HANDLE_VALUE) {
      print_error_message("GetStdHandle (stdin)");
    } else {
      if (GetConsoleMode(hIn, &conpty_input_mode_save) == 0) {
        print_error_message("GetConsoleMode (stdin)");
      } else {
        if (SetConsoleMode(hIn, conpty_input_mode_save | ENABLE_VIRTUAL_TERMINAL_INPUT) == 0)
          print_error_message("SetConsoleMode (stdin)");
      }
    }

    if (HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE); hOut == INVALID_HANDLE_VALUE) {
      print_error_message("GetStdHandle (stdout)");
    } else {
      if (GetConsoleMode(hOut, &conpty_output_mode_save) == 0) {
        print_error_message("GetConsoleMode (stdout)");
      } else {
        if (SetConsoleMode(hOut, conpty_output_mode_save | ENABLE_VIRTUAL_TERMINAL_PROCESSING) == 0)
          print_error_message("SetConsoleMode (stdout)");
      }
    }

    conpty_input_cp_save = GetConsoleCP();
    if (conpty_input_cp_save == 0)
      print_error_message("GetConsoleCP");
    else if (SetConsoleCP(CP_UTF8) == 0)
      print_error_message("SetConsoleCP");

    conpty_output_cp_save = GetConsoleOutputCP();
    if (conpty_output_cp_save == 0)
      print_error_message("GetConsoleOutputCP");
    else if (SetConsoleOutputCP(CP_UTF8) == 0)
      print_error_message("SetConsoleOutputCP");
  }

  static void conpty_leave() {
    if (!conpty_internal) return;
    conpty_internal = false;

    if (HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE); hIn == INVALID_HANDLE_VALUE) {
      print_error_message("GetStdHandle (stdin)");
    } else if (SetConsoleMode(hIn, conpty_input_mode_save) == 0) {
      print_error_message("SetConsoleMode (stdin)");
    }

    if (HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE); hOut == INVALID_HANDLE_VALUE) {
      print_error_message("GetStdHandle (stdout)");
    } else if (SetConsoleMode(hOut, conpty_output_mode_save) == 0) {
      print_error_message("SetConsoleMode (stdout)");
    }

    if (conpty_input_cp_save != 0 && SetConsoleCP(conpty_input_cp_save) == 0)
      print_error_message("SetConsoleCP (restore)");
    if (conpty_output_cp_save != 0 && SetConsoleOutputCP(conpty_output_cp_save) == 0)
      print_error_message("SetConsoleOutputCP (restore)");
  }

  static std::ptrdiff_t conpty_read(byte* buffer, std::size_t size) {
    DWORD dwNumberOfEvents;
    if (GetNumberOfConsoleInputEvents(conpty_hStdOutput, &dwNumberOfEvents) == 0) {
      print_error_message("GetNumberOfConsoleInputEvents (broken console)");
      return 0;
    }

    std::size_t read_size = 0;

    INPUT_RECORD input_buffer;
    while (read_size < size && dwNumberOfEvents--) {
      DWORD dwNumberOfEventsRead;
      if (ReadConsoleInput(conpty_hStdOutput, &input_buffer, 1, &dwNumberOfEventsRead) == 0) {
        print_error_message("GetNumberOfConsoleInputEvents (broken console)");
        return read_size;
      }

      if (dwNumberOfEventsRead) {
        switch (input_buffer.EventType) {
        case KEY_EVENT:
          {
            auto const& event = input_buffer.Event.KeyEvent;
            if (event.bKeyDown && event.uChar.UnicodeChar < 0x100)
              buffer[read_size++] = (std::uint8_t) event.uChar.UnicodeChar & 0xFF;
          }
          break;
        case WINDOW_BUFFER_SIZE_EVENT:
          {
            auto const& event = input_buffer.Event.WindowBufferSizeEvent;
            if (event.dwSize.X != default_cols || event.dwSize.Y != default_rows)
              trapwinch(28);
          }
          break;
        }
      }
    }

    return (std::ptrdiff_t) read_size;
  }


  static constexpr std::uint32_t stty_checkwinsize_interval = 20;
  static bool stty_enabled = false;
  static HANDLE stty_hStdInput = INVALID_HANDLE_VALUE;
  static std::uint32_t stty_refresh_count = 0;

  static bool stty_update_winsize(int& cols, int& rows) {
    // We want to do something like str=$(stty size 2> NUL) using Win API

    char command[] = "stty.exe size";

    SECURITY_ATTRIBUTES securityAttributes = {};
    securityAttributes.nLength = sizeof securityAttributes;
    securityAttributes.bInheritHandle = TRUE;
    securityAttributes.lpSecurityDescriptor = NULL;

    HANDLE hNulFile = CreateFileA("nul", GENERIC_WRITE, FILE_SHARE_WRITE, &securityAttributes, OPEN_EXISTING, 0, NULL);
    if (hNulFile == INVALID_HANDLE_VALUE) {
      print_error_message("CreateFileA");
      return false;
    }

    HANDLE hPipeRead, hPipeWrite;
    if (CreatePipe(&hPipeRead, &hPipeWrite, &securityAttributes, 0) == 0) {
      print_error_message("CreatePipe");
      CloseHandle(hNulFile);
      return false;
    }

    STARTUPINFOA startupInfo = {};
    {
      startupInfo.cb = sizeof startupInfo;

      startupInfo.dwFlags |= STARTF_USESTDHANDLES;
      startupInfo.hStdInput = stty_hStdInput;
      startupInfo.hStdOutput = hPipeWrite;
      startupInfo.hStdError = hNulFile;

      startupInfo.dwFlags |= STARTF_USESHOWWINDOW;
      startupInfo.wShowWindow = SW_HIDE;
    }

    PROCESS_INFORMATION proc = {};
    if (CreateProcessA(NULL, command, NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &startupInfo, &proc) == 0) {
      print_error_message("CreateProcessA");
      CloseHandle(hPipeRead);
      CloseHandle(hPipeWrite);
      CloseHandle(hNulFile);
      return false;
    }

    std::string output;
    bool alive;
    do {
      alive = WaitForSingleObject(proc.hProcess, 50) != WAIT_OBJECT_0;

      char buff[1024];
      DWORD available_size = 0;
      while (PeekNamedPipe(hPipeRead, NULL, 0, NULL, &available_size, NULL) && available_size > 0) {
        do {
          DWORD read_size = std::min((DWORD) sizeof(buff), available_size);
          if (ReadFile(hPipeRead, &buff[0], read_size, &read_size, NULL) == 0) {
            print_error_message("ReadFile (broken pipe)");
            goto end_read;
          }

          for (DWORD i = 0; i < read_size; i++) {
            if (buff[i] == '\r') {
              buff[i] = '\n';
              if (i + 1 < read_size && buff[i + 1] == '\n') i++;
            }
            output += buff[i];
          }
          available_size -= read_size;
        } while (available_size > 0);
      }
    } while (alive);

  end_read:
    CloseHandle(proc.hProcess);
    CloseHandle(proc.hThread);
    CloseHandle(hPipeRead);
    CloseHandle(hPipeWrite);
    CloseHandle(hNulFile);

    std::istringstream sstr(output);
    int int_cols = -1, int_rows = -1;
    if (sstr >> int_rows >> int_cols && int_cols > 0 && int_rows > 0) {
      cols = int_cols;
      rows = int_rows;
      return true;
    } else
      return false;
  }

  static bool stty_init(HANDLE hIn) {
    stty_hStdInput = hIn;
    stty_enabled = stty_update_winsize(default_cols, default_rows);
    return stty_enabled;
  }
  static void stty_enter() { std::system("stty.exe raw isig"); }
  static void stty_leave() { std::system("stty.exe sane"); }

  static std::ptrdiff_t stty_read(byte* buffer, std::size_t size) {
    DWORD read_size = 0;
    if (PeekNamedPipe(stty_hStdInput, NULL, 0, NULL, &read_size, NULL) && read_size > 0) {
      if (read_size > size) read_size = size;
      if (ReadFile(stty_hStdInput, buffer, read_size, &read_size, NULL) == 0) {
        print_error_message("ReadFile (broken pipe)");
        return 0;
      }
    }

    if (++stty_refresh_count % stty_checkwinsize_interval == 0) {
      int new_cols = -1, new_rows = -1;
      if (stty_update_winsize(new_cols, new_rows) && (new_cols != default_cols || new_rows != default_rows)) {
        default_cols = new_cols;
        default_rows = new_rows;
        trapwinch(28);
      }
    }
    return (std::ptrdiff_t) read_size;
  }

  void term_init() {
    if (HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE); hIn == INVALID_HANDLE_VALUE) {
      print_error_message("GetStdHandle (stdin)");
    } else {
      switch (GetFileType(hIn)) {
      case FILE_TYPE_CHAR: // Console/ConPTY
        if (conpty_init(hIn)) return;
        break;
      case FILE_TYPE_PIPE: // Cygwin/MSYS2 PTY?
        if (stty_init(hIn)) return;
        break;
      }
    }

    term_winsize_from_env(default_cols, default_rows);
  }

  bool term_get_size(int& cols, int& rows) {
    if (conpty_enabled && conpty_winsize(cols, rows)) return true;
    cols = default_cols;
    rows = default_rows;
    return true;
  }

  void term_enter() {
    if (conpty_enabled) conpty_enter();
    if (stty_enabled) stty_enter();
  }
  void term_leave() {
    if (conpty_enabled) conpty_leave();
    if (stty_enabled) stty_leave();
  }

  std::ptrdiff_t term_read(byte* buffer, std::size_t size) {
    if (conpty_enabled)
      return conpty_read(buffer, size);
    if (stty_enabled)
      return stty_read(buffer, size);
    return 0;
  }
}
