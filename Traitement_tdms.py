# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 13:42:45 2021

@author: Mathis Briatte
"""

from nptdms import TdmsFile
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import butter
from scipy import signal
from tqdm import tqdm
from pathlib import Path

directory = r'C:\Users\mbriatte\Desktop\test'
directory2 = 'C:\\Users\mbriatte\Desktop\\test\\'

for fich in os.listdir(directory):
    #if os.path.isfile(directory2 + str(fich)) and fich.endswith(".tdms"):
        tdms_file = TdmsFile(directory2 + str(fich))
        group=tdms_file.groups()[0]
        data = tdms_file.as_dataframe()
        print(data.columns)
        data.columns = ['Fn', 'Ft','Vitesse','Couple','CapaA','CapaB','Top','TriggCamera','Acc']
        Comparaison = ['Fn', 'Ft','Vitesse','Couple','CapaA','CapaB','Top','TriggCamera','Acc']
        facteur = [500,500,413,-50,0.1,0.3,1,1,1]

        print(data)
        #Fréquence d'acquisition
        FREQ = 25000 #A modifier
        Inc = 1/FREQ
        
        ### Select lines

        pas = 1
        
        for column in data.columns :
            i = list(data.columns).index(column)
            data[column]=data[column]*facteur[i]

        ### Create time table

        TIME = np.arange(0 , len(data['Fn']))/FREQ
        
        ### Plot channels

        # Create lowpass filter to calculate the continuous value for each TABL column

        nyquist = FREQ/2
        order = 3
        cutoff = 5
        b, a = butter(order, cutoff/nyquist,'lowpass')

        
        for column in data.columns:
    
            # Calculate continue and variable values for each TABL column
        
            val = data[column]
            val_cont = signal.filtfilt(b, a, val)
            val_var = val-val_cont
        
              
            
            # Plot TABL column data
        
            plt.figure()
        
            plt.plot(TIME,data[column],label=column)
            #plt.plot(TIME, val_var, color='steelblue', label=f'{i}_var', linewidth=0.5)
            #plt.plot(TIME, val_cont ,color='orangered', label=f'{i}_cont', linewidth=0.5)

            plt.title('Diagramme de ' + f'{column}', fontsize=10)            
            plt.xticks(fontsize=7.5)
            plt.yticks(fontsize=7.5)
            plt.xlabel('Temps (s)', fontsize=7.5)
            plt.ylabel(column, fontsize=7.5)
            plt.grid(color='lightgrey')
            plt.legend(loc='upper left', bbox_to_anchor=(0,1), fontsize=7.5)    
            plt.clf
            plt.show()
           
