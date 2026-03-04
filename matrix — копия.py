def read_matrix(filename):
    return [list(map(int, line.split())) for line in open(filename)]

def print_matrix(m, name):
    print(f"\n{name}:")
    for row in m:
        print(" ".join(f"{x:6}" for x in row))

def transpose(m):
    return [list(row) for row in zip(*m)]

def get_regions(n):
    a1, a2, a3, a4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1:
                a1.append((i, j))
            elif i < j and i + j > n - 1:
                a2.append((i, j))
            elif i > j and i + j > n - 1:
                a3.append((i, j))
            elif i > j and i + j < n - 1:
                a4.append((i, j))
    return a1, a2, a3, a4

def get_perimeter(indices, n):
    # Вернёт элементы по периметру заданной области
    perim = []
    min_i = min(i for i, _ in indices)
    max_i = max(i for i, _ in indices)
    min_j = min(j for _, j in indices)
    max_j = max(j for _, j in indices)
    for i, j in indices:
        if i == min_i or i == max_i or j == min_j or j == max_j:
            perim.append((i, j))
    return perim

def build_F_modified(A):
    n = len(A)
    F = [row[:] for row in A]  # копия A
    a1, a2, a3, a4 = get_regions(n)

    # Подсчёт количества чётных чисел в нечётных столбцах области 2
    count_even_in_odd_cols_a2 = 0
    for i, j in a2:
        if j % 2 == 1 and F[i][j] % 2 == 0:
            count_even_in_odd_cols_a2 += 1

    # Периметр области 3
    perim_a3 = get_perimeter(a3, n)

    # Произведение чисел по периметру области 3
    product_perim_a3 = 1
    for i, j in perim_a3:
        product_perim_a3 *= F[i][j]

    # Условие для замены
    if count_even_in_odd_cols_a2 > product_perim_a3:
        # Симметричная замена областей 1 и 3
        for (i1, j1), (i3, j3) in zip(sorted(a1), sorted(a3)):
            F[i1][j1], F[i3][j3] = F[i3][j3], F[i1][j1]
    else:
        # Несимметричная замена областей 1 и 2 (область 2 в обратном порядке)
        for (i1, j1), (i2, j2) in zip(sorted(a1), reversed(sorted(a2))):
            F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]

    return F, count_even_in_odd_cols_a2, product_perim_a3

def compute_result(A, F, K):
    n = len(A)
    A_T = transpose(A)
    F_T = transpose(F)

    KA_T = [[K * A_T[i][j] for j in range(n)] for i in range(n)]
    left = [[sum(KA_T[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    right = [[K * F_T[i][j] for j in range(n)] for i in range(n)]
    res = [[left[i][j] - right[i][j] for j in range(n)] for i in range(n)]
    return res

if __name__ == "__main__":
    K = int(input("Введите K: "))
    A = read_matrix("matrix.txt")
    F, count_even_in_odd_cols_a2, product_perim_a3 = build_F_modified(A)
    R = compute_result(A, F, K)

    print_matrix(A, "Исходная матрица A")
    print(f"\nКоличество чётных чисел в нечётных столбцах области 2: {count_even_in_odd_cols_a2}")
    print(f"Произведение чисел по периметру области 3: {product_perim_a3}")
    print_matrix(F, "Матрица F после преобразования")
    print_matrix(R, "Результат выражения ((K*A^T)*A) - K*F^T")
