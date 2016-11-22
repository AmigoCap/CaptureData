# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:19:39 2016

@author: Quentin
"""

#### Modules ####

import csv
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import os
import urllib


"""
Commentaire :

Seulement deux points sont représentés
"""

plotly.tools.set_credentials_file(username='Pepin', api_key='du5oc204lv')


#### Paramétres ####

num_iteration = 5

#### Variables ####

position=[]
nb_iterations = 0
nb_marqueurs = 0

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
                position=np.zeros((nb_marqueurs,nb_iterations,3))      
            for j in range(len(row)):
                position[j//3][i-5][j%3]=float(row[j])     
        i+=1  

token_1 = "7n6qfb5jg9"   # I'm getting my stream tokens from the end to ensure I'm not reusing tokens
token_2 = "68nbcbkovy"

stream_id1 = dict(token=token_1, maxpoints=300)
stream_id2 = dict(token=token_2, maxpoints=300)


trace1 = go.Scatter3d(
    x=[],
    y=[],
    z=[],
    mode='markers',
    stream=stream_id1,
    marker=dict(
        size=5,
        line=dict(
            color='rgba(217, 217, 217, 0.14)',
            width=0.5
        ),
        opacity=0.8
    )
)

trace2 = go.Scatter3d(
    x=[],
    y=[],
    z=[],
    mode='markers',
    stream=stream_id2,
    marker=dict(
        color='rgb(127, 127, 127)',
        size=5,
        symbol='circle',
        line=dict(
            color='rgb(204, 204, 204)',
            width=1
        ),
        opacity=0.9
    )
)
data = [trace1,trace2]
layout = go.Layout(
    xaxis=dict(
        autotick=False,
        ticks='outside',
        tick0=-150,
        dtick=100,
        ticklen=250,
        tickwidth=4,
        tickcolor='#000'
    ),
    yaxis=dict(
        autotick=False,
        ticks='outside',
        tick0=-300,
        dtick=100,
        ticklen=400,
        tickwidth=4,
        tickcolor='#000'
    ),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='multple-trace-axes-streaming')


s_1 = py.Stream(stream_id=token_1)
s_2 = py.Stream(stream_id=token_2)

s_1.open()
s_2.open()

import time

k=10
i=0




while i<nb_iterations:
    print(i)
    x1,y1,z1=position[0][i]
    x2,y2,z2=position[1][i]
    s_data1 = dict(
            type='scatter3d',
            x=x1,
            y=y1,
            z=z1
        )

    s_data2 = dict(
            type='scatter3d',
            x=x2,
            y=y2,
            z=z2
        )
    s_1.write(s_data1, validate=False)
    s_2.write(s_data2, validate=False)
    time.sleep(0.2)
    i += 1
    
s_1.close()
s_2.close()

#tls.embed('streaming-demos','124')


"""
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
    
x2, y2, z2=position[1].transpose()
trace1 = go.Scatter3d(
    x=x2,
    y=y2,
    z=z2,
    mode='markers',
    marker=dict(
        size=5,
        line=dict(
            color='rgba(217, 217, 217, 0.14)',
            width=0.5
        ),
        opacity=0.8
    )
)

x2, y2, z2=position[0].transpose()
trace2 = go.Scatter3d(
    x=x2,
    y=y2,
    z=z2,
    mode='markers',
    marker=dict(
        color='rgb(127, 127, 127)',
        size=5,
        symbol='circle',
        line=dict(
            color='rgb(204, 204, 204)',
            width=1
        ),
        opacity=0.9
    )
)
data = [trace1,trace2]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='test')"""