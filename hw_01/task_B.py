# B. Черепаха и монеты


def main():
    n, m = map(int, input().split())
    coins_map = [
        list(map(int, input().split()))
        for _ in range(n)
    ]

    accum_coins_map = [
        [None] * m
        for _ in range(n)
    ]
    accum_coins_map[0][0] = (coins_map[0][0], None)

    # forward step
    for row_idx in range(n):
        for col_idx in range(m):
            if row_idx == 0 and col_idx == 0:
                continue

            curr_value = coins_map[row_idx][col_idx]
            if row_idx == 0:
                result = (accum_coins_map[row_idx][col_idx - 1][0] + curr_value, 'R')
            elif col_idx == 0:
                result = (accum_coins_map[row_idx - 1][col_idx][0] + curr_value, 'D')
            else:
                left_value = accum_coins_map[row_idx][col_idx - 1][0]
                upper_value = accum_coins_map[row_idx - 1][col_idx][0]
                result = (left_value + curr_value, 'R') if left_value > upper_value else (upper_value + curr_value, 'D')

            accum_coins_map[row_idx][col_idx] = result

    # backward step
    reconstructed_path = []
    row_idx, col_idx = n - 1, m - 1

    while not (row_idx == 0 and col_idx == 0):
        step_direction = accum_coins_map[row_idx][col_idx][1]
        reconstructed_path.append(step_direction)
        if step_direction == 'R':
            col_idx -= 1
        else:
            row_idx -= 1
    reconstructed_path = ''.join(reversed(reconstructed_path))

    # print answer
    print(accum_coins_map[-1][-1][0])
    print(reconstructed_path)


if __name__ == '__main__':
    main()
