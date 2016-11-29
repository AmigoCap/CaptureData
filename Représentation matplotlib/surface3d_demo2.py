# First import everthing you need
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# Create some random data, I took this piece from here:
# http://matplotlib.org/mpl_examples/mplot3d/scatter3d_demo.py
def randrange(n, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin
n = 1
xx = randrange(n, 23, 32)
yy = randrange(n, 0, 100)
zz = randrange(n, -50, -25)

# Create a figure and a 3D Axes
fig = plt.figure()
ax = Axes3D(fig)

# Create an init function and the animate functions.
# Both are explained in the tutorial. Since we are changing
# the the elevation and azimuth and no objects are really
# changed on the plot we don't have to return anything from
# the init and animate function. (return value is explained
# in the tutorial.

position=np.zeros((1,3,100))
for i in range (1):
    position[i][0]=1
    position[i][1]=1
    position[i][2]=1

data = position
lines = [ax.scatter(np.random.rand(), np.random.rand(), np.random.rand(), marker='o', s=1000, c="goldenrod", alpha=0.6) for dat in data]

def animate(i):
    ax.view_init(elev=10., azim=i)
    
def update_lines(num,data,boules):
    for line,data in zip(boules,data):
        print(num)
        #if num>5:
         #   line.set_3d_properties(1+0.05*num,zdir='z')
    return lines

# Animate
anim = animation.FuncAnimation(fig, update_lines, 100, fargs=(data,lines), interval=2000, blit=True)