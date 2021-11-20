import numpy as np

def matrix_create(n):
    start = n - (n - 1)/2
    mat = np.full((n, n), start)
    i = 1
    while i <= start:
        mat[i : n - i, i : n - i] = start + i
        i += 1
    print(np.asmatrix(mat, dtype=int))

matrix_create(7)