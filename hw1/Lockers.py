lockers = [True for i in range(101)]

bound = 100

for i in range(2, bound + 1):
    for j in range(i, bound + 1, i):
        lockers[j] = not lockers[j]

for i in range(1, bound + 1):
    if lockers[i] == True:
        print(i)