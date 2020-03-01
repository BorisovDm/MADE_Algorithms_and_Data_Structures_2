# C. Наибольшая возрастающая подпоследовательность


def main():
    n = int(input())
    sequence = list(map(int, input().split()))

    dp = [0] * n
    dp[0] = 1
    for i in range(1, n):
        for j in range(i):
            if sequence[j] < sequence[i] and dp[j] > dp[i]:
                dp[i] = dp[j]
        dp[i] += 1

    # restore longest increasing subsequence
    longest_inc_subseq = []
    lis_len = max(dp)

    lis_idx = lis_len
    for seq_idx in range(n - 1, -1, -1):
        if dp[seq_idx] == lis_idx:
            longest_inc_subseq.append(sequence[seq_idx])
            lis_idx -= 1

    # print answer
    print(lis_len)
    print(*reversed(longest_inc_subseq))


if __name__ == '__main__':
    main()
