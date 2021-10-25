#coding:utf-8

import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # to graphics plot
import seaborn as sns # a good library to graphic plots

from KS_0_1.evaluation import *

def Branch_and_Bound(size, limit, p_w, Greedy_sol):
    best_solution = copy.copy(Greedy_sol)
    best_profit = 0
    best_weight = 0

    Nodes_explored = 0
    Max_nodes = np.power(2, size+1) - 1
    print("Number of possible nodes = ", Max_nodes)

    #Transform to minimization Problem
    p_w[1, :] = -p_w[1, :]
    Upper = np.Infinity

    ########first node [Greedy solution]
    Explored = False
    num_node = 0
    x = -1 #Variable

    solution = copy.copy(Greedy_sol)
    new_upper, weight_upper, node_solution, Feasible = compute_upper_bound(size, limit, p_w, solution, x)
    cost = compute_cost(new_upper, weight_upper, size, limit, p_w, node_solution, x)

    if new_upper < Upper:
        Upper = new_upper
        best_profit = new_upper
        best_weight = weight_upper

    if cost > Upper:
        print("There is problem in the first node")

    Tree = np.array([[Upper, cost, node_solution, num_node, x, Explored],], dtype=object)
    stop_exploration = False

    #####The Tree
    while not stop_exploration:
        Nodes_explored = Nodes_explored + 1
        print("\n****NEW STEP****\n")

        #search Less cost node (take the last node) LIFO if equal less cost node not explored yet
        print("Tree before:\n", Tree)
        LC = np.Infinity
        for i in range(Tree.shape[0]):
            if Tree[i, 5] == False:
                if Tree[i,1] <= LC:
                    LC = Tree[i,1]
                    index_LC_node = i


        #last_min_node = np.where(Tree[:,1] == np.amin(Tree[:,1]))
        #for i in range(len(last_min_node[0])):
        #    if Tree[last_min_node[0][i], 5] == False:
        #        index_LC_node = last_min_node[0][i]
        print("LC node:", index_LC_node)

        x = Tree[index_LC_node, 4] + 1 #Variable
        print("Variable to change:", x)

        if x < size:
            Go_for_it = True
        else:
            Go_for_it = False

        Tree[index_LC_node, 5] = True
        print("Go for it =", Go_for_it)

        if Go_for_it:
            for i in range(2): #binary 0 1
                print("change to = ", i)
                solution = copy.copy(Tree[index_LC_node,2])
                num_node = num_node + 1
                solution[x] = i
                print("Solution to use:", solution)
                new_upper, weight_upper, upper_solution, Feasible = compute_upper_bound(size, limit, p_w, solution, x)
                print("New upper:", new_upper)
                print("New weight_upper", weight_upper)
                print("Feasible = ", Feasible)
                cost = compute_cost(new_upper, weight_upper, size, limit, p_w, upper_solution, x)

                if new_upper < Upper and Feasible:
                    Upper = new_upper
                    best_solution = copy.copy(upper_solution)
                    best_profit = new_upper
                    best_weight = weight_upper

                node = np.array([Upper, cost, upper_solution, num_node, x, False], dtype=object)
                Tree = np.append(Tree, [node], axis = 0)

            #kill the high cost node
            node_to_kill = np.where(Tree[:,1] > Upper)
            print("node to kill with cost more thar upper bound:", node_to_kill[0])
            Tree = np.delete(Tree, node_to_kill[0], axis = 0)
            print("Tree after kill:\n", Tree)

        #All nodes Explored
        stop_exploration = np.all(Tree[:, 5] == Tree[0, 5])
        print("Stop exploration ?",stop_exploration)

    print("Nodes explored = ", Nodes_explored,"/", Max_nodes)

    return best_solution, best_profit, best_weight
