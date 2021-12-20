# Python 3.8
# plot_lj2_data.py
# Dernière modification : 09/07/21
# coding: utf-8


# Import Libraries

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import butter
from scipy import signal
import os


# Import .csv data in array

Titre = 'BE_1'

# directory = r"E:\Campagne_2021_FONTE\LabSpect\Thu_Nov_18_09_31_06/"
directory = r"D:\Mat/"
temp = pd.read_csv(directory + 'lj2.csv')

# sos = signal.butter(order, cutoff/nyquist, fs=25000)
# filtered = signal.sosfilt(sos,temp[" Ftlj(N)"])

# for i in range(len(filtered)):
#     temp[" Ftlj(N)"][i] = filtered[i]

# Création des dossiers
Dossier_CoF = 'PLOT_CoF'
path = os.path.join(directory, Dossier_CoF)
if not os.path.exists(directory + Dossier_CoF):
    os.mkdir(path)
del path

Dossier_Temp = 'PLOT_Temp'
path = os.path.join(directory, Dossier_Temp)
if not os.path.exists(directory + Dossier_Temp):
    os.mkdir(path)
del path

Dossier_Donnees = 'PLOT_Donnees'
path = os.path.join(directory, Dossier_Donnees)
if not os.path.exists(directory + Dossier_Donnees):
    os.mkdir(path)
del path

nyquist = 25000 / 2
order = 3
cutoff = 500
b, a = butter(order, cutoff/nyquist, 'lowpass')

Fn_filtered = signal.filtfilt(b, a, temp[' Fnlj(N)'])
Ft_filtered = signal.filtfilt(b, a, temp[' Ftlj(N)'])
Mu = Ft_filtered/Fn_filtered


# Detection of beginning and end of braking

# Detection on Ft because it is more constant than Fn
# data is an array containing, for each brake, beginning and end time values
# Beginning of braking is detected on rising edge of Ft at 100N
# End of braking is detected on falling edge of Ft at 100N
# Noise is eliminated by dropping brakings of less than 1s from data

Temp_ini = temp[' Tdisque1'][0]

print(temp.columns)
data = pd.DataFrame(columns=['debut', 'fin'])

for i in np.arange(2, len(temp)):
    if temp[" Fnlj(N)"][i - 1] < 200 < temp[" Fnlj(N)"][i]:
        d = {'debut': temp["t(s)"][i], 'fin': 0.0}
        data = data.append(d, ignore_index=True)
    if temp[" Fnlj(N)"][i - 1] > 200 > temp[" Fnlj(N)"][i]:
        data.iloc[-1, 1] = temp["t(s)"][i]
data['duree'] = data['fin'] - data['debut']

data = data[data['duree'] > .0]
data = data.reset_index()

# print(data['duree'])

# Straightening of force curves to eliminate deviation

# correction is an array containing, for each brake, mean values of Fn and Ft,
# before and after braking
# d is a list containing, for a given brake, mean values of Fn and Ft, before
# and after braking
# Mean values are aclculated before braking between -5s and -1s, and after
# braking between 1s and 5s to avoid noise
# This condition is reliable as long as time between brakes exceeds 5 seconds
 
correction = pd.DataFrame(columns=['fn_av', 'ft_av', 'fn_ap', 'ft_ap'])

for i in range(len(data)):

    mask = (temp["t(s)"] > data['debut'][i] - 5) & \
        (temp["t(s)"] < data['debut'][i] - 1)
    df = temp[mask]
    ftmoy_av = df[' Ftlj(N)'].mean()
    fnmoy_av = df[' Fnlj(N)'].mean()

    mask = (temp["t(s)"] < data['fin'][i] + 5) & \
        (temp["t(s)"] > data['fin'][i] + 1)
    df = temp[mask]
    ftmoy_ap = df[' Ftlj(N)'].mean()
    fnmoy_ap = df[' Fnlj(N)'].mean()

    d = {'fn_av': fnmoy_av, 'ft_av': ftmoy_av,
         'fn_ap': fnmoy_ap, 'ft_ap': ftmoy_ap}
    
    correction = correction.append(d, ignore_index=True)

   # For each brake, force curves are straightened by subtracting linear
   # deviations over its duration


