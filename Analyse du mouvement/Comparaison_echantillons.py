# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:00:42 2016

@author: pauline

Analyse de mouvements similaires, vers la reconnaissance de mouvement"""

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
    nb_iterations_base = len(data)-5
    for row in data:
        if row!=[] and i>4:
            row = row[2:]
            if i == 5:
                nb_marqueurs = len(row)//3
                position_base=np.zeros((nb_marqueurs,nb_iterations_base,3))      
            for j in range(len(row)):
                position_base[j//3][i-5][j%3]=float(row[j])     
        i+=1
        

"""reste à importer un deuxième fichier et ses positions position1 à comparer à position base
en attendant : """
nb_marqueurs1=nb_marqueurs
position1=position_base
nb_iterations1=nb_iterations_base

"""on considère que position_base commence à 0,0,0 """
"""remise à origine de l'échantillon 1 à comparer"""

ec_x,ec_y,ec_z=position1[0][0][0],position1[0][1][0],position1[0][2][0]
for i in range (0,nb_iterations1):
    position1[0][i][0]-=ec_x
    position1[0][i][1]-=ec_y
    position1[0][i][2]-=ec_z

"""pour qu'ils aient la même taille, troncature selon la taille du plus petit"""
taille=min(nb_iterations_base,nb_iterations1)
if len(position_base[0][0])<taille:
    for i in range (nb_marqueurs):
        for j in range(3):
            position_base[i][j]=position_base[i][j][0:taille]
else:
    for i in range (nb_marqueurs):
        for j in range(3):
            position1[i][j]=position1[i][j][0:taille]

"""les échantillons font la même taille"""

### Comparaison vitesse et accélérations
"""fonction qui calcule les matrices correspondantes"""
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

def v_et_a(position,nb_marqueurs,nb_iterations):
    vitesses=np.zeros((nb_marqueurs,3,nb_iterations-1))
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
        for j in range(n-5):
            module_v[i][j+3]=(module_v_intact[i][j]+module_v_intact[i][j+1]+module_v_intact[i][j+2]+module_v_intact[i][j+3]+module_v_intact[i][j+4])/5
    for i in range(nb_marqueurs):
        module_a_intact[i]=np.diff(module_v[i])
        module_a_intact[i]=abs(module_a_intact[i])
        n=len(module_a_intact[i])
        module_a[i]=module_a_intact[i]
        for j in range(n-7):
            module_a[i][j+4]=(module_a_intact[i][j]+module_a_intact[i][j+1]+module_a_intact[i][j+2]+module_a_intact[i][j+3]+module_a_intact[i][j+4]+module_a_intact[i][j+5]+module_a_intact[i][j+6])/7
    return module_v,module_a

V_base,A_base=v_et_a(position_base,nb_marqueurs,nb_iterations_base)
V_1,A_1=v_et_a(position1,nb_marqueurs1,nb_iterations1)

def tracer_donnees(liste,indices):
    fig = plt.figure(1)
    fig.subplots_adjust(hspace=0.4,wspace=0.2)
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
        i+=1

def comparer(liste,liste2,indices):
    fig = plt.figure(1)
    fig.subplots_adjust(hspace=0.4,wspace=0.2)
    n=len(indices)
    x_max=len(liste[0])
    y_min1,y_max1 = minmax(liste)
    y_min2,y_max2 = minmax(liste2)
    y_min,y_max=min(y_min1,y_min2),max(y_max1,y_max2)
    y=math.ceil(math.sqrt(n))
    i=0
    for x in indices:
        if y*(y-1)>=n:
            plt.subplot2grid((y-1,y),(i//y,i%y))
        else:
            plt.subplot2grid((y,y),(i//y,i%y))
        p1=plt.plot(liste[x])
        p2=plt.plot(liste2[x])
        plt.legend([p1, p2], ["Mouvement de base", "Mouvement capturé"])
        plt.axis([0,x_max,y_min,y_max])
        plt.title("Marqueur "+str(x))
        i+=1
comparer(A_base,A_1,[0,1,2,3,4,5])

