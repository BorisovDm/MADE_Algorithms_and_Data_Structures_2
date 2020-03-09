# B. Удаление скобок 2.0

brackets_mapping = {
    '(': ')',
    '[': ']',
    '{': '}',
}


def restore_path(string, dp, l_idx, r_idx):
    if l_idx >= r_idx:
        return ''

    sep_idx = dp[l_idx][r_idx][1]
    if sep_idx == -1:
        return string[l_idx] + restore_path(string, dp, l_idx + 1, r_idx - 1) + string[r_idx]

    return restore_path(string, dp, l_idx, sep_idx) + restore_path(string, dp, sep_idx + 1, r_idx)


def main():
    brackets_string = input()
    n_brackets = len(brackets_string)

    dp = [
        [(0, None)] * n_brackets
        for _ in range(n_brackets)
    ]

    for idx in range(n_brackets):
        dp[idx][idx] = (1, None)

    for l_idx in range(n_brackets - 2, -1, -1):
        for r_idx in range(l_idx + 1, n_brackets):
            n_deletions, deletion_idx = float('inf'), None
            if brackets_mapping.get(brackets_string[l_idx]) == brackets_string[r_idx]:
                n_deletions = dp[l_idx + 1][r_idx - 1][0]
                deletion_idx = -1

            for k in range(l_idx, r_idx):
                temp_n_deletions = dp[l_idx][k][0] + dp[k + 1][r_idx][0]
                if temp_n_deletions < n_deletions:
                    n_deletions = temp_n_deletions
                    deletion_idx = k

            dp[l_idx][r_idx] = (n_deletions, deletion_idx)

    print(restore_path(brackets_string, dp, 0, n_brackets - 1))


if __name__ == '__main__':
    main()
