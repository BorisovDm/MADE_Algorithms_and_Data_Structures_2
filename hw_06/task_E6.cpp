// E. Самое дешевое ребро

#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

#define INF std::numeric_limits<int>::max()

class WeightedTree {
public:
    explicit WeightedTree(const std::vector<int>& parents_, const std::vector<int>& weights_);
    int lca_min_edge(int u, int v) const;
private:
    int size;
    std::vector<int> parents;
    std::vector<int> weights;
    std::vector<int> depth;
    std::vector<std::vector<int>> adjacency_list;
    std::vector<std::vector<int>> jumps;
    std::vector<std::vector<int>> min_edges;

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
    min_edges = std::vector<std::vector<int>>(size, std::vector<int>(degree2 + 1));
    for (int i = 0; i < jumps[0].size(); i++) {
        for (int v = 0; v < size; v++) {
            if (i == 0) {
                jumps[v][i] = parents[v];
                min_edges[v][i] = weights[v];
            } else {
                int u = jumps[v][i - 1];
                jumps[v][i] = jumps[u][i - 1];
                min_edges[v][i] = std::min(min_edges[v][i - 1], min_edges[u][i - 1]);
            }
        }
    }
}

WeightedTree::WeightedTree(const std::vector<int>& parents_, const std::vector<int>& weights_) {
    parents.assign(parents_.begin(), parents_.end());
    weights.assign(weights_.begin(), weights_.end());
    size = parents.size();

    adjacency_list = std::vector<std::vector<int>>(size);
    for (int i = 1; i < size; i++) {
        adjacency_list[parents[i]].push_back(i);
    }

    calc_depth();
    calc_jumps();
}

int WeightedTree::lca_min_edge(int u, int v) const {
    int min_edge = INF;
    if (depth[u] < depth[v]) {
        std::swap(u, v);
    }

    int delta = depth[u] - depth[v];
    for (int k = jumps[0].size() - 1; k >= 0; k--) {
        if (delta >= (1 << k)) {
            min_edge = std::min(min_edge, min_edges[u][k]);
            u = jumps[u][k];
            delta -= (1 << k);
        }
    }

    if (u == v) {
        return min_edge;
    }

    for (int k = jumps[0].size() - 1; k >= 0; k--) {
        int u1 = jumps[u][k];
        int v1 = jumps[v][k];

        if (u1 != v1) {
            min_edge = std::min(min_edge, min_edges[u][k]);
            min_edge = std::min(min_edge, min_edges[v][k]);
            u = u1;
            v = v1;
        }
    }

    min_edge = std::min(min_edge, min_edges[u][0]);
    min_edge = std::min(min_edge, min_edges[v][0]);

    return min_edge;
}

int main() {
    std::ifstream fin("minonpath.in");

    int n;
    fin >> n;

    std::vector<int> tree_parents(n);
    std::vector<int> tree_weights(n);
    tree_parents[0] = 0;
    tree_weights[0] = INF;

    for (int i = 1; i < n; i++) {
        int parent, weight;
        fin >> parent >> weight;
        tree_parents[i] = parent - 1;
        tree_weights[i] = weight;
    }
    WeightedTree tree(tree_parents, tree_weights);

    int m;
    fin >> m;

    std::ofstream fout;
    fout.open("minonpath.out");
    for (int i = 0; i < m; i++) {
        int u, v;
        fin >> u >> v;
        fout << tree.lca_min_edge(u - 1, v - 1) << "\n";
    }

    return 0;
}
