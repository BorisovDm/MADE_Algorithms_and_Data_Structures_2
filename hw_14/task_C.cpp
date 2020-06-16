// C. ДНК Роботов

#include <cmath>
#include <complex>
#include <iostream>
#include <vector>

const double PI = std::atan(1.0) * 4;
const std::vector<char> chars = {'A', 'C', 'G', 'T'};

std::vector<std::complex<double>> recursive_fft(const std::vector<std::complex<double>>& coeffs) {
    int n = coeffs.size();
    if (n == 1) {
        return std::vector<std::complex<double>>(1, coeffs[0]);
    }

    std::vector<std::complex<double>> y_even(n / 2);
    std::vector<std::complex<double>> y_odd(n / 2);

    for (int i = 0; 2 * i < n; i++) {
        y_even[i] = coeffs[2 * i];
        y_odd[i] = coeffs[2 * i + 1];
    }

    y_even = recursive_fft(y_even);
    y_odd = recursive_fft(y_odd);

    double arg = 2 * PI / n;
    std::complex<double> w(1);
    std::complex<double> w_n(cos(arg), sin(arg));
    std::vector<std::complex<double>> y(n);

    for (int k = 0; 2 * k < n; k++) {
        y[k] = y_even[k] + w * y_odd[k];
        y[k + n / 2] = y_even[k] - w * y_odd[k];
        w *= w_n;
    }
    return y;
}


int main() {
    int size;
    std::string dna_1, dna_2;
    std::cin >> size >> dna_1 >> dna_2;

    std::vector<std::complex<double>> dna_1_polynom(2 * size);
    std::vector<std::complex<double>> dna_2_polynom(2 * size, 0);
    std::vector<std::complex<double>> accum_fft_sum(2 * size, 0);

    for (const auto& c: chars) {
        for (int i = 0; i < size; i++) {
            dna_1_polynom[i] = dna_1[i] == c;
            dna_2_polynom[i] = dna_2[size - 1 - i] == c;
        }
        for (int i = size; i < 2 * size; i++) {
            dna_1_polynom[i] = dna_1_polynom[i - size];
        }

        std::vector<std::complex<double>> dna_1_fft = recursive_fft(dna_1_polynom);
        std::vector<std::complex<double>> dna_2_fft = recursive_fft(dna_2_polynom);

        // write in reverse order
        for (int i = 0; i < 2 * size; i++) {
            accum_fft_sum[(-i + 2 * size) % (2 * size)] += dna_1_fft[i] * dna_2_fft[i];
        }
    }

    accum_fft_sum = recursive_fft(accum_fft_sum);
    std::vector<int> likelihood(2 * size);
    for (int i = 0; i < 2 * size; i++) {
        likelihood[i] = int(floor(accum_fft_sum[i].real() / (2 * size) + 0.5));
    }

    int max_matchings = 0;
    int max_matchings_idx = 0;
    for (int i = 0; i < 2 * size; i++) {
        if (likelihood[i] > max_matchings) {
            max_matchings = likelihood[i];
            max_matchings_idx = i;
        }
    }
    std::cout << max_matchings << ' ' << (max_matchings_idx + 1) % size;

    return 0;
}
