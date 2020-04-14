// B. RSQ

#include <iostream>
#include <vector>


class FenwickTree3D {
public:
    explicit FenwickTree3D(const std::vector<long long>& init_array);
    long long Get(int i) const;
    void Update(int i, long long x);
    void Set(int i, long long x);
    long long Rsq(int l, int r) const;

private:
    int Func_f(int i) const;
    int size;
    std::vector<long long> original_array;
    std::vector<long long> fenwick_tree;
};

FenwickTree3D::FenwickTree3D(const std::vector<long long>& init_array) {
    original_array.assign(init_array.begin(), init_array.end());
    size = original_array.size();

    fenwick_tree.resize(size, 0);
    for (int i = 0; i < size; i++) {
        for (int j = Func_f(i); j <= i; j++) {
            fenwick_tree[i] += original_array[j];
        }
    }
}

long long FenwickTree3D::Get(int i) const {
    long long res = 0;
    while (i >= 0) {
        res += fenwick_tree[i];
        i = Func_f(i) - 1;
    }
    return res;
}

void FenwickTree3D::Update(int i, long long x) {
    while (i < fenwick_tree.size()) {
        fenwick_tree[i] += x;
        i = i | (i + 1);
    }
}

void FenwickTree3D::Set(int i, long long x) {
    long long diff = x - original_array[i];
    original_array[i] = x;
    Update(i, diff);
}

long long FenwickTree3D::Rsq(int l, int r) const {
    if (l == 0) {
        return Get(r);
    }
    return Get(r) - Get(l - 1);
}

int FenwickTree3D::Func_f(int i) const {
    return i & (i + 1);
}

int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n;
    std::cin >> n;

    std::vector<long long> input_array(n);
    for (int i = 0; i < n; i++) {
        std::cin >> input_array[i];
    }
    FenwickTree3D fenwick_tree(input_array);

    std::string command;
    while (std::cin >> command) {
        if (command == "sum") {
            int i, j;
            std::cin >> i >> j;
            std::cout << fenwick_tree.Rsq(i - 1, j - 1) << '\n';
            continue;
        }

        if (command == "set") {
            long long i, x;
            std::cin >> i >> x;
            fenwick_tree.Set(i - 1, x);
        }
    }

    return 0;
}
