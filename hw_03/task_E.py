# E. Китайская теорема


def gcd(a, b):
    if a == 0:
        return b, 0, 1

    g, x1, y1 = gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def main():
    n_tests = int(input())
    for _ in range(n_tests):
        a, b, n, m = map(int, input().split())

        _, x1, x2 = gcd(m, n)
        x1 %= n
        x2 %= m

        solution = (a * x1 * m + b * x2 * n) % (n * m)
        print(solution)


if __name__ == '__main__':
    main()
