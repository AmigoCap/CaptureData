# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:30:29 2016

@author: Pauline
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import csv
import math


class Boules:
    def __init__(self,position):
        self.position=position #N vecteurs des 3 coordoonées, tableau taille 3*N
        self.nb_ite=len(position) #N nombre d'itérations
        self.couleur=np.zeros((self.nb_ite,3)) #on prévoit un triplet RGB par itération
        self.vitesse=np.zeros((1,self.nb_ite)) #une vitesse par itération
        for i in range (1,self.nb_ite): #vitesse initiale nulle on commence à 1
            self.vitesse[0][i]=math.sqrt(pow(position[0][i]-position[0][i-1],2)+pow(position[1][i]-position[1][i-1],2)+pow(position[2][i]-position[2,i-1],2))
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
        
        




#### Paramétres ####

nom_fichier = 'donnees2'
num_iteration = 5

#### Variables ####

position=[]
nb_iterations = 0
nb_marqueurs = 0

#### Script ####

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
                #attention ici position de taille Nmarqueurs*3*Nitérations
                position=np.zeros((nb_marqueurs,3,nb_iterations))      
            for j in range(len(row)):
                position[j//3][j%3][i-5]=float(row[j])     
        i+=1  

particules=[] #on remplit la liste d'objets de la classe boule
for i in range (nb_marqueurs):
    particules.append(Boules(position[i])) 
#calcul mini et maxi d'apres toutes les boules puis ajout des couleurs
"""ajouter calcul mini maxi
for boule in particules:
    boule.set_couleur(self,mini,maxi)"""
    
"""NE FONCTIONNE PAS ENCORE :  """
fig = plt.figure()
ax = p3.Axes3D(fig)

    
def animate(i):
    global ax, fig, particules
    return particules[0].get_position()[i]
    #devrait renvoyer le triplet de coordonnées de la première boule à l'itération i
    """a completer"""

# Setting the axes properties
ax.set_xlim3d([-1000, 1000])
ax.set_xlabel('X')

ax.set_ylim3d([-1000, 1000])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1500])
ax.set_zlabel('Z')

line_ani = animation.FuncAnimation(fig,animate, nb_iterations,
                                   interval=10, blit=True)

plt.show()