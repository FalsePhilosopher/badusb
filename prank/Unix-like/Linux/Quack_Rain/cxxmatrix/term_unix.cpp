#include <cstddef>
#include <csignal>
#include <unistd.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <poll.h>
#include "cxxmatrix.hpp"

namespace cxxmatrix {
  void term_init() {
    std::signal(SIGWINCH, trapwinch);
    std::signal(SIGTSTP, traptstp);
    std::signal(SIGCONT, trapcont);
  }

  bool term_get_size(int& cols, int& rows) {
    struct winsize ws;
    if (ioctl(STDIN_FILENO, TIOCGWINSZ, (char*) &ws) == 0) {
      cols = ws.ws_col;
      rows = ws.ws_row;
      return true;
    }

    return term_winsize_from_env(cols, rows);
  }

  static struct termios term_termios_save;

  void term_enter() {
    tcgetattr(STDIN_FILENO, &term_termios_save);
    struct termios termios = term_termios_save;
    termios.c_lflag &= ~(ECHO | ICANON | IEXTEN); // シグナルは使うので ISIG は消さない
    termios.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
    termios.c_cflag &= ~(CSIZE | PARENB);
    termios.c_cflag |= CS8;
    termios.c_oflag &= ~(OPOST);
    termios.c_cc[VMIN]  = 1;
    termios.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &termios);
  }

  void term_leave() {
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &term_termios_save);
  }

  std::ptrdiff_t term_read(byte* buffer, std::size_t size) {
    struct pollfd pollfd;
    pollfd.fd = STDIN_FILENO;
    pollfd.events = POLLIN | POLLERR;
    poll(&pollfd, 1, 0);
    if (pollfd.revents & POLLIN)
      return (ssize_t) read(STDIN_FILENO, buffer, (ssize_t) size);
    return 0;
  }
}
