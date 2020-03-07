# C. Выбор вершин дерева

from collections import defaultdict


def main():
    n = int(input())
    tree = [int(input()) - 1 for _ in range(n)]

    childs_mapping = defaultdict(list)
    for idx, parent_idx in enumerate(tree):
        if parent_idx == -1:
            root_idx = idx
        else:
            childs_mapping[parent_idx].append(idx)

    dp = [[0, 1] for _ in range(n)]
    nodes_stack = [(root_idx, 0)]

    while nodes_stack:
        node, status = nodes_stack.pop()
        if status == 1:
            for child_node in childs_mapping[node]:
                dp[node][0] += max(dp[child_node])
                dp[node][1] += dp[child_node][0]
        elif node in childs_mapping:
            nodes_stack.append((node, 1))
            for child_node in childs_mapping[node]:
                nodes_stack.append((child_node, 0))

    print(max(dp[root_idx]))


if __name__ == '__main__':
    main()
