#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def f_nd(arr):
    '''
        5D her in arr from 0 to 4
    '''
    return arr[0] + (16 * arr[1]) - arr[2] + (arr[3] * arr[4])

def f2(x):
    '''
    2D fct, x is an array of 2D
    '''
    return np.sin(x[0]) + np.cos(x[0]+x[1]) * np.cos(x[0])

def f(x):
    return x**2 + 15*np.sin(x)

def Continues_Optimization_1D():

    '''
    ### 1D optimization
    '''

    LandingScape = np.linspace(-10, 10, 100)
    plt.plot(LandingScape, f(LandingScape))
    plt.show()

    x0 = -10
    resume = optimize.minimize(f, x0)
    Local_min = optimize.minimize(f, x0).x #x here give the best value
    print(resume)
    print(Local_min)
    print(f(Local_min))

    plt.plot(LandingScape,f(LandingScape),lw=3,zorder=-1) #zorder -1 pour mettre en arriére plan
    plt.scatter(Local_min, f(Local_min), s=100, c='r', zorder=1)
    plt.scatter(x0, f(x0), s=200, marker = '+', c='g', zorder=1)
    plt.show()

def Continues_Optimization_2D():

    '''
    ### 2D optimization
    '''

    x = np.linspace(-3, 3, 10)
    y = np.linspace(-3, 3, 10)

    x, y = np.meshgrid(x, y)

    x0 = np.zeros((2,1)) #start the researh at the point of coordinate (0,0)
    resume = optimize.minimize(f2, x0)
    Local_min = optimize.minimize(f2, x0).x
    print(resume)
    print(Local_min)
    print(f2(Local_min))

    plt.contour(x, y, f2(np.array([x, y])), 20)
    plt.scatter(x0[0], x0[1], marker='+', c='r', s=100)
    plt.scatter(Local_min[0], Local_min[1], s=100, c='g')
    plt.show()

def Multistart_Local_search():
    #Nb dimensiion
    n = 5
    MultiStart = 10
    best = 1000000

    for i in range(MultiStart):
        #start
        x0 = np.random.randn(n,1)

        #resume = optimize.minimize(f_nd, x0)
        Local_min = optimize.minimize(f_nd, x0).x
        print(f_nd(Local_min))

        if f_nd(Local_min) < best:
            best = f_nd(Local_min)

    print("The best result is:", best)

def main():
    Continues_Optimization_1D()
    #Continues_Optimization_2D()
    #Multistart_Local_search()

if __name__ == '__main__':
    main()
