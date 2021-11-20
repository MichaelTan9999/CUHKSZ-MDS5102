from sys import argv
import numpy as np

def matrix(n):
    box = np.arange(start = 1, stop = n ** 2 + 1, dtype = np.int16)
    box.resize(n, n)
    print('The matrix is: ')
    print(box)

    # determinant
    print('\nThe determinant of the matrix is {}.\n'.format(int(np.linalg.det(box))))

    # inverse
    print('The inverse of the matrix is: ')
    print(np.linalg.inv(box))

    # inverse validation
    print('\nCheck the dot product result: ')
    print((box @ np.linalg.inv(box)).astype(int))
    print(np.array_equal((box @ np.linalg.inv(box)).astype(int), np.identity(n, dtype=int)))

    # normalization: min-max normalization
    max_item = np.amax(box)
    min_item = np.amin(box)
    normalized = (box - min_item) / (max_item - min_item)
    print('\nThe normalized matrix is: ')
    print(normalized)


if __name__ == '__main__':
    if len(argv) > 1:
        matrix(int(argv[1]))
    else:
        n = input('Enter a positive integer: ')
        matrix(int(n))