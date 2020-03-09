# D. Продавец аквариумов

INF = float('inf')


def get_bit(mask, i):
    return (mask >> i) & 1


def main():
    n = int(input())
    adjacency_matrix = [
        list(map(int, input().split()))
        for _ in range(n)
    ]

    dp = [[INF] * (1 << n) for _ in range(n)]
    for idx in range(n):
        dp[idx][0] = 0
    previous_node = [[None] * (1 << n) for _ in range(n)]

    for mask in range(1, len(dp[0])):
        for v_idx in range(n):
            for u_idx in range(n):
                if get_bit(mask, u_idx) == 1:
                    new_min_path = dp[u_idx][mask - (1 << u_idx)] + adjacency_matrix[u_idx][v_idx]
                    if new_min_path < dp[v_idx][mask]:
                        dp[v_idx][mask] = new_min_path
                        previous_node[v_idx][mask] = u_idx

    min_weight_path, edge_idx = INF, None
    for idx in range(n):
        if dp[idx][-1] < min_weight_path:
            min_weight_path = dp[idx][-1]
            edge_idx = idx

    path = [edge_idx]
    mask = len(dp[0]) - 1
    while mask:
        new_node = previous_node[path[-1]][mask]
        mask -= (1 << new_node)
        path.append(new_node)

    print(min_weight_path)
    print(*[x + 1 for x in path[1:]])


if __name__ == '__main__':
    main()
