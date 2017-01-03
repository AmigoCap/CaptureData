#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:49:33 2016

@author: Emy
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import pandas as pd
import time


fig = plt.figure()
ax = p3.Axes3D(fig)

with open("brasdroit_Cal_11.csv","r",encoding="utf-8") as csvfile:
    "spamreader = csv.reader(csvfile,delimiter=',')"
    L=[list(map(float,row)) for row in csv.reader(csvfile,delimiter=',')]
Lbis = [L[i][2:] for i in range(len(L))]

nb_capt=len(Lbis[0])//3

x=[[] for i in range(nb_capt)]
y=[[] for i in range(nb_capt)]
z=[[] for i in range(nb_capt)]

def animate(i):
	
    for j in range(nb_capt):
        x[j].append(Lbis[i][3*j])
        y[j].append(Lbis[i][3*j+1])
        z[j].append(Lbis[i][3*j+2])

    ax.clear()
    fig.canvas.draw()
     
    for j in range(nb_capt):
        ax.scatter(x[j],y[j],z[j])
         

ani = animation.FuncAnimation(fig, animate, interval=100)

ani.save('tt.mp4',fps=100, writer="ffmpeg")
plt.show()