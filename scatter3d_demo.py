import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
xs = []
ys = []
zs = []
with open ("/home/deepak/gac.csv") as file:
	for line in file:
		x,y,z = line.split(",")
		if x == "distance":
			continue
		xs.append(float(x))
		ys.append(float(y))
		zs.append(float(z))

for x,y,z in zip(xs, ys, zs):
    ax.scatter(x, y, z, c = 'y')

xs = []
ys = []
zs = []
with open ("/home/deepak/gacp.csv") as file:
	for line in file:
		x,y,z = line.split(",")
		if x == "distance":
			continue
		xs.append(float(x))
		ys.append(float(y))
		zs.append(float(z))

for x,y,z in zip(xs, ys, zs):
    ax.scatter(x, y, z, c = 'b')

ax.set_xlabel('Distance')
ax.set_ylabel('Time')
ax.set_zlabel('Satisfaction')

plt.show()
