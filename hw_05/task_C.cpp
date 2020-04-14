// C. RMQ2

#include <algorithm>
#include <iostream>
#include <limits>
#include <vector>


#define NEUTRAL_ELEMENT std::numeric_limits<long long>::max()
#define INF std::numeric_limits<long long>::max()


long long get(int v, std::vector<long long>& segment_tree, std::vector<long long>& add_storage, std::vector<long long>& set_storage) {
    if (set_storage[v] == INF) {
        return segment_tree[v] + add_storage[v];
    }
    return set_storage[v] + add_storage[v];
}



void push(int v, int l, int r,
        std::vector<long long>& segment_tree, std::vector<long long>& add_storage, std::vector<long long>& set_storage) {
    if (l == r) {
        segment_tree[v] = get(v, segment_tree,add_storage, set_storage);
//        segment_tree[v] += add_storage[v];
    } else {
//        if (set_storage[v] != INF) {
//            segment_tree[v] = set_storage[v] + add_storage[v];
//            set_storage[2 * v + 1] = set_storage[v];
//            set_storage[2 * v + 2] = set_storage[v];
//
//            add_storage[2 * v + 1] = add_storage[v];
//            add_storage[2 * v + 2] = add_storage[v];
//        } else {
//            add_storage[2 * v + 1] += add_storage[v];
//            add_storage[2 * v + 2] += add_storage[v];
//            int m = (l + r) / 2;
//            segment_tree[v] = std::min(get(2 * v + 1, l, m, segment_tree, add_storage, set_storage), get(2 * v + 2, m + 1, r, segment_tree, add_storage, set_storage));
//
//        }
//        int m = (l + r) / 2;
//        segment_tree[v] = std::min(get(2 * v + 1, l, m, segment_tree, add_storage, set_storage), get(2 * v + 2, m + 1, r, segment_tree, add_storage, set_storage));


        if (set_storage[v] == INF) {
            add_storage[2 * v + 1] += add_storage[v];
            add_storage[2 * v + 2] += add_storage[v];
            segment_tree[v] = std::min(get(2 * v + 1, segment_tree, add_storage, set_storage), get(2 * v + 2, segment_tree, add_storage, set_storage));
        } else {
            segment_tree[v] = set_storage[v] + add_storage[v];
            set_storage[2 * v + 1] = set_storage[v];
            set_storage[2 * v + 2] = set_storage[v];

            add_storage[2 * v + 1] = add_storage[v];
            add_storage[2 * v + 2] = add_storage[v];

//            segment_tree[v] = std::min(get(2 * v + 1, segment_tree, add_storage, set_storage), get(2 * v + 2, segment_tree, add_storage, set_storage));
        }
    }

    set_storage[v] = INF;
    add_storage[v] = 0;
}


long long rmq(int v, int l, int r, int a, int b,
        std::vector<long long>& segment_tree, std::vector<long long>& add_storage, std::vector<long long>& set_storage) {
    push(v, l, r, segment_tree, add_storage, set_storage);

    if (l > b || r < a) {
        return NEUTRAL_ELEMENT;
    }

    if (l >= a && r <= b) {
        return get(v, segment_tree,add_storage, set_storage); //segment_tree[v];
    }

    int m = (l + r) / 2;
    return std::min(rmq(2 * v + 1, l, m, a, b, segment_tree, add_storage, set_storage), rmq(2 * v + 2, m + 1, r, a, b, segment_tree, add_storage, set_storage));
}


void set(int v, int l, int r, int a, int b, int x,
        std::vector<long long>& segment_tree, std::vector<long long>& add_storage, std::vector<long long>& set_storage) {
    push(v, l, r, segment_tree, add_storage, set_storage);

    if (l > b || r < a) {
        return;
    }

    if (l >= a && r <= b) {
        set_storage[v] = x;
        add_storage[v] = 0;
        return;
    }

    int m = (l + r) / 2;
    set(2 * v + 1, l, m, a, b, x, segment_tree, add_storage, set_storage);
    set(2 * v + 2, m + 1, r, a, b, x, segment_tree, add_storage, set_storage);
}

void add(int v, int l, int r, int a, int b, int x,
        std::vector<long long>& segment_tree, std::vector<long long>& add_storage, std::vector<long long>& set_storage) {
    push(v, l, r, segment_tree, add_storage, set_storage);

    if (l > b || r < a) {
        return;
    }

    if (l >= a && r <= b) {
        add_storage[v] += x;
        return;
    }

    int m = (l + r) / 2;
    add(2 * v + 1, l, m, a, b, x, segment_tree, add_storage, set_storage);
    add(2 * v + 2, m + 1, r, a, b, x, segment_tree, add_storage, set_storage);
}


int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n;
    std::cin >> n;

    int degree2_size = 1;
    while (degree2_size < n) {
        degree2_size *= 2;
    }

//    std::cout << degree2_size << " " << NEUTRAL_ELEMENT;

    std::vector<long long> segment_tree(2 * degree2_size - 1);
    for (int i = degree2_size - 1; i < degree2_size - 1 + n; i++) {
        std::cin >> segment_tree[i];
    }
    for (int i = degree2_size - 1 + n; i < segment_tree.size(); i++) {
        segment_tree[i] = NEUTRAL_ELEMENT;
    }

    for (int i = degree2_size - 2; i >= 0; i--) {
        segment_tree[i] = std::min(segment_tree[2 * i + 1], segment_tree[2 * i + 2]);
    }

    std::vector<long long> add_storage(2 * degree2_size - 1, 0);
    std::vector<long long> set_storage(2 * degree2_size - 1, INF);

    std::string command;
    while (std::cin >> command) {
        if (command == "min") {
            int i, j;
            std::cin >> i >> j;
            std::cout << rmq(0, 0, degree2_size - 1, i - 1, j - 1, segment_tree, add_storage, set_storage) << '\n';
            continue;
        }

        if (command == "set") {
            int i, j, x;
            std::cin >> i >> j >> x;
            set(0, 0, degree2_size - 1, i - 1, j - 1, x, segment_tree, add_storage, set_storage);

            for (int i = 0; i < segment_tree.size(); i++) {
                std::cout << i << " " << segment_tree[i] << ' ' << set_storage[i] << " " << add_storage[i] << '\n';
            }
//            std::cout << '\n';
//
//            for (auto x: segment_tree) {
//                std::cout << x << ' ';
//            }
//            std::cout << '\n';


            continue;
        }

        if (command == "add") {
            int i, j, x;
            std::cin >> i >> j >> x;
            add(0, 0, degree2_size - 1, i - 1, j - 1, x, segment_tree, add_storage, set_storage);


            for (int i = 0; i < segment_tree.size(); i++) {
                std::cout << i << " " << segment_tree[i] << ' ' << set_storage[i] << " " << add_storage[i] << '\n';
            }


//            for (auto x: segment_tree) {
//                std::cout << x << ' ';
//            }
//            std::cout << '\n';


            continue;
        }
    }

    return 0;
}




//5
//1 2 3 4 5
//min 2 5
//min 1 5
//min 1 4
//min 2 4
//add 3 5 1
//min 1 3
//add 1 2 4
//min 1 3
//

//1
//1
//
//2
//add 3 5 1
//min 1 3
//1
//add 1 2 4
//min 1 3
//1




