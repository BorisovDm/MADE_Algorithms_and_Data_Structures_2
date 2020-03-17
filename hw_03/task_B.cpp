// B. Просеивай!

#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n;
    std::cin >> n;

    std::vector<int> min_prime_divisor(n + 1, -1);
    for (int i = 2; i < min_prime_divisor.size(); i++) {
        if (min_prime_divisor[i] > 0) {
            continue;
        }

        for (int j = i; j < min_prime_divisor.size(); j += i) {
            if (min_prime_divisor[j] < 0) {
                min_prime_divisor[j] = i;
            }
        }
    }

    long long ans_d = 0;
    for (int i = 2; i < min_prime_divisor.size(); i++) {
        ans_d += min_prime_divisor[i];
    }

    long long ans_s0 = 1;
    long long ans_s1 = 1;
    long long ans_phi = 1;

    for (int i = 2; i < min_prime_divisor.size(); i++) {
        int number = i;
        long long n_divisors = 1;
        long long divisors_sum = 1;
        long long temp_phi = 1;

        int divisor = -1;
        int n_div = 0;

        while (number != 1) {
            if (divisor == min_prime_divisor[number]) {
                number /= divisor;
                n_div++;
            } else {
                if (divisor > 0) {
                    n_divisors *= n_div + 1;
                    long long divisor_pow = pow(divisor, n_div - 1);
                    temp_phi *= divisor_pow * (divisor - 1);
                    divisors_sum *= (divisor_pow * divisor * divisor - 1) / (divisor - 1);
                }

                divisor = min_prime_divisor[number];
                number /= divisor;
                n_div = 1;
            }
        }

        n_divisors *= n_div + 1;
        long long divisor_pow = pow(divisor, n_div - 1);
        temp_phi *= divisor_pow * (divisor - 1);
        divisors_sum *= (divisor_pow * divisor * divisor - 1) / (divisor - 1);

        ans_s0 += n_divisors;
        ans_s1 += divisors_sum;
        ans_phi += temp_phi;
    }

    std::cout << ans_d << ' ' << ans_s0 << ' ' << ans_s1 << ' ' << ans_phi << '\n';
    return 0;
}
