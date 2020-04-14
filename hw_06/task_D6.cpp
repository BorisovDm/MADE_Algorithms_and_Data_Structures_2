// D. LCA

#include <algorithm>
#include <iostream>
#include <vector>


class WeightedTree {
public:
    explicit WeightedTree(const std::vector<int>& tree_parents);
    int lca_min_edge(int u, int v) const;
private:
    int size;
    std::vector<int> parents;
    std::vector<int> depth;
    std::vector<std::vector<int>> adjacency_list;
    std::vector<std::vector<int>> jumps;

    void calc_depth();
    void calc_jumps();
};

void WeightedTree::calc_depth() {
    int root_idx = 0;
    depth = std::vector<int>(parents.size());
    depth[root_idx] = 0;

    std::vector<int> temp_stack;
    temp_stack.push_back(root_idx);

    while (!temp_stack.empty()) {
        int parent_idx = temp_stack.back();
        temp_stack.pop_back();

        for (auto child_idx: adjacency_list[parent_idx]) {
            temp_stack.push_back(child_idx);
            depth[child_idx] = depth[parent_idx] + 1;
        }
    }
}

void WeightedTree::calc_jumps() {
    int max_depth = *std::max_element(depth.begin(), depth.end());
    int degree2 = 0, pow2 = 1;
    while (pow2 < max_depth) {
        degree2++;
        pow2 *= 2;
    }

    jumps = std::vector<std::vector<int>>(size, std::vector<int>(degree2 + 1));
    for (int i = 0; i < jumps[0].size(); i++) {
        for (int v = 0; v < size; v++) {
            if (i == 0) {
                jumps[v][i] = parents[v];
            } else {
                jumps[v][i] = jumps[jumps[v][i - 1]][i - 1];
            }
        }
    }
}

WeightedTree::WeightedTree(const std::vector<int>& tree_parents) {
    parents.assign(tree_parents.begin(), tree_parents.end());
    size = parents.size();

    adjacency_list = std::vector<std::vector<int>>(size);
    for (int i = 1; i < size; i++) {
        adjacency_list[parents[i]].push_back(i);
    }

    calc_depth();
    calc_jumps();
}

int WeightedTree::lca_min_edge(int u, int v) const {
    if (depth[u] < depth[v]) {
        std::swap(u, v);
    }

    int delta = depth[u] - depth[v];
    for (int k = jumps[0].size() - 1; k >= 0; k--) {
        if (delta >= (1 << k)) {
            u = jumps[u][k];
            delta -= (1 << k);
        }
    }

    if (u == v) {
        return u;
    }

    for (int k = jumps[0].size() - 1; k >= 0; k--) {
        int u1 = jumps[u][k];
        int v1 = jumps[v][k];

        if (u1 != v1) {
            u = u1;
            v = v1;
        }
    }
    return jumps[u][0];
}

int main() {
    std::ios::sync_with_stdio(false), std::cin.tie(0), std::cout.tie(0);

    int n;
    std::cin >> n;

    std::vector<int> tree_parents(n);
    tree_parents[0] = 0;
    for (int i = 1; i < n; i++) {
        int x;
        std::cin >> x;
        tree_parents[i] = x - 1;
    }
    WeightedTree tree(tree_parents);

    int m;
    std::cin >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        std::cin >> u >> v;
        std::cout << tree.lca_min_edge(u - 1, v - 1) + 1 << "\n";
    }

    return 0;
}
