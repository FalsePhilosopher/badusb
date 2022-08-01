#ifndef cxxmatrix_mandel_hpp
#define cxxmatrix_mandel_hpp
#include <cstddef>
#include <cmath>
#include <vector>
#include <algorithm>
#include <complex>
#include <numeric>
#include "cxxmatrix.hpp"

namespace cxxmatrix {

  class mandelbrot_t {
    int cols = 0, rows = 0;
    std::vector<double> data;
    double scale;
    double theta;

    bool prev_avail = false;
    std::vector<double> data_new;
  public:
    void resize(int cols, int rows) {
      if (cols == this->cols && rows == this->rows) return;
      this->cols = cols;
      this->rows = rows;
      this->data.resize(cols * rows);
      this->data_new.resize(cols * rows);
      this->prev_avail = false;
      std::fill(data.begin(), data.end(), -1.0);
    }

    double& get(int x, int y) {
      return data[y * cols + x];
    }
    double const& get(int x, int y) const {
      return const_cast<mandelbrot_t*>(this)->data[y * cols + x];
    }

  private:
    static constexpr int max_iterate = 5000;

    static int mandel(double u, double v) {
      std::complex<double> const c(u, v);
      std::complex<double> z = c;
      int count = 0;
      while (count < max_iterate) {
        if (std::abs(z) > 2.0) break;
        z = z * z + c;
        count++;
      }
      return std::max(0, count - 5);
    }

    double get_nearest(double x, double y) const {
      x = std::round(x);
      y = std::round(y);
      if (x < 0 || cols <= x) return -1.0;
      if (y < 0 || rows <= y) return -1.0;
      return data[y * cols + x];
    }
    double get_average(double x, double y, int R) const {
      int x0 = std::round(x);
      int y0 = std::round(y);
      double sum = 0.0;
      int count = 0;
      int const a0 = std::max(x0 - R, 0);
      int const aN = std::min(x0 + R, cols - 1);
      int const b0 = std::max(y0 - R, 0);
      int const bN = std::min(y0 + R, rows - 1);
      for (int a = a0; a <= aN; a++) {
        for (int b = b0; b <= bN; b++) {
          double const v =data[b * cols + a];
          sum += v;
          count++;
        }
      }
      if (count == 0) return -1.0;
      return sum / count;
    }

    void resample_prev(double theta, double scale) {
      if (!prev_avail) return;
      double const dtheta = theta - this->theta;
      double const dscale = scale / this->scale;
      int const ox = cols / 2, oy = rows / 2;
      double const u_x = +dscale * std::cos(dtheta) * 0.5 * 2.0;
      double const u_y = -dscale * std::sin(dtheta)       * 2.0;
      double const v_x = +dscale * std::sin(dtheta) * 0.5;
      double const v_y = +dscale * std::cos(dtheta);
      int const Na = 5, Nb = 5;
      for (int y = 0; y < rows; y++) {
        for (int x = 0; x < cols; x++) {
          double const u = ox + (u_x * (x - ox) + u_y * (oy - y));
          double const v = oy - (v_x * (x - ox) + v_y * (oy - y));

          int count = 0;
          double sum = 0.0;
          for (int a = 0; a < Na; a++) {
            for (int b = 0; b < Nb; b++) {
              double const dx = (a + 0.5) / Na - 0.5;
              double const dy = (b + 0.5) / Nb - 0.5;
              double const u1 = u + u_x * dx + u_y * dy;
              double const v1 = v + v_x * dx + v_y * dy;
              double const value = get_nearest(u1, v1);
              if (value >= 0.0) sum += value, count++;
            }
          }
          data_new[y * cols + x] = count ? sum / count : -1.0;
        }
      }
      data.swap(data_new);
    }

    bool is_close(double a, double b) const {
      return std::abs(a - b) / std::abs(a + b) < range * 0.01;
    }
    bool resample_safe(int x, int y) const {
      if (!prev_avail) return false;
      if (x <= 0 || cols - 1 <= x) return false;
      if (y <= 0 || rows - 1 <= y) return false;
      double const value = get(x, y);
      if (value == min_power || value < 0.0) return false;
      if (!is_close(value, get(x + 1, y))) return false;
      if (!is_close(value, get(x - 1, y))) return false;
      if (!is_close(value, get(x, y + 1))) return false;
      if (!is_close(value, get(x, y - 1))) return false;
      if (!is_close(value, get(x + 1, y + 1))) return false;
      if (!is_close(value, get(x + 1, y - 1))) return false;
      if (!is_close(value, get(x - 1, y + 1))) return false;
      if (!is_close(value, get(x - 1, y - 1))) return false;
      return true;
    }

    std::vector<int> positions;

