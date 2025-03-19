# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:23:15 2025

@author: kubap
"""
# COMPARANDO CON VAN DER WAALS

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

temperaturas = ["21", "22_7", "24_6", "26_6", "28_3", "30_1", "32_5", "34_3",
                "35_5", "36_5", "37_5", "38_6", "40_6", "41_6", "42_6", "43_6", "45", "46", "47", "49"]
R = 8.314  # J / mol K
temp_critica = 53.30456282808045
temp_critica_kelvin = 273.15 + temp_critica  # K
pres_critica = 41.16544682268891 * 10**5  # Pa
n = 8 / 6.022 * 10**23  # mol^(-1)

# UNIDADES QUE USAMOS: temp(K), pres(10^5 Pa), volum(cm^3)


def van_de_waals_fit_func(V, T):

    temp_kelvin = T + 273.15
    V_m = V * 10**(-6)

    n_moles = (9.5 * 4*10*(-6)) / (R * temp_kelvin)

    print()
    print(T)
    print(V_m)

    a = (27 * (R**2) * (temp_critica_kelvin**2)) / (64*pres_critica)
    b = (R * temp_critica_kelvin) / (8*pres_critica)

    """
    b_cm = b*10**6
    a_cm = a*10**12
    print("a_cm, b_cm =", a_cm, b_cm)
    """
    #print("a, b =", a, b)

    parte_1 = (R*temp_kelvin)/((V_m/n_moles) - b)
    parte_2 = a/((V_m/n_moles)**2)

    presion = parte_1 - parte_2

    print(presion)

    return presion / (10**5)


def read_data(file_name):
    data = np.genfromtxt(file_name, comments='%',
                         delimiter=';', skip_header=1, filling_values=np.nan)
    return data


def plot(data, temperatura):
    # Datos crudos
    volumen = data[:, 0]
    presion = data[:, 1]

    volumen_new = np.arange(0.2, 4.1, 0.1)

    plt.errorbar(volumen, presion, ecolor="r")
    plt.plot(volumen, presion, 'go')

    presion_van = van_de_waals_fit_func(volumen, float(temperatura))
    plt.plot(volumen, presion_van)

    plt.xlabel(r'Volumen, $cm^3$')
    plt.ylabel(r'Presión, $10^5$ Pa')
    plt.title(r'Variación de presión con volumen con T = ' +
              str(temperatura)+"$\degree$C")

    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    plt.minorticks_on()

    plt.show()
    plt.close()


for i in range(0, 20):
    temp_file_name = "VP_datos_"+(temperaturas[i])+".csv"
    temp_data = read_data(temp_file_name)

    temp_temperatura = temperaturas[i]
    if '_' in temp_temperatura:
        temp_temperatura = temp_temperatura.replace("_", ".")

    temp_plot = plot(temp_data, temp_temperatura)

plt.show()
