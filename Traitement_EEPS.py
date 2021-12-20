# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 13:02:30 2021

@author: mbriatte
"""

# Python 3.8
# Dernière modification : 20/07/21
# coding: utf-8


### Import Libraries
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import seaborn as sns

### Import .csv data in array

directory = r"C:\Users\mbriatte\Desktop\03 - Campagne essai IRE\EEPS\AE3/"
#temp=pd.read_csv(directory + 'test - Copie.csv',delimiter=(';'))
temp=pd.read_csv(directory + 'test.csv', sep=";", usecols=list(range(36)), skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24], skipfooter=24)

temp.rename(columns={'Channel Size [nm]:' : 'Temps', 'Unnamed: 34': 'Temps (s)', 
                           'Unnamed: 35': 'Concentration totale'}, inplace=True)

font={'family' : 'normal', 'weight' : 'regular', 'size' : 22}
matplotlib.rc('font',**font)


#Afficher la concentration totale
fig=plt.figure(figsize=(12,8))
plt.plot(temp['Temps'],temp['Concentration totale'])
plt.xlabel('Temps (s)')
plt.ylabel('Concentration totale (#/cm$^{3}$)')
plt.title('Concentration totale en fonction du temps')
plt.savefig(directory+'Concentration totale.png')
plt.show()

#Afficher la concentration en fonction des channels 
#for column in temp.columns :
    #fig=plt.figure(figsize=(12,8))
    #if column != 'Temps' and column != 'Concentration totale':
    #    plt.plot(temp['Temps'],temp[column],label=column)   
    #    plt.xlabel('Temps (s)')
    #    plt.ylabel('Concentration (#/cm$^{3}$)')
    #    plt.title('Concentration en fonction de leurs tailles et du temps')
    #    plt.legend(loc='upper right')
    #    plt.savefig(directory + f'Repartition_{column}.png')
    #    plt.show()
    

#Afficher le diagramme de répartition des tailles 
#Instant sélectionné :
Instant = temp[['Concentration totale']].idxmax()


fig = plt.figure(figsize=(30,10))
width = 0.5
BarName =temp.columns[1:-3]
x= np.arange(len(BarName))
y=[]
df=temp.iloc[Instant]
y=df.to_numpy()
y=y[0]
y=y[1:-3]
plt.bar(x, y, width, color=(0.65098041296005249, 0.80784314870834351, 0.89019608497619629, 1.0) )
#plt.scatter([i+width/5.0 for i in temp.iloc[0]],temp.loc[Instant],color='k',s=40)
plt.grid()
plt.xticks(x,BarName, rotation=45)
plt.xlabel('Taille équivalente (nm)')
plt.ylabel('Densité (#/cm$^{3}$)')
plt.title('Répartition en taille des particules analysées par le système EEPS')
plt.savefig(directory + f'Repartition en taille.png')
plt.show()

a=0
b=len(temp.iloc[:,1])

font={'family' : 'normal', 'weight' : 'regular', 'size' : 20}
matplotlib.rc('font',**font)

grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
fig, ax = plt.subplots(figsize=(12,20))
sns.heatmap(temp.iloc[a:b,1:32], ax=ax)
ax.set(title = "Evolution de la taille en fonction du temps")
plt.savefig(directory + f'Evolution de la taille en fonction du temps')
