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
import urllib

"""
rajouter nom des marqueurs et tout
mettre le sol enlever axes"""

#### Paramétres ####

num_iteration = 5

#### Variables ####

position=[]
nb_iterations = 0
nb_marqueurs = 0
min_v=0
max_v=0

#### Fonctions ####

class Marqueurs:
    def __init__(self,position,vitesse):
        
        self.position=position #N vecteurs des 3 coordoonées, tableau taille 3*N
        
        self.nb_ite=nb_iterations #N nombre d'itérations
        
        self.couleur=np.zeros((self.nb_ite,3)) #on prévoit un triplet RGB par itération
        self.couleur[0]=couleurRBG(vitesse[0],min_v,max_v)
        for i in range(1,self.nb_ite):
            self.couleur[i]=couleurRBG(vitesse[i-1],min_v,max_v)
            
    def set_couleur(self,mini,maxi):
        self.couleur[0][0],self.couleur[0][1],self.couleur[0][2]=0,0,255
        for i in range(1,self.nb_ite):
            self.couleur[i][0],self.couleur[i][1],self.couleur[i][2]=0,0,255
            """self.couleur[0][0][i],self.couleur[0][1][i],self.couleur[0][2][i]=couleurRGB(self.vitesse[0][i],mini,maxi)
            """
    def get_position(self):
        return self.position
    def get_couleur(self):
        return self.couleur
    def get_vitesse(self):
        return self.vitesse
        
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
    
    return r/255,g/255,b/255
    
def update_lines(num, dataLines, lines):
    i=0
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2,num-1:num])
        line.set_3d_properties(data[2,num-1:num])
        line.set_color((marqueurs[i].get_couleur()[num][0],marqueurs[i].get_couleur()[num][1],marqueurs[i].get_couleur()[num][2]))
        i+=1
    return lines

#### Script ####

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
                position=np.zeros((nb_marqueurs,3,nb_iterations))      
            for j in range(len(row)):
                position[j//3][j%3][i-5]=float(row[j])     
        i+=1  
        


print("Calcul des vitesses et accélerations")   

vitesses=np.zeros((nb_marqueurs,3,nb_iterations-1))
accelerations=np.zeros((nb_marqueurs,3,nb_iterations-2))

module_a_intact=np.zeros((nb_marqueurs,nb_iterations-2))
module_v_intact=np.zeros((nb_marqueurs,nb_iterations-1))
module_v=np.zeros((nb_marqueurs,nb_iterations-1))
module_a=np.zeros((nb_marqueurs,nb_iterations-2))
         
for i in range(nb_marqueurs):
    temp=np.transpose(position[i])
    for j in range(3):    
        vitesses[i][j]=np.diff(position[i][j])
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

print("Initialisation du tracé")

min_v,max_v = minmax(module_v)

marqueurs=[]
for i in range(nb_marqueurs):
    marqueurs.append(Marqueurs(position[i],module_v[i]))

indices=[0,1,2,3,4,5,6]
    
fig = plt.figure()
ax = p3.Axes3D(fig)
    
association = list(range(len(indices)))    
    
 
data=[position[i] for i in indices]
    
print("Tracé")


lines = [ax.plot(position[i][0, 0:1], position[i][1, 0:1], position[i][2, 0:1], marker='o',color=(marqueurs[i].get_couleur()[0][0],marqueurs[i].get_couleur()[1][0],marqueurs[i].get_couleur()[2][0]),markersize=10)[0] for i in indices]


ax.set_xlim3d([-2000, 2000])
ax.set_xlabel('X')
    
ax.set_ylim3d([-2000, 2000])
ax.set_ylabel('Y')
    
ax.set_zlim3d([0.0, 2000])
ax.set_zlabel('Z')

ax.set_title('Motion capture')
    
print("Animation")


line_ani = animation.FuncAnimation(fig, update_lines, nb_iterations, fargs=(data, lines), interval=10, blit=True)
    
plt.show()