    static constexpr double u0 = -0.743643887037158704752191506114774;
    static constexpr double v0 = +0.131825904205311970493132056385139;
    double u_x;
    double u_y;
    double v_x;
    double v_y;
    double calculate_power_at(int x, int y, int* iterate_count) const {
      int const ox = cols / 2, oy = rows / 2;
      double const u = u0 + (u_x * (x - ox) + u_y * (oy - y));
      double const v = v0 + (v_x * (x - ox) + v_y * (oy - y));

      int sum = 0;
      int const Na = 1, Nb = 1;
      for (int a = 0; a < Na; a++) {
        for (int b = 0; b < Nb; b++) {
          double const dx = (a + 0.5) / Na;
          double const dy = (b + 0.5) / Nb;
          double const u1 = u + u_x * dx + u_y * dy;
          double const v1 = v + v_x * dx + v_y * dy;
          sum += mandel(u1, v1);
        }
      }

      if (iterate_count) *iterate_count += sum;
      return (1.0 / max_iterate / Na / Nb) * sum;
    }
  public:
    void update_frame(double theta, double scale) {
      this->resample_prev(theta, scale);

      this->theta = theta;
      this->scale = scale;
      this->u_x = +scale * std::cos(theta) * 0.5;
      this->u_y = -scale * std::sin(theta);
      this->v_x = +scale * std::sin(theta) * 0.5;
      this->v_y = +scale * std::cos(theta);

      positions.resize(cols * rows);
      std::iota(positions.begin(), positions.end(), 0);
      std::shuffle(positions.begin(), positions.end(), util::rand_engine());

      int total_iterate = 0, processed = 0;
      double min_value = 1.0;
      double max_value = 0.0;
      for (int pos: positions) {
        processed++;
        int const x = pos % cols;
        int const y = pos / cols;
        if (resample_safe(x, y)) continue;

        double const power = calculate_power_at(x, y, &total_iterate);
        get(x, y) = power;
        min_value = std::min(min_value, power);
        max_value = std::max(max_value, power);

        if ((total_iterate > 1000000 && (double) processed / positions.size() > 0.2) ||
          total_iterate > 1000000 * 5) break;
      }
      this->prev_avail = true;
      this->update_range(min_value, max_value);
    }

  private:
    static constexpr double mix_ratio = 0.2;
    double min_power = 0.0;
    double max_power = 1.0;
    double range = 1.0;

    static constexpr std::size_t level_bins = 100;
    std::vector<double> level_mapping;
    std::vector<int> histogram;

  public:
    void update_range(double min_value, double max_value) {
      this->min_power = (1.0 - mix_ratio) * min_power + mix_ratio * min_value;
      this->max_power = (1.0 - mix_ratio) * max_power + mix_ratio * max_value;
      this->range = std::max(max_power - min_power, 1.0 / max_iterate);

      histogram.resize(level_bins);
      level_mapping.resize(level_bins + 1);
      std::fill(histogram.begin(), histogram.end(), 0);
      int const max_bin_content = cols * rows / 10;
      int count = 0;
      for (double power: data) {
        double const value = (power - min_power) / range;
        if (value < 0.0 || 1.0 < value) continue;
        auto& bin = histogram[std::min<int>(value * level_bins, level_bins - 1)];
        if (bin < max_bin_content) bin++, count++;
      }
      int accum = 0, index = 0;
      for (int h: histogram) {
        level_mapping[index] = count ? (double) accum / count : (double) index / level_bins;
        index++;
        accum += h;
      }
      level_mapping.back() = 1.0;
    }

    double operator()(int x, int y) {
      double power = data[y * cols + x];
      if (power < 0) {
        if (util::rand() % 10 == 0) {
          power = calculate_power_at(x, y, nullptr);
          data[y * cols + x] = power;
        } else {
          power = get_average(x, y, 3);
        }
        // power = get_average(x, y, 2);
        // if (power >= 0.0) {
        //   power += range * 0.2 * (util::randf() - 0.5);
        // } else {
        //   power = calculate_power_at(x, y, nullptr);
        //   data[y * cols + x] = power;
        // }
      }
      double const value = std::clamp((power - min_power) / range, 0.0, 1.0);

      // level_mapping 線形補間
      double const frac = value * level_bins;
      int const index = std::min<int>(std::ceil(frac), level_bins - 1);
      double const p1 = level_mapping[index];
      double const p2 = level_mapping[index + 1];
      double const p = p1 + (frac - index) * (p2 - p1);
      double const pscale = std::clamp(p - 0.2, 0.0, 0.7) / 0.7;

      return value + 0.5 * (pscale * pscale - value);
    }
  };

}

#endif
