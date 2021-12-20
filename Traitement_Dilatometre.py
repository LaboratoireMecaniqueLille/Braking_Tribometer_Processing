# -*- coding: utf-8 -*-

"""
Created on Thu Jul 22 14:36:51 2021

@author: mbriatte
"""


import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math
import pandas as pd


# Read data from file


directory = r'C:\Users\mbriatte\Desktop\02 - Modelisation_et_' \
            r'caracterisations\Dilatation thermique/'
fichier = 'MA4_L1440_D525.txt'

df = pd.read_csv(directory + fichier,
                 sep=';',
                 skiprows=range(26),
                 skipfooter=1)
df2 = pd.read_csv(directory + fichier,
                  sep=';',
                  skiprows=range(1),
                  skipfooter=len(df)+5)


# Récupération de la longueur initiale
longueur_ini = df2['NETZSCH5                              '][13]
long_ini = ''

for i in longueur_ini:
    if i != ' ':
        long_ini = long_ini + i
longueur_ini = float(long_ini)

# Extraction des données

df.rename(columns={'##Temp./øC': 'Temperature', 'Time/min': 'Temps (min)',
                   'dL/um': 'dL (um)'}, inplace=True)

font = {'family': 'normal', 'weight': 'regular', 'size': 22}
matplotlib.rc('font', **font)

coef = 10 ** (round(math.log10(max(df['Temperature']) / max(df['dL (um)']))))

df['DT'] = 0
df['Dl'] = 0

for i in range(1, len(df)):
    df.loc[i, 'DT'] = df['Temperature'][i] - df['Temperature'][i-1]
    df.loc[i, 'Dl'] = df['dL (um)'][i] - df['dL (um)'][i-1]

df['Derive'] = df['Dl']/df['DT']/longueur_ini

df['DeriveeCorrigee'] = 0

for i in range(1, len(df)):
    df.loc[i, 'DeriveeCorrigee'] = np.percentile(df['Derive'][i:i+50], 50)

# /!\ Changement d'indice en raison d'une suppression de ligne ''NaN''
df.dropna(inplace=True)
df.reset_index(inplace=True)

# Afficher l'évolution de la température et de la longueur
fig, ax = plt.subplots(figsize=(20, 14))
ax2 = ax.twinx()
ax.plot(df['Temps (min)'], df['Temperature'])
ax2.plot(df['Temps (min)'], df['dL (um)'], color='orange')
ax.grid()
ax.set_xlabel('Temps (min)')
ax.set_ylabel('Température (°C)')
ax2.set_ylabel('dL (um)')
ax.set_ylim(0, max(df['Temperature']))
ax2.set_ylim(0, max(df['Temperature'])/coef)
plt.title('Evolution de la température et de la variation de longueur '
          'en fonction du temps')
plt.savefig(directory+'Temperature.png')
plt.show()

# Afficher le coefficient de dilatation thermique en fonction de la température
fig = plt.figure(figsize=(20, 14))
plt.plot(df['Temperature'], df['Derive'])
plt.plot(df['Temperature'], df['DeriveeCorrigee'], 'o')
plt.xlabel('Temperature (°C)')
plt.ylabel('Coefficient de dilatation thermique')
plt.xlim(0, 750)
plt.ylim(0, 0.01)
plt.title('Dilatation thermique en fonction de la température')
plt.savefig(directory+'CoefDilatationThermique.png')
plt.show()
