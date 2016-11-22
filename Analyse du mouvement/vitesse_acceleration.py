# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:19:39 2016

@author: Quentin
"""

#### Modules ####

import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import urllib


#### Variables ####

position=[]
nb_iterations = 0
nb_marqueurs = 0

#### Fonctions ####

print("Téléchargement des données")
fullfilename = os.path.join("C:/Downloads/", "temp.csv")
nom_fichier = "temp"
urllib.request.urlretrieve('https://raw.githubusercontent.com/AmigoCap/CaptureData/master/Data/BrasSimple.csv', fullfilename)
os.chdir("C:/Downloads")
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
                position=np.zeros((nb_marqueurs,nb_iterations,3))      
            for j in range(len(row)):
                position[j//3][i-5][j%3]=float(row[j])     
        i+=1        

vitesses=np.zeros((nb_marqueurs,3,nb_iterations-1))
accelerations=np.zeros((nb_marqueurs,3,nb_iterations-2))

"""
for i in range(nb_marqueurs):
    for j in range(nb_iterations):
        for k in range(3):
            if j+1<nb_iterations:
                vitesses[i][j][k]=position[i][j+1][k]-position[i][j][k]
            if j+2<nb_iterations:
                accelerations[i][j+1][k]=position[i][j+2][k]+position[i][j][k]-2*position[i][j][k]"""

module_v2=np.zeros((nb_marqueurs,nb_iterations-1))
module_v=np.zeros((nb_marqueurs,nb_iterations-1))
module_a=np.zeros((nb_marqueurs,nb_iterations-2))
module_a2=np.zeros((nb_marqueurs,nb_iterations-2))

"""
for i in range(nb_marqueurs):
    for j in range(nb_iterations):
        if j+1<nb_iterations:
            module_v[i][j]=math.sqrt(pow(vitesses[i][j][0],2)+pow(vitesses[i][j][1],2)+pow(vitesses[i][j][2],2))
        if j+2<nb_iterations:
            module_a[i][j]=math.sqrt(pow(accelerations[i][j][0],2)+pow(accelerations[i][j][1],2)+pow(accelerations[i][j][2],2))"""
            
for i in range(nb_marqueurs):
    temp=np.transpose(position[i])
    for j in range(3):    
        vitesses[i][j]=np.diff(temp[j])
    module_v2[i]=np.sqrt(np.power(vitesses[i][0],2)+np.power(vitesses[i][1],2)+np.power(vitesses[i][2],2))
    module_v[i]=module_v2[i]
    n=len(module_v[i])
    for j in range(n-5):
        module_v[i][j+3]=(module_v2[i][j]+module_v2[i][j+1]+module_v2[i][j+2]+module_v2[i][j+3]+module_v2[i][j+4])/5
    
for i in range(nb_marqueurs):

    module_a2[i]=np.diff(module_v[i])
    module_a2[i]=abs(module_a2[i])
    n=len(module_a2[i])
    module_a[i]=module_a2[i]
    for j in range(n-7):
        module_a[i][j+4]=(module_a2[i][j]+module_a2[i][j+1]+module_a2[i][j+2]+module_a2[i][j+3]+module_a2[i][j+4]+module_a2[i][j+5]+module_a2[i][j+6])/7

    
plt.plot(module_a[1])
#plt.plot(module_a2[1])
    


maxi_v=0
mini_v=0

for i in range(len(module_v)):
    t1=max(module_v[i])
    t2=min(module_v[i])
    if t1>maxi_v:
        maxi_v=t1
    if t2<mini_v:
        mini_v=t2


maxi_a=0
mini_a=0

for i in range(len(module_a)):
    t1=max(module_a[i])
    t2=min(module_a[i])
    if t1>maxi_a:
        maxi_a=t1
    if t2<mini_a:
        mini_a=t2
        
def couleurRBG(y,mini,maxi):
    x = (1020/(maxi-mini))*y
    if x>=0 and x < 255:
        b=255
        g=x
        r=0
    elif x>=255 and x<510:
        b=510-x
        g=255
        r=0
    elif x>=510 and x<765:
        b=0
        g=255
        r=x-510
    elif x>=765 and x<=1020:
        b=0
        g=1020-x
        r=255
    
    return r,g,b
        
    