for i in range(len(data)):
    plt.figure(7, figsize=(19.2, 10.8))
    mask = (temp["t(s)"] > data['debut'][i]) & (temp["t(s)"] < data['fin'][i])
    df = temp[mask]
    df = df.reset_index()
    df["t(s)"] -= df["t(s)"][0]

    a = (correction['fn_ap'][i] - correction['fn_av'][i]) / data['duree'][i]
    b = correction['fn_av'][i]
    df[' Fnlj(N)'] -= a * df['t(s)'] + b
    a = (correction['ft_ap'][i] - correction['ft_av'][i]) / data['duree'][i]
    b = correction['ft_av'][i]
    df[' Ftlj(N)'] -= a * df['t(s)'] + b

# Calculation of friction coefficient for each brake

    df["µ"] = df[' Ftlj(N)'] / df[' Fnlj(N)']
    
# Plot of µ, Fn and Ft for each brake

    plt.figure(i, figsize=(19.2, 10.8))
    # plt.plot(df["t(s)"], df["µ"])
    plt.plot(df["t(s)"], df["µ"],
             color='rebeccapurple',
             label=f'µ{i+1}')  # darkcyan, tab:blue, rebeccapurple
    # plt.grid()
    plt.ylim(0.35, 0.65)
    # plt.xlim(-0.5, 26.5)
    plt.xticks(fontsize=20, rotation=0)
    plt.yticks(fontsize=20, rotation=0)
    plt.xlabel('Temps de freinage (s)', fontsize=30)
    plt.ylabel('Coefficient de friction', fontsize=30)
    plt.title(Titre + f', Brake {i+1}', fontsize=30)
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1), fontsize=15)
    plt.savefig(directory + f'Plot_CoF/CoF_Ser_{i+1}.png')
    # plt.close()

    df_pad = df.iloc[:, 9:-7]
    # for column in df_pad.columns:
    #     if ((df_pad[column][int(len(df_pad) / 2)] - Temp_ini) < 50) :
    #         df_pad = df_pad.drop(columns=[column])
    df_disque = df.iloc[:, -7:-2]
    # for column in df_disque.columns:
    #     if ((df_disque[column][int(len(df_disque) / 2)] - Temp_ini) < 50) :
    #         df_disque = df_disque.drop(columns=[column])
    df_force = df.iloc[:, 6:9]
    Colors_Patin = ['lightcoral', 'red', 'darkred', 'orange', 'yellow', 'lime',
                    'limegreen', 'darkgreen', 'cyan', 'blue', 'violet',
                    'darkviolet']
    Colors_Disque = ['rosybrown', 'chartreuse', 'lemonchiffon', 'deeppink',
                     'lavender', 'magenta', 'hotpink']

# Plot of temperatures for each brake

    plt.figure(300 + i, figsize=(19.2, 10.8))
    for column in df_pad.columns:
        num = ''
        for k in column:
            if k != 'T':
                num += k
        num_ = int(num)
        plt.plot(df["t(s)"], df_pad[column], Colors_Patin[num_], label=column)
        plt.grid()  
    plt.xlabel('Temps de freinage (s)', fontsize=30)
    plt.ylim(50, 250)
    plt.ylabel('Temperatures patins (°C)', fontsize=30)
    plt.title(Titre + f', Brake {i+1}', fontsize=30)
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
    plt.savefig(directory + f'Plot_Temp/T_Ser_{i+1}.png')
    # plt.close()
    
    plt.figure(400 + i, figsize=(19.2, 10.8))
    for column in df_disque.columns:
        num = ''
        for k in column:
            if k not in 'Tdisque':
                num += k
        num_ = int(num)
        plt.plot(df["t(s)"], df_disque[column], Colors_Disque[num_],
                 label=column)
    plt.xlabel('Temps de freinage (s)', fontsize=30)
    plt.ylim(50, 250)
    plt.ylabel('Temperatures disques (°C)', fontsize=30)
    plt.title(Titre + f', Brake {i+1}', fontsize=30)
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
    plt.savefig(directory + f'Plot_Temp/T_Ser_{i+1}.png')
    # plt.close()
    
    plt.figure(500 + i, figsize=(19.2, 10.8))
    plt.plot(df["t(s)"], df_force[" Ftlj(N)"], label='Ft')
    plt.plot(df["t(s)"], df_force[" Fnlj(N)"], label='Fn')
    plt.ylim(0, 600)
    plt.xlabel('Temps de freinage (s)', fontsize=30)
    plt.ylabel('Forces tangentielles et normales (N)', fontsize=30)
    plt.title(Titre + f', Brake {i+1}', fontsize=30)
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
    plt.savefig(directory + f'Plot_Temp/T_Ser_{i+1}.png')
    # plt.close()

