# A. Разбиение на пары


def get_bit(mask, i):
    return (mask >> i) & 1


def main():
    n = int(input())
    adjacency_matrix = [
        [x == 'Y' for x in input()]
        for _ in range(n)
    ]

    dp = [0] * (1 << n)
    for mask in range(1, len(dp)):
        for i in range(n):
            if get_bit(mask, i) == 1:
                dp[mask] = dp[mask - (1 << i)]
                for j in range(n - 1):
                    if get_bit(mask, j) == 1 and adjacency_matrix[i][j]:
                        dp[mask] = max(dp[mask], dp[mask - (1 << i) - (1 << j)] + 1)
    print(dp[-1] * 2)


if __name__ == '__main__':
    main()
