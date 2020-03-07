# E. Замощение доминошками


def main():
    n, m = map(int, input().split())
    board = [input() + 'X' for _ in range(n)]

    dp = [[0] * (1 << n) for _ in range(n * m + 1)]
    dp[0][0] = 1

    for x in range(len(dp) - 1):
        row_idx, col_idx = x % n, x // n
        for mask in range(len(dp[0])):
            board_cell = board[row_idx][col_idx]
            if (board_cell == 'X' and mask & 1 == 0) or (board_cell == '.' and mask & 1 == 1):
                next_mask = mask >> 1
                dp[x + 1][next_mask] += dp[x][mask]

            if board_cell == '.' and mask & 1 == 0:
                if board[row_idx][col_idx + 1] == '.':
                    next_mask = (mask >> 1) + (1 << (n - 1))
                    dp[x + 1][next_mask] += dp[x][mask]

                if mask & 2 == 0 and row_idx + 1 < n and board[row_idx + 1][col_idx] == '.':
                    next_mask = (mask >> 1) + 1
                    dp[x + 1][next_mask] += dp[x][mask]

    print(dp[-1][0])


if __name__ == '__main__':
    main()