plt.show()


'''
### Plot of temperatures for each brake

    plt.figure(i + 300, figsize=(19.2, 10.8))
    plt.plot(temp["t(s)"], temp[" T1"], 'lightcoral',label='TP1')        #TP1
    plt.plot(temp["t(s)"], temp[" T2"], 'red',label='TP2')               #TP2
    plt.plot(temp["t(s)"], temp[" T3"], 'darkred',label='TP3')           #TP3
    plt.plot(temp["t(s)"], temp[" T4"], 'orange',label='TP4')            #TP4
    plt.plot(temp["t(s)"], temp[" T5"], 'yellow',label='TP5')            #TP5
    plt.plot(temp["t(s)"], temp[" T6"], 'lime',label='TP6')              #TP6
    plt.plot(temp["t(s)"], temp[" T7"], 'limegreen',label='TP7')         #TP7
    plt.plot(temp["t(s)"], temp[" T8"], 'darkgreen',label='TP8')         #TP8
    plt.plot(temp["t(s)"], temp[" T9"], 'cyan',label='TP9')              #TP9
    plt.plot(temp["t(s)"], temp[" T10"], 'blue',label='TP10')            #TP10
    plt.plot(temp["t(s)"], temp[" T11"], 'violet',label='TP11')          #TP11

    plt.plot(df["t(s)"], df[" Tdisque1"], 'lightcoral', label='TD1 (cen)')
    plt.plot(df["t(s)"], df[" Tdisque2"], 'red', label='TD2 (int)')
    plt.plot(df["t(s)"], df[" Tdisque6"], 'darkred', label='TD6 (ext)')

    plt.plot(df["t(s)"], df[" Tdisque3"], 'cyan', label='TD3 (cen)')
    plt.plot(df["t(s)"], df[" Tdisque4"], 'deepskyblue', label='TD4 (cen)')
    plt.plot(df["t(s)"], df[" Tdisque5"], 'blue', label='TD5 (cen)')

    
    plt.grid()
    plt.ylim(0,320)    
    plt.xlim(-0.5, 26.5)    
    plt.xlabel('Braking Time (s)')
    plt.ylabel('Temperatures (°C)')
    plt.title(f'Service, Brake {i+1}')
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1))

    plt.savefig(directory + f'Plot_Temp/T_Ser_{i+1}.png')
    plt.close()

plt.show()



### Plot temperatures of pad and disc #########################################

plt.figure(1)
#plt.plot(temp["t(s)"], temp[" T1"], 'lightcoral', label='TP1')  # TP1
plt.plot(temp["t(s)"], temp[" T2"], 'red', label='TP2')  # TP2
#plt.plot(temp["t(s)"], temp[" T3"], 'darkred', label='TP3')  # TP3
plt.plot(temp["t(s)"], temp[" T4"], 'orange', label='TP4')  # TP4
plt.plot(temp["t(s)"], temp[" T5"], 'yellow', label='TP5')  # TP5
plt.plot(temp["t(s)"], temp[" T6"], 'lime', label='TP6')  # TP6
#plt.plot(temp["t(s)"], temp[" T7"], 'limegreen', label='TP7')  # TP7
plt.plot(temp["t(s)"], temp[" T8"], 'darkgreen', label='TP8')  # TP8
#plt.plot(temp["t(s)"], temp[" T9"], 'cyan', label='TP9')  # TP9
plt.plot(temp["t(s)"], temp[" T10"], 'blue', label='TP10')  # TP10
plt.plot(temp["t(s)"], temp[" T11"], 'violet', label='TP11')  # TP11

plt.legend()
plt.xlabel('temps (s)')
plt.ylabel('Temperature (degC)')
plt.title('Temperatures patin')
plt.show()

plt.figure(2)
plt.plot(temp["t(s)"], temp[" Tdisque1"], 'lightcoral', label='TD1')  # TD1
plt.plot(temp["t(s)"], temp[" Tdisque2"], 'red', label='TD2')  # TD2
plt.plot(temp["t(s)"], temp[" Tdisque6"], 'darkred', label='TD6')  # TD6

plt.plot(temp["t(s)"], temp[" Tdisque3"], 'cyan', label='TD3')  # TD3
plt.plot(temp["t(s)"], temp[" Tdisque4"], 'deepskyblue', label='TD4')  # TD4
plt.plot(temp["t(s)"], temp[" Tdisque5"], 'blue', label='TD5')  # TD5

plt.legend()
plt.xlabel('temps (s)')
plt.ylabel('Temperature (degC)')
plt.title('Temperatures disques')
'''


