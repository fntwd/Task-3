import copy

# ввод целого числа с проверкой
def input_int(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if value < min_val or value > max_val:
            print("Ошибка: число должно быть от " + str(min_val) + " до " + str(max_val))
            continue
        return value

# ввод вещественного числа с проверкой
def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите вещественное число.")

# ввод матрицы n x n
def input_matrix(n):
    print("Введите матрицу " + str(n) + "x" + str(n) + " построчно:")
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            val = input_float("  a[" + str(i+1) + "][" + str(j+1) + "] = ")
            row.append(val)
        matrix.append(row)
    return matrix

# вывод матрицы
def print_matrix(matrix):
    for row in matrix:
        line = ""
        for val in row:
            line += "{:10.4f}".format(val)
        print(line)
    print()

# нахождение обратной матрицы методом Гаусса
def inverse_matrix(matrix):
    n = len(matrix)

    # строим сдвоенную матрицу [A | E]
    aug = copy.deepcopy(matrix)
    for i in range(n):
        for j in range(n):
            if i == j:
                aug[i].append(1.0)
            else:
                aug[i].append(0.0)

    for col in range(n):
        # ищем ненулевой ведущий элемент
        pivot_row = -1
        for row in range(col, n):
            if abs(aug[row][col]) > 1e-12:
                pivot_row = row
                break
        if pivot_row == -1:
            return None  # матрица вырождена

        # переставляем строки
        if pivot_row != col:
            temp = aug[col]
            aug[col] = aug[pivot_row]
            aug[pivot_row] = temp

        # нормируем ведущую строку
        pivot = aug[col][col]
        for k in range(2 * n):
            aug[col][k] = aug[col][k] / pivot

        # исключаем из остальных строк
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            for k in range(2 * n):
                aug[row][k] = aug[row][k] - factor * aug[col][k]

    # извлекаем правую половину — обратная матрица
    inv = []
    for i in range(n):
        inv.append(aug[i][n:])
    return inv

# перемножение матриц для проверки
def mat_mul(a, b):
    n = len(a)
    result = []
    for i in range(n):
        row = []
        for j in range(n):
            s = 0
            for k in range(n):
                s += a[i][k] * b[k][j]
            row.append(s)
        result.append(row)
    return result

# проверка: A * A^-1 должна быть единичной
def verify(original, inv):
    n = len(original)
    product = mat_mul(original, inv)
    max_err = 0.0
    for i in range(n):
        for j in range(n):
            if i == j:
                err = abs(product[i][j] - 1.0)
            else:
                err = abs(product[i][j])
            if err > max_err:
                max_err = err
    print("Проверка A * A^(-1) = E:")
    print_matrix(product)
    print("Максимальное отклонение от E: " + str(round(max_err, 10)))
    if max_err < 1e-9:
        print("Результат верен.")
    else:
        print("Внимание: большое отклонение.")


def main():
    print("Нахождение обратной матрицы")
    print("=" * 30)

    n = input_int("Введите порядок матрицы (от 1 до 8): ", 1, 8)
    matrix = input_matrix(n)

    print("Введённая матрица A:")
    print_matrix(matrix)

    inv = inverse_matrix(matrix)

    if inv is None:
        print("Обратная матрица не существует.")
        print("Матрица вырождена (определитель равен нулю).")
    else:
        print("Обратная матрица A^(-1):")
        print_matrix(inv)
        verify(matrix, inv)


main()
