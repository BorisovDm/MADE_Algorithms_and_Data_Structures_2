# D. Расстояние по Левенштейну


def main():
    word_1, word_2 = input(), input()

    correction_matrix = [[0] * (len(word_2) + 1) for _ in range(len(word_1) + 1)]
    for i in range(len(correction_matrix)):
        correction_matrix[i][0] = i
    for j in range(len(correction_matrix[0])):
        correction_matrix[0][j] = j

    for i in range(1, len(word_1) + 1):
        for j in range(1, len(word_2) + 1):
            correction_matrix[i][j] = min([
                correction_matrix[i - 1][j] + 1,
                correction_matrix[i][j - 1] + 1,
                correction_matrix[i - 1][j - 1] + int(word_1[i - 1] != word_2[j - 1]),
            ])

    print(correction_matrix[-1][-1])


if __name__ == '__main__':
    main()
