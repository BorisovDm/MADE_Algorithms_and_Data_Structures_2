# B. Дуэль

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

    return mul_ab


def main():
    trees = list(map(int, input()))

    # a[i - k] * a[i + k] -> a[2 * i], symmetry
    convolution = mul_polynomes(trees, trees)
    n_positions = 0
    for i in range(len(trees)):
        n_positions += trees[i] * convolution[2 * i] // 2

    print(n_positions)


if __name__ == '__main__':
    main()
