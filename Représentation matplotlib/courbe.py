# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:41:38 2016

@author: Quentin
"""


import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import csv
import os

#### Paramétres ####

nom_fichier = 'BrasSimple'
num_iteration = 5

#### Variables ####

position=[]
nb_iterations = 0
nb_marqueurs = 0

#### Script ####


os.chdir("C:/Users/Quentin/Documents/Python/PAr")
print("Lecture csv")

with open(nom_fichier+'.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i=0
    data = list(spamreader)
    nb_iterations = len(data)-5
    for row in data:
        if row!=[] and i>4:
            row = row[2:]
            if i == 5:
                nb_marqueurs = len(row)//3
                position=np.zeros((nb_marqueurs,3,nb_iterations))      
            for j in range(len(row)):
                position[j//3][j%3][i-5]=float(row[j])     
        i+=1  



def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

print("Init")

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
#data = [Gen_RandLine(25, 3) for index in range(50)]
data=position

print("Création lines")
# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

# Setting the axes properties
ax.set_xlim3d([-2000, 2000])
ax.set_xlabel('X')

ax.set_ylim3d([-2000, 2000])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 2000])
ax.set_zlabel('Z')

ax.set_title('Motion capture')

print("Anim")

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, nb_iterations, fargs=(data, lines),
                                   interval=10, blit=True)
                                   
FFMpegWriter = animation.writers['ffmpeg'] 
line_ani.save('animation_bas.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()