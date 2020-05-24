// E. Циклические сдвиги

#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>


void find_cyclic_shift(const std::string& s, int k_shift) {
    std::set<char> ordered_unique_symbols(s.begin(), s.end());
    std::unordered_map<char, int> symbol_to_class;
    for (const auto& symbol: ordered_unique_symbols) {
        symbol_to_class[symbol] = symbol_to_class.size();
    }

    const int length = s.size();

    std::vector<int> cnt(symbol_to_class.size(), 0);
    for (const auto& symbol: s) {
        cnt[symbol_to_class[symbol]]++;
    }
    for (int i = 1; i < cnt.size(); i++) {
        cnt[i] += cnt[i - 1];
    }

    std::vector<int> suff(length);
    for (int i = 0; i < length; i++) {
        suff[--cnt[symbol_to_class[s[i]]]] = i;
    }

    std::vector<int> classes(length);
    for (int i = 0; i < length; i++) {
        classes[suff[i]] = symbol_to_class[s[suff[i]]];
    }

    int n_classes = symbol_to_class.size();
    for (int k = 0; (1 << k) < length; k++) {
        const int shift = 1 << k;

        std::vector<int> temp_suff(length);
        for (int i = 0; i < length; i++) {
            temp_suff[i] = (suff[i] - shift + length) % length;
        }

        std::vector<int> cnt(n_classes, 0);
        for (const auto& x: temp_suff) {
            cnt[classes[x]]++;
        }
        for (int i = 1; i < cnt.size(); i++) {
            cnt[i] += cnt[i - 1];
        }

        for (int i = length - 1; i >= 0; i--) {
            suff[--cnt[classes[temp_suff[i]]]] = temp_suff[i];
        }

        std::vector<int> temp_classes(length);
        n_classes = 0;
        classes[suff[0]] = 0;
        for (int i = 1; i < length; i++) {
            if (classes[suff[i]] != classes[suff[i - 1]] || classes[(suff[i] + shift) % length] != classes[(suff[i - 1] + shift) % length]) {
                n_classes++;
            }
            temp_classes[suff[i]] = n_classes;
        }
        n_classes++;
        classes = temp_classes;
    }

    for (int i = 0; i < length; i++)
        if (classes[i] == k_shift - 1) {
            for (int j = 0; j < length; j++) {
                std::cout << s[(j + i) % length];
            }
            return;
        }
    std::cout << "IMPOSSIBLE";

}


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);
    std::string s;
    std::cin >> s;

    int k;
    std::cin >> k;
    find_cyclic_shift(s, k);

    return 0;
}
