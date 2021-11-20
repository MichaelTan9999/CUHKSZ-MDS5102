import numpy as np
import matplotlib.pyplot as plt
from math import pi, e

N = 200
s = 3
 
x1 = np.linspace(-1, 1, N)
x2 = np.linspace(-1, 1, N)

X1, X2 = np.meshgrid(x1, x2)
Y = 1 / (2 * pi * s ** 2) * e ** (-(X1 ** 2 + X2 ** 2) / 2 * s ** 2)
cm = plt.cm.get_cmap('viridis')
plt.ylim(-1, 1)
plt.xlim(-1, 1)
plt.scatter(X1, X2, c=Y, cmap=cm)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()