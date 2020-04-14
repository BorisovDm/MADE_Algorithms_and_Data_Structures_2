# C. Корень по модулю

# import functools
import math


MAX_SIZE = 10 ** 9
prime_numbers = [True] * math.ceil(math.sqrt(MAX_SIZE))
for i in range(2, len(prime_numbers)):
    if prime_numbers[i]:
        for j in range(i * 2, len(prime_numbers), i):
            prime_numbers[j] = False

# print(prime_numbers)


# def is_prime(n):
#     for i in range(2, n):
#         if i * i > n:
#             break
#
#         if n % i == 0:
#             return False
#
#     return True


# for i in range(2, len(prime_numbers)):
#     if prime_numbers[i] != is_prime(i):
#         print(i)


# @functools.lru_cache(maxsize=None)
# def find_prime_divisors(n):
#     prime_divisors = []
#     for i in range(2, n):
#         if n % i == 0:
#             prime_divisors.append(i)
#             while n % i == 0:
#                 n //= i
#
#         if n == 1:
#             break
#
#     return prime_divisors


def find_prime_divisors(n):
    prime_divisors = []
    for i in range(2, n):
        # if i * i > n:
        #     break

        if prime_numbers[i]:
            prime_divisors.append(i)

        # if n % i == 0:
        #     prime_divisors.append(i)
        #     while n % i == 0:
        #         n //= i
        #
        # if n == 1:
        #     break

    return prime_divisors


# @functools.lru_cache(maxsize=None)
def find_primitive_root(p):
    prime_divisors = find_prime_divisors(p - 1)
    for root in range(2, p + 1):
        for divisor in prime_divisors:
            degree = (p - 1) // divisor
            if pow(root, degree, p) == 1:
                break
        else:
            return root


# @functools.lru_cache(maxsize=None)
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


# @functools.lru_cache(maxsize=None)
def gcd(a, b):
    if a == 0:
        return b, 0, 1

    g, x1, y1 = gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


# @functools.lru_cache(maxsize=None)
def find_module_root(a, b, n):
    primitive_root = find_primitive_root(n)
    p = find_discrete_logarithm(primitive_root, a, n)

    mod, k, y = gcd(b, n - 1)
    if p % mod != 0:
        return -1

    k = (k * p // mod) % (n - 1)
    answer = pow(primitive_root, k, n)
    return answer


def main():
    n_tests = int(input())
    for _ in range(n_tests):
        a, b, m = map(int, input().split())
        print(find_module_root(a, b, m))


if __name__ == "__main__":
    main()
