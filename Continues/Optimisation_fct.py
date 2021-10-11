#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def f2(x):
    '''
    fct qui prend 2 dimension
    '''
    return np.sin(x[0]) + np.cos(x[0]+x[1]) * np.cos(x[0])

def f(x):
    return x**2 + 15*np.sin(x)

def Optim():
    '''
    dans scipy il y a aussi un module qui permet de faire de la programmation linaire,
    le nom du module est linprog qui permet de faire du simplex par exemple
    '''

    #optimisation 1d
    x = np.linspace(-10, 10, 100)
    #plt.plot(x, f(x))
    #plt.show()

    x0 = -5
    Local_min = optimize.minimize(f, x0).x
    print(Local_min)

    #plt.plot(x,f(x),lw=3,zorder=-1) #zorder -1 pour mettre en arriére plan
    #plt.scatter(Local_min, f(Local_min), s=100, c='r', zorder=1)
    #plt.scatter(x0, f(x0), s=200, marker = '+', c='g', zorder=1)
    #plt.show()

    #optimisation 2d
    x = np.linspace(-3, 3, 10)
    y = np.linspace(-3, 3, 10)

    x, y = np.meshgrid(x, y)

    x0 = np.zeros((2,1)) #départ de la recherche avec un poit de coord 0,0
    Local_min = optimize.minimize(f2, x0).x
    print(Local_min)

    plt.contour(x, y, f2(np.array([x, y])), 20)
    plt.scatter(x0[0], x0[1], marker='+', c='r', s=100)
    plt.scatter(Local_min[0], Local_min[1], s=100, c='g')
    plt.show()
