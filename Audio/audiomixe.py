# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:18:28 2017

@author: Quentin
"""

#### Modules ####

import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import urllib
from pydub import AudioSegment
import random as rd

#### Paramètres ####

frequence = 100
bpm = 110
tempsmesure=4

#### Variables ####

position=[]
nb_iterations = 0
nb_marqueurs = 0

seconde = 1000
battement = (1/(bpm/60))*1000

#### Données audio ####

nb_audio = 8
nb_instrument = 3

audio = [0]*nb_audio
intensite = [0]*nb_instrument
instrument = [0]*nb_instrument
intro = [0]*nb_instrument
solo = [0]*nb_instrument
zindex = [0]*nb_instrument

audio[7] = AudioSegment.from_wav("solo2.wav")
audio[6] = AudioSegment.from_wav("solo1.wav")
audio[5] = AudioSegment.from_wav("bass3.wav")
audio[4] = AudioSegment.from_wav("guitar4.wav")
audio[3] = AudioSegment.from_wav("guitar2.wav")
audio[2] = AudioSegment.from_wav("batterie.wav")
audio[1] = AudioSegment.from_wav("bass.wav")
audio[0] = AudioSegment.from_wav("funk.wav")


instrument[0]=[(audio[0],0), (audio[3],3)]
intensite[0]=[20, 20]
intro[0]=[0, 0]
solo[0]=[0, 0]

instrument[1]=[(audio[1],1)]
intensite[1]=[30]
intro[1]=[0]
solo[1]=[0]

instrument[2]=[(audio[2],2)]
intensite[2]=[35]
intro[2]=[0]
solo[2]=[0]
"""
instrument[3]=[(audio[6],6), (audio[7],7)]
intensite[3]=[60, 60]
intro[3]=[0, 0]
solo[3]=[1, 1]"""

zindex = [0, 20, 20, 50]

occurence = [0]*nb_instrument
for i in range(nb_instrument):
    occurence[i]=[0]*len(instrument[i])

#### Fonctions ####

print("Téléchargement des données")
fullfilename = os.path.join("C:/Downloads/", "temp.csv")
nom_fichier = "temp"
urllib.request.urlretrieve('https://raw.githubusercontent.com/AmigoCap/CaptureData/master/Data/pauline1.csv', fullfilename)
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
                try:
                    position[j//3][j%3][i-5]=float(row[j])
                except:
                    print(row[j])
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

def tracer_donnees(liste, indices, titre_a, titre_o):
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

#### Analyse ####

#On va analyser la vitesse du morceau

v_musique =np.zeros(nb_iterations-1)
v_musique_discret =np.zeros(nb_iterations-1)
v_list = []
minv=0
maxv=0

#On moyenne la vitesse de chaque marquer => vitesse globale

for i in range(nb_marqueurs):
    v_musique = v_musique + module_v[i]
    
v_musique = v_musique / nb_marqueurs
v_musique[nb_iterations-2]=0 #correction

plt.plot(v_musique)

#On analyse les différents fichiers audio pour trouver la division adhéquate

temps=[0]*nb_audio
battement=[0]*nb_audio
mesure=[0]*nb_audio

for i in range(nb_audio):
    temps[i]=len(audio[i])/seconde
    battement[i]=temps[i]*bpm/(60)
    mesure[i]=battement[i]/tempsmesure

divbatt = min(mesure)*tempsmesure


#On calcul les caractéristiques de l'acquisitions pour le tempo donné

t=nb_iterations/frequence
b=t*bpm/(60)
m=b/tempsmesure
print('#### Analyse du fichier audio ####')
print("L'acquisition dure : " + str(t) + " s.")
print("Cela correspond à :")
print("Nombre battement : " + str(b))
print("Nombre de mesures : " +str(m))
div=b/divbatt
print("Divisé en " + str(div) + " parties avec " + str(min(mesure)) + " mesures par parties")
fd = math.ceil(nb_iterations/(b/divbatt))
print("Frame par division : "+ str(fd))
print(" ")

estSolo = [0]*math.ceil(div)

for i in range(math.ceil(div)):
    t1=math.ceil(nb_iterations/(b/divbatt)*i)
    t2=math.ceil(nb_iterations/(b/divbatt)*(i+1))
    somme=np.sum(v_musique[t1:t2])
    somme=somme/(t2-t1)
    v_musique_discret[t1:t2] = somme
    v_list.append(somme)
    if i==0:
        minv = somme
        maxv = somme
    else:
        if somme < minv:
            minv=somme
        else:
            if somme > maxv:
                maxv = somme
                
moyv=np.sum(v_musique)/nb_iterations

v_musique_discret = v_musique_discret/max(v_musique_discret)*100

plt.plot(v_musique_discret)

piste=[0]*nb_instrument
for i in range(nb_instrument):
    piste[i] = AudioSegment.silent(duration=0)
    
def choixaudio(i,vm,t_temp_p):
    l = [0]
    diff=abs(vm-intensite[i][0])
    for a in range(1,len(instrument[i])):
        if intro[i][a]==1:        
            if t_temp_p <20 or t_temp_p >80:
                if abs(vm-intensite[i][a])/2<diff:
                    l=[a]
                    diff=abs(vm-intensite[i][a])/2
                elif abs(vm-intensite[i][a])/2==diff:
                    l.append(a)
        elif solo[i][a]==1:
            if not(estSolo[math.floor(div*t_temp_p/100)]==1):
                if abs(vm-intensite[i][a])<diff:
                    l=[a]
                    diff=abs(vm-intensite[i][a])
                elif abs(vm-intensite[i][a])==diff:
                    l.append(a)
        else:
            if abs(vm-intensite[i][a])<diff:
                l=[a]
                diff=abs(vm-intensite[i][a])
            elif abs(vm-intensite[i][a])==diff:
                l.append(a)
            #yy=abs(vm-intensite[i][a])
            #print(yy)
    x = choix_poids(l,occurence[i])
    if solo[i][x]==1:
        l_t = estSolo[math.floor(div*t_temp_p/100):math.floor(div*(t_temp_p+(temps[instrument[i][x][1]]/t*100))/100)]
        l_t = [1] * len(l_t)
    #if instrument[i][x][1] == 5:
     #   print(t_temp_p, vm)
    occurence[i][x]+=1
    return x
    
def choix_poids(l,occ):
    maxi = max(occ)
    l2=[]
    for x in l:
        for i in range(maxi-occ[x]+1):
            l2.append(x)
    #print(l2)
    return rd.choice(l2)

for i in range(nb_instrument):
    print("instrument = " + str(i))
    t_temp = 0
    t_temp_p = 0
    while t_temp_p < 100:
        if zindex[i]>v_musique_discret[t_temp*frequence]:
            #print(zindex[i],t_temp, t_temp_p,v_musique_discret[t_temp*frequence])
            piste[i] += AudioSegment.silent(duration=fd/frequence*seconde)
            t_temp += fd/frequence
            t_temp_p = t_temp / t *100
            print("silence")
        else:
            choix = choixaudio(i,v_musique_discret[t_temp*frequence], t_temp_p)
            choix_global = instrument[i][choix][1]
            piste[i] += instrument[i][choix][0]
            #print("temps choix : " + str(temps[choix_global]))
            t_temp += temps[choix_global]
            t_temp_p = t_temp / t *100
            print("audio " + str(choix_global))
        #print(str(t_temp_p) + "    " + str(t_temp))
    #print("temps : "+str(t_temp)+ " "+str(t_temp_p))


combined = piste[0]
for i in range(1,nb_instrument):
    combined = combined.overlay(piste[i])
    
combined = combined[:t*seconde]

t0=len(combined)/seconde
b0=t0*bpm/(60)
m0=b0/tempsmesure

print('#### Analyse du fichier final ####')

for i in range(nb_instrument):
    print("taille : " + str(len(piste[i])/seconde))

print("Taille finale : "+str(t0)+" s.")
print("Nombre battement " + str(b0))
print("Nombre de mesures " +str(m0))

combined.export("final.wav", format='wav')
