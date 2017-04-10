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
import math
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

module_a_intact=np.zeros((nb_marqueurs,nb_iterations-2))
module_v_intact=np.zeros((nb_marqueurs,nb_iterations-1))
module_v=np.zeros((nb_marqueurs,nb_iterations-1))
module_a=np.zeros((nb_marqueurs,nb_iterations-2))


            
for i in range(nb_marqueurs):
    temp=np.transpose(position[i])
    for j in range(3):    
        vitesses[i][j]=np.diff(temp[j])
    module_v_intact[i]=np.sqrt(np.power(vitesses[i][0],2)+np.power(vitesses[i][1],2)+np.power(vitesses[i][2],2))
    module_v[i]=module_v_intact[i]
    n=len(module_v[i])
    for j in range(n-4):
        module_v[i][j+2]=(module_v_intact[i][j]+module_v_intact[i][j+1]+module_v_intact[i][j+2]+module_v_intact[i][j+3]+module_v_intact[i][j+4])/5
    
for i in range(nb_marqueurs):

    module_a_intact[i]=np.diff(module_v[i])
    module_a_intact[i]=abs(module_a_intact[i])
    n=len(module_a_intact[i])
    module_a[i]=module_a_intact[i]
    for j in range(n-6):
        module_a[i][j+3]=(module_a_intact[i][j]+module_a_intact[i][j+1]+module_a_intact[i][j+2]+module_a_intact[i][j+3]+module_a_intact[i][j+4]+module_a_intact[i][j+5]+module_a_intact[i][j+6])/7


def tracer_donnees(liste, indices, titre_a, titre_o):
    fig = plt.figure(1)
    fig.subplots_adjust(hspace=0.4,wspace=0.6)
    n=len(indices)
    x_max=len(liste[0])
    y_min,y_max = minmax(liste)
    y=math.ceil(math.sqrt(n))
    i=0
    for x in indices:
        if y*(y-1)>=n:
            plt.subplot2grid((y-1,y),(i//y,i%y))
        else:
            plt.subplot2grid((y,y),(i//y,i%y))
        plt.plot(liste[x])
        plt.axis([0,x_max,y_min,y_max])
        plt.title("Marqueur "+str(x))
        plt.ylabel(titre_o)
        plt.xlabel(titre_a)
        i+=1
    

def minmax(l1):
    maxi_v=0
    mini_v=0

    for i in range(len(l1)):
        t1=max(l1[i])
        t2=min(l1[i])
        if t1>maxi_v:
            maxi_v=t1
        if t2<mini_v:
            mini_v=t2
            
    return mini_v, maxi_v
        
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
        
    