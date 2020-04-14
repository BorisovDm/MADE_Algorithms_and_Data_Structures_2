// A. Звезды

#include <iostream>
#include <vector>


class FenwickTree3D {
public:
    explicit FenwickTree3D(int size);
    void Add(int x, int y, int z, int value);
    long long Rsq(int x1, int y1, int z1, int x2, int y2, int z2) const;
private:
    int size;
    std::vector<std::vector<std::vector<int>>> state3d;
    long long Get(int x, int y, int z) const;
};

FenwickTree3D::FenwickTree3D(int size_) {
    size = size_;
    state3d = std::vector<std::vector<std::vector<int>>>(size, std::vector<std::vector<int>>(size, std::vector<int>(size, 0)));
}

long long FenwickTree3D::Get(int x, int y, int z) const {
    if (x < 0 || y < 0 || z < 0) {
        return 0;
    }

    long long result = 0;
    for (int i = x; i >= 0; i = (i & (i + 1)) - 1) {
        for (int j = y; j >= 0; j = (j & (j + 1)) - 1) {
            for (int k = z; k >= 0; k = (k & (k + 1)) - 1) {
                result += state3d[i][j][k];
            }
        }
    }
    return result;
}

void FenwickTree3D::Add(int x, int y, int z, int value) {
    for (int i = x; i < size; i = i | (i + 1)) {
        for (int j = y; j < size; j = j | (j + 1)) {
            for (int k = z; k < size; k = k | (k + 1)) {
                state3d[i][j][k] += value;
            }
        }
    }
}

long long FenwickTree3D::Rsq(int x1, int y1, int z1, int x2, int y2, int z2) const {
    long long result =  Get(x2, y2, z2)
        - Get(x1 - 1, y2, z2) - Get(x2, y1 - 1, z2) - Get(x2, y2, z1 - 1)
        + Get(x1 - 1, y1 - 1, z2) + Get(x2, y1 - 1, z1 - 1) + Get(x1 - 1, y2, z1 - 1)
        - Get(x1 - 1, y1 - 1, z1 - 1);
    return result;
}

int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n;
    std::cin >> n;
    FenwickTree3D fenwick_tree(n);

    while (true) {
        int command;
        std::cin >> command;

        if (command == 1) {
            int x, y, z, k;
            std::cin >> x >> y >> z >> k;
            fenwick_tree.Add(x, y, z, k);
            continue;
        }

        if (command == 2) {
            int x1, y1, z1, x2, y2, z2;
            std::cin >> x1 >> y1 >> z1 >> x2 >> y2 >> z2;
            std::cout << fenwick_tree.Rsq(x1, y1, z1, x2, y2, z2) << '\n';
            continue;
        }

        if (command == 3) {
            break;
        }
    }

    return 0;
}
