# B. Дискретное логарифмирование

import math


def find_discrete_logarithm(a, b, n):
    k = math.ceil(math.sqrt(n))

    prev_module = b
    modules = dict()
    for s in range(1, k + 1):
        prev_module = (prev_module * a) % n
        if prev_module not in modules:
            modules[prev_module] = s

    base = pow(a, k, n)
    accumulated_value = 1
    for r in range(1, k + 1):
        accumulated_value = (accumulated_value * base) % n
        if accumulated_value in modules:
            return r * k - modules[accumulated_value]
    return -1


def main():
    a, b, n = map(int, input().split())
    print(find_discrete_logarithm(a, b, n))


if __name__ == "__main__":
    main()
