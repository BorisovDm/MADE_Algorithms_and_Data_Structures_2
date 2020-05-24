// B. Множественный поиск

#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>


std::vector<int> build_suff_array(const std::string& s) {
    std::set<char> ordered_unique_symbols(s.begin(), s.end());
    const char delimiter = char(*ordered_unique_symbols.begin() - 1);

    std::unordered_map<char, int> symbol_to_class;
    symbol_to_class[delimiter] = 0;
    for (const auto& symbol: ordered_unique_symbols) {
        symbol_to_class[symbol] = symbol_to_class.size();
    }

    const std::string new_s = s + delimiter;
    const int length = new_s.size();

    std::vector<int> cnt(symbol_to_class.size(), 0);
    for (const auto& symbol: new_s) {
        cnt[symbol_to_class[symbol]]++;
    }
    for (int i = 1; i < cnt.size(); i++) {
        cnt[i] += cnt[i - 1];
    }

    std::vector<int> suff(length);
    for (int i = 0; i < length; i++) {
        suff[--cnt[symbol_to_class[new_s[i]]]] = i;
    }

    std::vector<int> classes(length);
    for (int i = 0; i < length; i++) {
        classes[suff[i]] = symbol_to_class[new_s[suff[i]]];
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

    return suff;
}


bool check_prefix_in_suffix_array(const std::vector<int>& suff, const std::string& s, const std::string& t) {
    int left = 0;
    int right = suff.size();

    while (left <= right) {
        int middle = (left + right) / 2;
        int start_idx = suff[middle];

        for (int i = 0; ; i++) {
            if (i >= t.size()) {
                return true;
            }

            if (start_idx + i >= s.size() or t[i] > s[start_idx + i]) {
                left = middle + 1;
                break;
            }

            if (t[i] < s[start_idx + i]) {
                right = middle - 1;
                break;
            }
        }
    }

    return false;
}


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n_queries;
    std::cin >> n_queries;
    std::vector<std::string> queries(n_queries);
    for (auto& x: queries) {
        std::cin >> x;
    }

    std::string s;
    std::cin >> s;
    std::vector<int> suff = build_suff_array(s);

    for (auto& query: queries) {
        std::cout << (check_prefix_in_suffix_array(suff, s, query) ? "YES" : "NO") << '\n';
    }

    return 0;
}
