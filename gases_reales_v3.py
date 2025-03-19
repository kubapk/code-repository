# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:49:54 2025

@author: kubap
"""

from scipy.optimize import curve_fit
# from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np


temperaturas = ["21", "22_7", "24_6", "26_6", "28_3", "30_1", "32_5", "34_3",
                "35_5", "36_5", "37_5", "38_6", "40_6", "41_6", "42_6", "43_6", "45", "46", "47", "49"]
R = 8.314  # J / mol K


def van_de_waals_fit_func(V, T, a, b):
    parte_1 = (R*T) / (V-b)
    parte_2 = a / V**2

    return parte_1 - parte_2


def cubic_fit_func(x, a, b, c, d):

    return a*x**3 + b*x**2 + c*x + d


def read_data(file_name):
    data = np.genfromtxt(file_name, comments='%',
                         delimiter=';', skip_header=1, filling_values=np.nan)
    return data


def plot(data, temperatura):
    # Datos crudos
    volumen = data[:, 0]
    presion = data[:, 1]

    # Ajuste de función
    # popt, pcov = curve_fit(cubic_fit_func, volumen, presion)
    # print("*******")
    # print(popt)
    # a, b, c, d = popt
    # T = float(temperatura)

    plt.errorbar(volumen, presion, 2.5, ecolor="r", label='Error en presión x 5')
    plt.plot(volumen, presion, 'go')
    
    #plt.plot(volumen, presion, 'r')
    # plt.plot(volumen, cubic_fit_func(
         #volumen, a, b, c, d), 'r-', label='Curva ajustada')

    plt.xlabel(r'Volumen, $cm^3$')
    plt.ylabel(r'Presión, $10^5$ Pa')
    plt.title(r'Variación de presión con volumen con T = ' +
              str(temperatura)+"$\degree$C")
    
    # plt.xticks(np.linspace(0,4,10))
    # plt.yticks((0, 5, 10, 15, 20, 25, 30, 35, 40))
    
    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    plt.minorticks_on() 
    
    plt.legend()
    plt.show()
    plt.close()


for i in range(0, 20):
    temp_file_name = "VP_datos_"+(temperaturas[i])+".csv"
    temp_data = read_data(temp_file_name)

    temp_temperatura = temperaturas[i]
    if '_' in temp_temperatura:
        temp_temperatura = temp_temperatura.replace("_", ".")

    temp_plot = plot(temp_data, temp_temperatura)

    print("")
    print("TEMP", temp_temperatura)
