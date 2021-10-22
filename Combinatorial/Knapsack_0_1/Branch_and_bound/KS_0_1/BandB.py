#coding:utf-8

import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # to graphics plot
import seaborn as sns # a good library to graphic plots

from KS_0_1.evaluation import *

def Branch_and_Bound(size, limit, p_w, Greedy_sol):
    print("Number of possible nodes = ", np.power(2, size+1) - 1)

    #Transform to minimization Problem
    p_w[1, :] = -p_w[1, :]
    Upper = np.Infinity

    #first node
    num_node = 0
    x = -1 #Variable
    solution = copy.copy(Greedy_sol)
    new_upper, weight_upper, node_solution = compute_upper_bound(size, limit, p_w, solution, x)
    cost = compute_cost(new_upper, weight_upper, size, limit, p_w, node_solution, x)

    if new_upper < Upper:
        Upper = new_upper
    if cost > Upper:
        print("There is problem in the first node")

    Tree = np.array([[Upper, cost, node_solution, num_node],], dtype=object)

    x = 0 #Variable
    for i in range(2): #binary
        solution = copy.copy(node_solution)
        num_node = num_node + 1
        solution[x] = i
        new_upper, weight_upper, upper_solution = compute_upper_bound(size, limit, p_w, solution, x)
        cost = compute_cost(new_upper, weight_upper, size, limit, p_w, upper_solution, x)

        if new_upper < Upper:
            Upper = new_upper

        node = np.array([Upper, cost, upper_solution, num_node], dtype=object)
        Tree = np.append(Tree, [node], axis = 0)

    print(Tree)
