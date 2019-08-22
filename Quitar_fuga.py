# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 16:28:52 2019

@author: julio
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.pyplot import plot
import scipy.signal as sg
#from scipy import interpolate
#import pdb

###  Eliminar las fugas de la señal ####

def senal_con_fuga(mes,cliente,circuito):
    
    archivos_circuitos = []
    puertos_circuitos = []
    for key,value in circuito.items():
        findero_circuito = f'DATALOG_{key}_{cliente[3:]}.CSV'
        archivos_circuitos.append(f'D:/01 Findero/{mes}/{cliente}/Datos/{findero_circuito}')
        puertos_circuitos.append([f'L{puerto}' for puerto in value])
    
    df_senales_circuitos = {}
    for i, puertos in enumerate(puertos_circuitos):
        df_senales_circuitos[i] = pd.read_csv(archivos_circuitos[i], usecols=['Datetime','Milis'] + puertos, engine='python')

    senales_circuitos = []
    for dframe in df_senales_circuitos.values():
        for column in dframe.columns:
            if 'Datetime' not in column and 'Milis' not in column:
                senales_circuitos.append(dframe[column].values)     
                
    dic1 = list(circuito.keys())[0]
    senal_circuito = dframe[f'L{circuito[dic1][0]}']
    
    return senal_circuito
    
if __name__ == '__main__':
    mes = '08 Agosto'
    cliente = '12 Suegros Javier'
    circuito = {'F12':[1]}    

    senal_circuito = senal_con_fuga(mes,cliente,circuito)
    
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,4), sharey=True, dpi=120)

    # Sub.Plot
    ax1.plot(senal_circuito[:7000]) 
    ax1.axhline(y=0.0, color='r', linestyle='-')  
    ax1.set_ylim([-1,200])
    
    ax2.plot(senal_circuito[-7000:])  # bluestart
    ax2.axhline(y=0.0, color='r', linestyle='-')
    ax2.set_ylim([-1,200])
    plt.pause(10)
    
    # Title
    ax1.set_title('Primeros 7000'); ax2.set_title('Ultimos 7000')
    
    
    rango1 = int(input('Valor mínimo relativo de la fuga: '))
        
    rango2 = int(input('Valor máximo relativo de la fuga: '))
    # Determina los maximos relativos en el nivel base
    peaks, _ = sg.find_peaks(senal_circuito, height=(rango1, rango2))
    
    Fuga = np.round(np.mean(senal_circuito[peaks]),0)

#
#plt.plot(senal_circuito)
#plt.plot(peaks, senal_circuito[peaks], "x")