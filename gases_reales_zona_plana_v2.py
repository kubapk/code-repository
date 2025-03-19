# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 18:10:09 2025

@author: kubap
"""

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np


def read_data(file_name):
    data = np.genfromtxt(file_name, comments='%',
                         delimiter=';', skip_header=1, filling_values=np.nan)
    return data


def quadratic_fit_func(x, a, b, c):

    return a*(x**2) + b*x + c


def plot_graph(data):
    # Datos crudos
    temperatura = data[:, 0]
    anchura = data[:, 1]
    x_new = np.array(range(10, 60, 2))

    # Interseccion
    x_new_longitud = len(x_new)
    y_interseccion_datos = [0] * int(x_new_longitud)

    plt.plot(temperatura, anchura, 'go')

    # Ajuste de función
    popt, pcov = curve_fit(quadratic_fit_func, temperatura, anchura)
    a, b, c = popt

    plt.plot(x_new, quadratic_fit_func(x_new, a, b, c),
             'r-', label='Curva ajustada')
    plt.plot(x_new, y_interseccion_datos, label="Anchura = 0")

    plt.xlabel(r'Temperatura, $\degree C$')
    plt.ylabel(r'Anchura de la zona plana, $cm^3$')
    plt.title(r'Variación de la anchura de la zona plana con la temperatura')

    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    plt.minorticks_on()

    plt.annotate("Punto crítico", xy=(53.3, 0),
                 xytext=(55, 0.15), arrowprops={})

    plt.legend()
    plt.show()
    plt.close()

    return


def find_critical_temperature(data):
    temperatura = data[:, 0]
    anchura = data[:, 1]

    # finding variables of quadratic function
    popt, pcov = curve_fit(quadratic_fit_func, temperatura, anchura)
    a, b, c = popt

    solucion_1 = (-b + np.sqrt(b**2 - (4*a*c))) / (2*a)
    solucion_2 = (-b - np.sqrt(b**2 - (4*a*c))) / (2*a)

    solucion = 0
    if solucion_1 > solucion_2:
        solucion = solucion_1
    else:
        solucion = solucion_2

    return solucion
    #anchura_nueva = quadratic_fit_func(temperatura_nueva, a, b, c)


data = read_data("zona_plana_datos.csv")

plot_graph(data)

temperatura_crit = find_critical_temperature(data)
print("Temperatura crítica = ", temperatura_crit)
