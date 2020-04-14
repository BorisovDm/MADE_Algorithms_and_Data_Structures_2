// A. Сумма простая

#include <algorithm>
#include <iostream>
#include <vector>

#define MOD_16 (1 << 16)
#define MOD_30 (1 << 30)


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n, x, y, a_0;
    std::cin >> n >> x >> y >> a_0;

    int m, z, t, b_0;
    std::cin >> m >> z >> t >> b_0;
    if (m == 0) {
        std::cout << 0 << '\n';
        return 0;
    }

    // calculate part_sum
    std::vector<long long> part_sum(n);
    part_sum[0] = a_0;
    for (int i = 1; i < part_sum.size(); i++) {
        part_sum[i] = (part_sum[i - 1] * x + y) & (MOD_16 - 1);
    }
    for (int i = 1; i < part_sum.size(); i++) {
        part_sum[i] += part_sum[i - 1];
    }

    // queries
    std::vector<long long> array_b(2 * m);
    array_b[0] = b_0;
    for (int i = 1; i < array_b.size(); i++) {
        array_b[i] = (array_b[i - 1] * z + t) % MOD_30;
        if (array_b[i] < 0) {
            array_b[i] += MOD_30;
        }
    }

    unsigned long long queries_sum = 0;
    for (int i = 0; i < m; i++) {
        int l = std::min(array_b[2 * i] % n, array_b[2 * i + 1] % n);
        int r = std::max(array_b[2 * i] % n, array_b[2 * i + 1] % n);
        long long querie_value = (l == 0 ? part_sum[r] : part_sum[r] - part_sum[l - 1]);
        queries_sum += querie_value;
    }
    std::cout << queries_sum << '\n';

    return 0;
}