# Plot forces, friction coefficient and rotation speed ########################
plt.figure(3, figsize=(19.2, 10.8))
plt.plot(temp["t(s)"], temp[" Fnlj(N)"], 'orange', label='Fn(N)')  # Fn(N)
plt.plot(temp["t(s)"], temp[" Ftlj(N)"], 'grey', label='Ft(N)')
plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
plt.xlabel('temps (s)')
plt.ylabel('Force (N)')
plt.title(Titre)
plt.savefig(directory + f'Plot_Donnees/Donnees_3.png')
plt.show()

plt.figure(2, figsize=(19.2, 10.8))
plt.plot(temp["t(s)"], temp[" Ftlj(N)"] / temp[" Fnlj(N)"], 'grey', label='Mu')
plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
plt.ylim(0, 1)
plt.xlim(73, 89)
plt.xlabel('temps (s)')
plt.ylabel('Coefficient de friction')
plt.title(Titre)
plt.savefig(directory + f'Plot_Donnees/Donnees_2.png')
plt.show()

plt.figure(5, figsize=(19.2, 10.8))
plt.plot(temp["t(s)"], Fn_filtered, 'orange', label='Fn_filtered(N)')  # Fn(N)
plt.plot(temp["t(s)"], Ft_filtered, 'grey', label='Ft_filtered(N)')  # Ft(N)
plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
plt.xlabel('temps (s)')
plt.ylabel('Force (N)')
plt.title(Titre)
plt.savefig(directory + f'Plot_Donnees/Donnees_1.png')
plt.show()


# LJ1
# Import .csv data in array
temp = pd.read_csv(directory + 'lj1.csv')
plt.figure(4, figsize=(19.2, 10.8))
plt.plot(temp["t(s)"], temp[" lj1_C(Nm)"], 'orange', label='Couple (Nm)')
plt.plot(temp["t(s)"], temp[" lj1_F(N)"], 'grey', label='Fn(N)')
plt.plot(temp["t(s)"], temp[" lj1_rpm(t/min)"], '-k',
         label='Vitesse de rotation(rpm)')  # N(rpm)

plt.legend(loc="upper left", bbox_to_anchor=(0, 1))
plt.xlabel('temps (s)')
plt.ylabel('Force (N)')
plt.title(Titre)
plt.savefig(directory + f'Donnees_lj1.png')
plt.show()
