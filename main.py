# Вариант 12
# Уплотнить заданную матрицу, удаляя из нее строки и столбцы, заполненные нулями. Найти номер
# первой из строк, содержащих хотя бы один положительный элемент.
def first(matrix):
    def compact_matrix(matrix):
        compacted_matrix = []
        cols_to_delete = []
        rows_to_delete = []
        for i in range(len(matrix)):
            col_all_zero = True
            for j in range(len(matrix[0])):
                if matrix[i][j] != 0:
                    col_all_zero = False
                    break
            if col_all_zero:
                rows_to_delete.append(i)

        for j in range(len(matrix[0])):
            row_all_zero = True
            for i in range(len(matrix)):
                if matrix[i][j] != 0:
                    row_all_zero = False
                    break
            if row_all_zero:
                cols_to_delete.append(j)

        for i in range(len(matrix)):
            if i in rows_to_delete:
                continue

            compacted_row = []

            for j in range(len(matrix[0])):
                if j in cols_to_delete:
                    continue
                compacted_row.append(matrix[i][j])

            compacted_matrix.append(compacted_row)

        return compacted_matrix

    def find_first_positive_row(matrix):
        for i, row in enumerate(matrix):
            if any(elem > 0 for elem in row):
                return i
        return -1
    compacted_matrix = compact_matrix(matrix)
    i = find_first_positive_row(compacted_matrix)

    print("compacted matrix:")
    for row in compacted_matrix:
        print(row)

    if i != -1:
        print("First row with positive number:", compacted_matrix[i])
    else:
        print("Matrix don't have positive numbers")


# Вариант 15
# Дана целочисленная прямоугольная матрица. Определить номер первого из столбцов, содержащих
# хотя бы один нулевой элемент.
# Характеристикой строки целочисленной матрицы назовем сумму ее отрицательных четных
# элементов. Переставляя строки заданной матрицы, располагать их в соответствии с убыванием
# характеристик.
def second(matrix):
    def find_first_column_with_zero(matrix):
        for j in range(len(matrix[0])):
            for i in range(len(matrix)):
                if matrix[i][j] == 0:
                    return j
        return -1

    def row_characteristic(row):
        sum = 0
        for i in range(len(row)):
            if row[i] < 0 and row[i] % 2 == 0:
                sum += row[i]
        return sum

    i = find_first_column_with_zero(matrix)
    if i != -1:
        print("Num of first column with element zero:", i)
    else:
        print("Matrix don't column with element zero")


    sorted_matrix = matrix

    for i in range(len(sorted_matrix)):
        for j in range(len(sorted_matrix) - i - 1):
            char1 = row_characteristic(sorted_matrix[j])
            char2 = row_characteristic(sorted_matrix[j + 1])

            if char1 < char2:
                sorted_matrix[j], sorted_matrix[j + 1] = sorted_matrix[j + 1], sorted_matrix[j]

    print("\nMatrix after sort with characteristic:")
    for row in sorted_matrix:
        print(row)


# Вариант 16
# Упорядочить строки целочисленной прямоугольной матрицы по возрастанию количества
# одинаковых элементов в каждой строке.
# Найти номер первого из столбцов, не содержащих ни одного отрицательного элемента.
def third(matrix):

    def find_first_column_with_positive(matrix):
        for j in range(len(matrix[0])):
            positive = True
            for i in range(len(matrix)):
                if matrix[i][j] < 0:
                    positive = False
                    break
            if positive:
                return j
        return -1

    def find_num_same_el(row):
        num_same_el = 0
        was_already = [False for _ in row]
        for i in range(len(row)):
            if was_already[i]:
                continue
            for j in range(i + 1, len(row)):
                if row[i] == row[j] and not was_already[j]:
                    num_same_el += 1
                    was_already[j] = True
        return num_same_el

    sorted_matrix = matrix

    for i in range(len(sorted_matrix)):
        for j in range(len(sorted_matrix) - i - 1):
            char1 = find_num_same_el(sorted_matrix[j])
            char2 = find_num_same_el(sorted_matrix[j + 1])
            if char1 < char2:
                sorted_matrix[j], sorted_matrix[j + 1] = sorted_matrix[j + 1], sorted_matrix[j]

    print("\nMatrix after sort with same elements:")
    for row in sorted_matrix:
        print(row)

    i = find_first_column_with_positive(matrix)
    if i != -1:
        print("Num of first column with all positive elements:", i)
    else:
        print("Matrix don't column with all positive elements")


matrix = [
    [2, 0, -1, 0],
    [1, 4, -2, 0],
    [0, -2, 0, 0],
    [2, 1, 3, 0]
]
print('matrix before first one : ')
for row in matrix:
    print(row)
print('\n')
first(matrix)
print('\n\n')

matrix = [
    [1, -2, -8, 0],
    [-1, -2, 0, 4],
    [0, 0, 5, -6]
]
print('matrix before second one :')
for row in matrix:
    print(row)
print('\n')
second(matrix)
print('\n\n')

matrix = [
    [1, -2, 8],
    [-1, -1, 0],
    [0, 0, 5]
]
print('matrix before third one : ')
for row in matrix:
    print(row)
print('\n')
third(matrix)