// A. Массовое разложение на множители

#include <iostream>
#include <vector>

#define MAX_N 1000000


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    std::vector<int> linear_sieve(MAX_N + 1, -1);  // store min prime divisor
    for (int i = 2; i < linear_sieve.size(); i++) {
        if (linear_sieve[i] > 0) {
            continue;
        }

        for (int j = i; j < linear_sieve.size(); j += i) {
            if (linear_sieve[j] < 0) {
                linear_sieve[j] = i;
            }
        }
    }

    int n;
    std::cin >> n;

    int min_prime_divisor, number;
    for (int i = 0; i < n; i++) {
        std::cin >> number;
        while (number != 1) {
            min_prime_divisor = linear_sieve[number];
            number /= min_prime_divisor;
            std::cout << min_prime_divisor << ' ';
        }
        std::cout << '\n';
    }

    return 0;
}
