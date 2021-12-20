# -*- coding: utf-8 -*-

"""
Created on Tue Jul 20 15:50:29 2021

@author: mbriatte
"""

# Python 3.8
# Dernière modification : 21/07/21
# coding: utf-8


# Import Libraries
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import seaborn as sns

# Import .csv data in array

directory = r"C:\Users\mbriatte\Desktop\03 - Campagne essai IRE\OPS\G36S/"
# temp = pd.read_csv(directory + 'test - Copie.csv',delimiter=(';'))
temp = pd.read_csv(directory + '20210602_G36S_ACIER_OPS_RODCUM_01.csv',
                   sep=";",
                   skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                   skipfooter=1)

temp.rename(columns={'Sample #': 'Temps (s)'}, inplace=True)

font = {'family': 'normal', 'weight': 'regular', 'size': 22}
matplotlib.rc('font', **font)

# Affiche les données de base :
print('Facteur de dilution :', temp['Dilution Factor'][0])
print('Température initiale :', temp['Temp(C)'][0])

# Afficher la concentration totale
plt.figure(figsize=(12, 8))
plt.plot(temp['Temps (s)'], temp['Total Conc. (#/cm³)'])
plt.xlabel('Temps (s)')
plt.ylabel('Concentration totale (#/cm$^{3}$)')
plt.title('Concentration totale en fonction du temps')
plt.savefig(directory+'Concentration totale.png')
plt.show()

# Afficher la concentration totale
plt.figure(figsize=(12, 8))
plt.plot(temp['Temps (s)'], temp['Temp(C)'])
plt.xlabel('Temps (s)')
plt.ylabel('Température (°C)')
plt.title('Température dans l OPS en fonction du temps')
plt.savefig(directory+'Temperature.png')
plt.show()

# Afficher la concentration en fonction des channels
plt.figure(figsize=(20, 14))
for column in temp.columns[17:33]:
    plt.plot(temp['Temps (s)'], temp[column], label=column)
    plt.xlabel('Temps (s)')
    plt.ylabel('Concentration (#/cm$^{3}$)')
    plt.title('Concentration en fonction de leurs tailles et du temps')
    plt.legend(loc='upper right')
plt.savefig(directory + f'Repartition.png')
plt.show()


# Afficher le diagramme de répartition des tailles
# Instant sélectionné (en pratique, choisir un freinage):
Instant = temp[['Total Conc. (#/cm³)']].idxmax()


plt.figure(figsize=(30, 10))
width = 0.5
BarName = temp.columns[17:33]
x = np.arange(len(BarName))
df = temp.iloc[Instant]
y = df.to_numpy()
y = y[0]
y = y[17:33]
plt.bar(x, y, width, color=(0.65098041296005249,
                            0.80784314870834351,
                            0.89019608497619629, 1.0))
# plt.scatter([i + width / 5.0 for i in temp.iloc[0]],
#             temp.loc[Instant], color='k', s=40)
plt.grid()
plt.xticks(x, BarName, rotation=45)
plt.xlabel('Taille équivalente (nm)')
plt.ylabel('Densité (#/cm$^{3}$)')
plt.title('Répartition en taille des particules analysées par le système OPS')
plt.savefig(directory + f'Repartition en taille.png')
plt.show()

a = 0
b = len(temp.iloc[:, 1])

font = {'family': 'normal', 'weight': 'regular', 'size': 20}
matplotlib.rc('font', **font)

grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
fig, ax = plt.subplots(figsize=(12, 20))
sns.heatmap(temp.iloc[a:b, 17:33], ax=ax)
ax.set(title="Evolution de la taille en fonction du temps")
plt.savefig(directory + f'Evolution de la taille en fonction du temps')
