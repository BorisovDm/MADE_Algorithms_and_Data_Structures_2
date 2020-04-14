// D. Разреженные таблицы

#include <algorithm>
#include <iostream>
#include <vector>


int rmq_query(const std::vector<std::vector<int>>& rmq, int l, int r, const std::vector<int>& pow2) {
    int width = r - l;
    int degree_step = pow2[width];

    if ((1 << degree_step) == width) {
        return rmq[l][degree_step];
    }
    return std::min(rmq[l][degree_step], rmq[r - (1 << degree_step)][degree_step]);
}


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n, m, a0;
    std::cin >> n >> m >> a0;

    // fill array a
    std::vector<int> array_a(n);
    array_a[0] = a0;
    for (int i = 1; i < array_a.size(); i++) {
        array_a[i] = (23 * array_a[i - 1] + 21563) % 16714589;
    }

    // fill pow2 vector
    std::vector<int> pow2(n + 1);
    pow2[0] = -1;
    int next_update_idx = 1;
    for (int i = 1; i < pow2.size(); i++) {
        pow2[i] = pow2[i - 1];
        if (i == next_update_idx) {
            pow2[i]++;
            next_update_idx *= 2;
        }
    }

    // fill rmq array
    std::vector<std::vector<int>> rmq(n, std::vector<int>(pow2[n] + 1));
    for (int left = 0; left < rmq.size(); left++) {
        rmq[left][0] = array_a[left];
    }

    for (int k = 1; k < rmq[0].size(); k++) {
        for (int left = 0; left < rmq.size(); left++) {
            if (left + (1 << k) > n) {
                break;
            }
            rmq[left][k] = std::min(rmq[left][k - 1], rmq[left + (1 << (k - 1))][k - 1]);
        }
    }

    // run queries
    int u, v, r;
    for (int i = 1; i < m + 1; i++) {
        if (i == 1) {
            std::cin >> u >> v;
        } else {
            u = ((17 * u + 751 + r + 2 * (i - 1)) % n) + 1;
            v = ((13 * v + 593 + r + 5 * (i - 1)) % n) + 1;
        }
        r = rmq_query(rmq, std::min(u, v) - 1, std::max(u, v), pow2);
    }
    std::cout << u << " " << v << " " << r << "\n";

    return 0;
}
