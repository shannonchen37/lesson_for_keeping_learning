from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt

fig = plt.figure()
ax = Axes3D(fig)
x = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
y = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
X, Y = np.meshgrid(x, y)  # 网格的创建，这个是关键
Z = 3.226 * Y - (6.452 * (X + 0.125 * Y) * (np.cos(X) - np.cos(2 * X)) ** 2) / np.sqrt(
    0.8 + (X - 0.42) ** 2 + 2 * (X - 7) ** 2
)

plt.xlabel("x")
plt.ylabel("y")
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="rainbow")
plt.show()
