#coding:utf-8

import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # to graphics plot
import seaborn as sns # a good library to graphic plots

from KS_0_1.evaluation import *

def form_analysis(size, limit, p_w, Greedy_sol):
    print("size od the problem:", size)

    print("\nind    prof     weig")
    for i in range(size):
        print(p_w[0,i],"  ",p_w[1,i],"   ",p_w[2,i])

    print("\nlimit of the knapsack:", limit)

    print("\nGreedy solution :")
    print(Greedy_sol)
    profit, weight = evaluation_KS_individual(size, limit, p_w, Greedy_sol)
    print("profit = ", profit)
    print("weight = ", weight)

    print("Number of possible solutions without the constraint :", np.power(2, size))

def content_analysis(size, limit, p_w):
    #random generation of 100 random solution:
    space_solutions = np.zeros((100,size))
    profit_solutions = np.zeros((100))
    weight_solutions = np.zeros((100))
    for i in range(100):
        rand_obj = np.random.randint(1, size+1) #random number of selected solution
        for j in range(rand_obj):
            space_solutions[i,j] = 1
        np.random.shuffle(space_solutions[i])
        profit, weight = evaluation_KS_individual(size, limit, p_w, space_solutions[i])
        profit_solutions[i] = profit
        weight_solutions[i] = weight

    print(space_solutions)
    feasible = 0
    best_profit = 0
    best_weight = 0
    best_random_solution = np.zeros((size))
    for i in range(100):
        if weight_solutions[i] <= limit:
            feasible = feasible + 1
            if profit_solutions[i] > best_profit:
                best_profit = profit_solutions[i]
                best_random_solution = space_solutions[i]
                best_weight = weight_solutions[i]

    print("Number of feasible solution = ", feasible)
    print("best profit = ", best_profit)
    print("weight = ", best_weight)
    print(best_random_solution)
