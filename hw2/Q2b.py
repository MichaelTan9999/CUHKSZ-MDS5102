import numpy as np

def moving_average(arr, n) -> np.ndarray:
    i = 0
    averaged = []
    while i + n <= len(arr):
        averaged.append(sum(arr[i:i+n]) / n)
        i += 1
    return np.array(averaged)

print(moving_average(np.arange(15), 3))
print(moving_average(np.arange(15), 6))