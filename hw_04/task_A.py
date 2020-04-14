# A. Первообразный корень по простому модулю


def find_prime_divisors(n):
    prime_divisors = []
    for i in range(2, n):
        if n % i == 0:
            prime_divisors.append(i)
            while n % i == 0:
                n //= i

        if n == 1:
            break

    return prime_divisors


def find_primitive_root(p):
    prime_divisors = find_prime_divisors(p - 1)
    for root in range(2, p + 1):
        for divisor in prime_divisors:
            degree = (p - 1) // divisor
            if pow(root, degree, p) == 1:
                break
        else:
            return root


def main():
    p = int(input())
    print(find_primitive_root(p))


if __name__ == "__main__":
    main()
