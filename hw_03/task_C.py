# C. Взлом RSA


def gcd(a, b):
    if a == 0:
        return b, 0, 1

    g, x1, y1 = gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def factorization(n):
    for i in range(2, n):
        if n % i == 0:
            return i, n // i


def main():
    n, e, c = (int(input()) for _ in range(3))
    p, q = factorization(n)
    mod = (p - 1) * (q - 1)
    
    _, d, _ = gcd(e, mod)
    d %= mod
    message = pow(c, d, n)
    print(message)


if __name__ == '__main__':
    main()
