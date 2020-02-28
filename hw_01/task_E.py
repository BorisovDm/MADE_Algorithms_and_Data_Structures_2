# E. Кафе


INF = float('inf')


def main():
    n = int(input())
    lunch_prices = [int(input()) for _ in range(n)]

    min_prices_matrix = [[INF] * (n + 2) for _ in range(n + 1)]
    min_prices_matrix[0][0] = 0

    # fill matrix
    n_rows, n_cols = len(min_prices_matrix), len(min_prices_matrix[0]) - 1  # right column is fictitious
    for row_idx in range(1, n_rows):
        lunch_price = lunch_prices[row_idx - 1]
        for col_idx in range(n_cols):
            if lunch_price > 100:
                min_price = min(
                    INF if col_idx == 0 else min_prices_matrix[row_idx - 1][col_idx - 1] + lunch_price,
                    min_prices_matrix[row_idx - 1][col_idx + 1],
                )
            else:
                min_price = min(
                    min_prices_matrix[row_idx - 1][col_idx] + lunch_price,
                    min_prices_matrix[row_idx - 1][col_idx + 1],
                )
            min_prices_matrix[row_idx][col_idx] = min_price

    # find min_price and k_1
    min_price_idx = 0
    min_price_value = min_prices_matrix[-1][min_price_idx]
    for col_idx, value in enumerate(min_prices_matrix[-1]):
        if value <= min_price_value:
            min_price_value = value
            min_price_idx = col_idx

    # reconstruct path
    days_with_coupon = []
    next_sum, col_idx = min_price_value, min_price_idx
    for row_idx in range(n_rows - 2, 0, -1):
        if min_prices_matrix[row_idx][col_idx + 1] == next_sum:
            days_with_coupon.append(row_idx + 1)
            col_idx += 1
        else:
            launch_price = lunch_prices[row_idx]
            if next_sum == min_prices_matrix[row_idx][col_idx] + launch_price and launch_price <= 100:
                pass
            else:
                col_idx -= 1
            next_sum -= launch_price

    days_with_coupon = list(reversed(days_with_coupon))

    print(min_price_value)
    print(min_price_idx, len(days_with_coupon))
    print(*days_with_coupon)


if __name__ == '__main__':
    main()
