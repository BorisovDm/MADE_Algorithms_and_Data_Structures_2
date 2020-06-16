# A. Задача для второклассника

import math


def recursive_fft(coeffs):
    n = len(coeffs)
    if n == 1:
        return coeffs

    angle = 2 * math.pi / n
    w_n = math.cos(angle) + 1j * math.sin(angle)
    w = 1

    y_even = recursive_fft(coeffs[0::2])
    y_odd = recursive_fft(coeffs[1::2])
    y = [0] * n

    for k in range(n // 2):
        y[k] = y_even[k] + w * y_odd[k]
        y[k + n // 2] = y_even[k] - w * y_odd[k]
        w *= w_n

    return y


def mul_polynomes(a, b):
    new_size = 2 ** math.ceil(math.log2(len(a) + len(b) - 1))
    a = a + [0] * (new_size - len(a))
    b = b + [0] * (new_size - len(b))

    fft_a = recursive_fft(a)
    fft_b = recursive_fft(b)

    fft_mul_ab = [0] * new_size
    for i in range(new_size):
        fft_mul_ab[-i] = fft_a[i] * fft_b[i]  # 0 n-1 ... 1

    mul_ab = [
        math.floor(x.real / new_size + 0.5)
        for x in recursive_fft(fft_mul_ab)
    ]

    for i in range(new_size - 1):
        mul_ab[i + 1] += mul_ab[i] // 10
        mul_ab[i] = mul_ab[i] % 10

    while mul_ab[-1] == 0 and len(mul_ab) > 1:
        mul_ab.pop()

    mul_ab.reverse()
    return mul_ab


def str_to_polynome(s):
    if s[0] == '-':
        start_idx = 1
        sign = -1
    else:
        start_idx = 0
        sign = 1
    polynome = [int(s[idx]) for idx in range(len(s) - 1, start_idx - 1, -1)]
    return sign, polynome


def main():
    number_1 = input()
    number_2 = input()

    sign_1, polynome_1 = str_to_polynome(number_1)
    sign_2, polynome_2 = str_to_polynome(number_2)

    result = mul_polynomes(polynome_1, polynome_2)
    if sign_1 * sign_2 == -1 and result[0] != 0:
        print('-', end='')
    print(''.join(map(str, result)))


if __name__ == '__main__':
    main()
