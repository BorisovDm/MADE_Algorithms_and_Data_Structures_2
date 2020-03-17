# D. Прямая


def gcd(a, b):
    if a == 0:
        return b, 0, 1

    g, x1, y1 = gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def main():
    a, b, c = map(int, input().split())
    c *= -1

    g, x, y = gcd(abs(a), abs(b))
    if c % g != 0:
        print(-1)
    else:
        x *= c // g
        y *= c // g
        if a < 0:
            x *= -1
        if b < 0:
            y *= -1
        print(x, y)


if __name__ == '__main__':
    main()
