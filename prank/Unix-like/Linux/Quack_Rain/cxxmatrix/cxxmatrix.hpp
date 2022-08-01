#ifndef cxxmatrix_hpp
#define cxxmatrix_hpp
#include <cstdint>
#include <random>
#include <limits>
#include <string>

namespace cxxmatrix {
  typedef uint8_t byte;

  bool term_winsize_from_env(int& cols, int& rows);
  void trapwinch(int sig);
  void traptstp(int sig);
  void trapcont(int sig);
}

namespace cxxmatrix::util {

inline std::mt19937& rand_engine() {
  static std::random_device seed_gen;
  static std::mt19937 engine(seed_gen());
  return engine;
}
inline std::uint32_t rand() {
  static std::uniform_int_distribution<std::uint32_t> dist(0, std::numeric_limits<std::uint32_t>::max());
  return dist(rand_engine());
}
inline double randf() {
  static std::uniform_real_distribution<double> dist(0, 1.0);
  return dist(rand_engine());
}
inline char32_t rand_char() {
  std::uint32_t r = util::rand() % 80;
  if (r < 10)
    return U'0' + r;
  else
    r -= 10;

  if (r < 46)
    return U'ｰ' + r;
  else
    r -= 46;

  return U"<>*+.:=_|"[r % 9];
}
inline int mod(int value, int modulo) {
  value %= modulo;
  if (value < 0) value += modulo;
  return value;
}

inline constexpr double interpolate(double value, double a, double b) {
  return a + (b - a) * value;
}

inline std::vector<std::string_view> split(const char* text, char c) {
  std::vector<std::string_view> vec;
  char const* p = text;
  do {
    char const* s = p;
    while (*p && *p != c) p++;
    vec.emplace_back(s, p - s);
  } while (*p++ == c);
  return vec;
}

}

#endif
