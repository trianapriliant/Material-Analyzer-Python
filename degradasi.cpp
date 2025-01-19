// degradasi.cpp
#include <vector>
#include <cmath>
#include <stdexcept>

extern "C" {
    // Fungsi untuk menghitung ln(A0/At)
    void hitung_ln_A0_At(double* A0, double* At, double* ln_A0_At, int n) {
        for (int i = 0; i < n; i++) {
            ln_A0_At[i] = std::log(A0[0] / At[i]);
        }
    }

    // Fungsi untuk fitting data linier (y = k * t + C)
    void fitting_linier(double* t, double* y, int n, double* k, double* C) {
        double sum_t = 0.0, sum_y = 0.0, sum_ty = 0.0, sum_tt = 0.0;
        for (int i = 0; i < n; i++) {
            sum_t += t[i];
            sum_y += y[i];
            sum_ty += t[i] * y[i];
            sum_tt += t[i] * t[i];
        }
        double denominator = n * sum_tt - sum_t * sum_t;
        if (denominator == 0) {
            throw std::runtime_error("Pembagian oleh nol dalam fitting linier.");
        }
        *k = (n * sum_ty - sum_t * sum_y) / denominator;
        *C = (sum_y - (*k) * sum_t) / n;
    }
}