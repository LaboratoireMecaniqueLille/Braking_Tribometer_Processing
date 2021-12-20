# -*- coding: utf-8 -*-
"""
Derniere modification : 23/07/2021 à 10h07

@author: Mathis Briatte
"""
from scipy.signal import butter, lfilter
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
#import scipy.signal
from scipy import fftpack
from scipy import signal
#import scipy.signal
import scipy.ndimage as ndi
import os
import pandas as pd
import librosa
import librosa.display
import glob
#import math

directory = r"E:\Campagne_2021_FONTE\Acquisition Labjack_SPectrum\FONTE\Mon_Nov_15_09:55:58"
fich = directory + "spectrum.h5"
fich_h5=(fich[0:-3])
print (fich_h5)
MechData = h5py.File(fich_h5+'.h5', 'r')
               
        
        ## Liste des channels utilisés
NAMES = []
for n in range(len(MechData['names'][0:])):
    NAMES.append(MechData['names'][n].decode('ascii'))
RecMechChNam = ["Fn(N)","Ft(N)","speed(rpm)","CapB(mm)","CH1","CH2"] #,"CapA(mm)" , "CapB(mm)"]# ] #"Trig(V)" , "top(V)" , 
        
        # Création de la table de temps
FREQ = MechData['freq']
MechDecim = 1
MechTime = np.arange(0 , MechData['table'].shape[0] , MechDecim)/FREQ.value
DataChan = {}

for ChN in RecMechChNam:
    idx = list(NAMES).index(ChN)
    # On applique les facteurs de correction
    DataChan[ChN] = MechData['table'][:,idx][::MechDecim]*MechData['factor'][idx]
        
del MechData
        
        #signal - valeur continue pour FCT et Fn
GaussFiltSize = 10000
fs=FREQ.value #fs=10000 initialement
nyquist = fs / 2
order=3
cutoff=5
b, a = butter(order, cutoff/nyquist,'lowpass')
        
        
        
        #Capacitif
plt.figure(figsize=(20,10))
CapB=DataChan['CapB(mm)']  
CapB=CapB-np.mean(CapB[200:1000])
plt.plot(MechTime,CapB,label='CapB(mm)')
SigncontCapB= signal.filtfilt(b, a, CapB)
CapB=CapB-SigncontCapB
plt.plot(MechTime,CapB,label='CapB-continue')
plt.plot(MechTime,SigncontCapB,label='SigncontCapB')
plt.legend(loc='upper left',prop = {'size':10})
plt.savefig(fich_h5+'_CAPB'+'.png',dpi=300, bbox_inches='tight',pad_inches=0.1)
       
        
        #Force normale
plt.figure(figsize=(20,10))
Fn=DataChan['Fn(N)']
Fn=Fn-np.mean(Fn[200:1000])
plt.plot(MechTime,Fn,label='Fn')
 #SigncontFCTRECH=ndi.filters.gaussian_filter1d(FCTRECH, GaussFiltSize)
SigncontFn= signal.filtfilt(b, a, Fn)
Fn=Fn-SigncontFn
plt.plot(MechTime,Fn,label='Fn-continue')
plt.plot(MechTime,SigncontFn,label='SigncontFn')
plt.legend(loc='upper left',prop = {'size':10})
plt.savefig(fich_h5+'_Fn'+'.png',dpi=300, bbox_inches='tight',pad_inches=0.1)
plt.clf()
        
        
        #Particules
plt.figure(figsize=(20,10))
CH1=DataChan['CH1']  
plt.plot(MechTime,CH1,label='CH1')        
plt.legend(loc='upper left',prop = {'size':10})
plt.savefig(fich_h5+'_CH1'+'.png',dpi=300, bbox_inches='tight',pad_inches=0.1)
plt.clf()
      
       
  
        #Analyse spectrale
plt.figure(figsize=(20,10))         
sr=1000
n_fft=2**14
d=Fn
D = librosa.amplitude_to_db(np.abs(librosa.stft(d,n_fft=n_fft)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis='s', y_axis='log',hop_length=n_fft/4)
plt.colorbar(format='%+2.0f dB')
#plt.setp(ay1.get_xticklabels(), visible=False)
plt.title('Fn')
plt.savefig(fich_h5+'_TF'+'.png',dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.clf()

font={'family' : 'normal', 'weight' : 'regular', 'size' : 22}
plt.rc('font',**font)

        #Informations globales spectrum
plt.figure(figsize=(10,20))
plt.suptitle('Affichage Spectrum')
plt.subplot(3, 1, 1)
Fn=DataChan['Fn(N)']
Ft=DataChan['Ft(N)']
plt.plot(MechTime,Fn,label='Fn')
plt.plot(MechTime,Ft,label='Ft')
plt.ylabel("Effort (N)")
plt.ylim(0,2000)
plt.xlim(0,)
plt.legend(loc='upper left',prop = {'size': 5})
plt.title('Effort')       
        
plt.subplot(3, 1, 2)
speed=DataChan['speed(rpm)']
plt.plot(MechTime,speed,label='Fn')
plt.ylabel("vitesse rotation (RPM)")
plt.ylim(0,1500)
plt.xlim(0,)
plt.title('vitesse')
        
                      
plt.subplot(3, 1, 3)
CH1=DataChan['CH1']
plt.plot(MechTime,CH1,label='totalconcentration')  
plt.title('Concentration Particules')
plt.xlabel("temps [s]")
        #plt.xlim(200,400)
        #plt.ylim(0,1e6)
plt.ylabel("dN/dlogDp [/cm³]")
plt.savefig(fich_h5+'.png',dpi=300, bbox_inches='tight',
            				pad_inches=0.1)
plt.clf()

