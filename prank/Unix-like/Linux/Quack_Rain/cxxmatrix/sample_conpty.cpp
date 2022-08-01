#include <cstdio>
#include <cstdlib>
#include <windows.h>
#include <conio.h>

void term_init() {
  HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
  DWORD dwMode;
  GetConsoleMode(hOut, &dwMode);
  dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
  SetConsoleMode(hOut, dwMode);

  HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE);
  GetConsoleMode(hIn, &dwMode);
  dwMode |= ENABLE_VIRTUAL_TERMINAL_INPUT;
  SetConsoleMode(hIn, dwMode);

  SetConsoleCP(CP_UTF8);
  SetConsoleOutputCP(CP_UTF8);
}

bool check_winsize() {
  HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
  if (hOut == INVALID_HANDLE_VALUE) {
    std::fprintf(stderr, "GetStdHandle: InvalidHandle\n");
    return false;
  }

  CONSOLE_SCREEN_BUFFER_INFO csbi;
  if (GetConsoleScreenBufferInfo(hOut, &csbi) == 0) {
    LPSTR lpMsgBuf;
    FormatMessageA(
      FORMAT_MESSAGE_ALLOCATE_BUFFER |
      FORMAT_MESSAGE_FROM_SYSTEM |
      FORMAT_MESSAGE_IGNORE_INSERTS,
      NULL, GetLastError(),
      //MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
      MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US),
      (LPSTR) &lpMsgBuf, 0, NULL);
    std::fprintf(stderr, "GetConsoleScreenBufferInfo: Error %lu\n%s\n", GetLastError(), lpMsgBuf);
    std::fflush(stderr);
    LocalFree(lpMsgBuf);
    return false;
  }


  int rows, cols;
  cols = csbi.srWindow.Right - csbi.srWindow.Left + 1;
  rows = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
  std::printf("cols=%d rows=%d\n", cols, rows);
  return true;
}

void readloop_conio() {
  for (;;) {
    while (_kbhit()) {
      int c = _getch();
      std::printf("input %d (%c)\n", c, c);
    }
    Sleep(50);
  }
}

void readloop_conapi() {
  HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE);

  for (;;) {
    DWORD dwNumberOfEvents;
    if (GetNumberOfConsoleInputEvents(hIn, &dwNumberOfEvents) == 0) {
      std::fprintf(stderr, "Error: GetNumberOfConsoleInputEvents\n");
      return;
    }

    std::ptrdiff_t read_size = 0;

    INPUT_RECORD buffer;
    while (dwNumberOfEvents--) {
      DWORD dwNumberOfEventsRead;
      if (ReadConsoleInput(hIn, &buffer, 1, &dwNumberOfEventsRead) == 0) {
        std::fprintf(stderr, "Error: GetNumberOfConsoleInputEvents\n");
        return;
      }

      if (dwNumberOfEventsRead) {
        switch (buffer.EventType) {
        case KEY_EVENT:
          {
            auto const& event = buffer.Event.KeyEvent;
            if (event.bKeyDown) {
              CHAR a = event.uChar.AsciiChar;
              std::printf("key down%d rep%d vk%x sc%x U+%04X (%s%c\x1b[m) mod%x\n",
                event.bKeyDown, event.wRepeatCount,
                event.wVirtualKeyCode, event.wVirtualScanCode,
                event.uChar.UnicodeChar,
                a < 0x20 || a == 0x7F ? "\x1b[94m^" : "",
                a < 0x20 ? a + 0x40 : a == 0x7F ? '?' : a,
                event.dwControlKeyState);
            }
          }
          break;
        case WINDOW_BUFFER_SIZE_EVENT:
          //trapwinch();
          std::printf("winch\n");
          break;
        }
      }
    }
  }
}

int main() {
  term_init();
  check_winsize();
  //readloop_conio();
  readloop_conapi();
  return 0;
}
