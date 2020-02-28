# A. Кузнечик собирает монеты


INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'


def find_max_with_index(arr, start_idx, end_idx):
    max_value_idx = start_idx
    max_value = arr[max_value_idx]

    for idx, value in enumerate(arr[start_idx: end_idx], start=start_idx):
        if value > max_value:
            max_value = value
            max_value_idx = idx

    return max_value, max_value_idx


def main():
    with open(INPUT_FILE_NAME, 'r') as fin:
        n, k = map(int, fin.readline().split())
        coins = list(map(int, fin.readline().split()))

    coins.append(0)  # for the last point
    accum_coins = [0]
    index_from = [None]  # to restore the path

    for i in range(1, n):
        max_value, max_value_idx = find_max_with_index(accum_coins, max(0, i - k), i)
        accum_coins.append(max_value + coins[i - 1])
        index_from.append(max_value_idx)

    restored_path = [len(accum_coins) - 1]
    while restored_path[-1] != 0:
        restored_path.append(index_from[restored_path[-1]])

    with open(OUTPUT_FILE_NAME, 'w') as fout:
        print(accum_coins[-1], file=fout)
        print(len(restored_path) - 1, file=fout)
        print(' '.join(reversed(list(map(lambda x: str(x + 1), restored_path)))), file=fout)


if __name__ == '__main__':
    main()
