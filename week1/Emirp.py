from math import sqrt, ceil
from sys import argv

def isPrime(x):
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    else:
        for i in range(3, ceil(sqrt(x + 1)), 2):
            if x % i == 0:
                return False
    return True

def getEmirp(n):
    emirp = []
    count = 0
    current = 3
    while count < n:
        if isPrime(current) and isPrime(int(str(current)[::-1])) and not current == int(str(current)[::-1]):
            emirp.append(current)
            count += 1
        current += 2

    for x in range(len(emirp)):
        print('{:>6}'.format(emirp[x]), end=' ')
        if (x + 1) % 10 == 0:
            print('\n')

if __name__ == '__main__':
    if len(argv) == 2:
        getEmirp(int(argv[1]))
    else:
        n = eval(input('Enter a range N (less than 500): '))
        getEmirp(n)

