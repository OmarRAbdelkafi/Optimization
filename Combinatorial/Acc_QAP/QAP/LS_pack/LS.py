#coding:utf-8

import copy

import numpy as np
import matplotlib.pyplot as plt # to graphics plot
from random import *

from QAP.evaluation import *

infinie = 99999999999

def LS_best_improvement_permutation(indiv, cost_indiv, distance, flow, mode, size, Total_budget, current_budget):

    iter_budget = current_budget
    best_improvement_cost = infinie
    iteration = 0
    history_search = np.array([cost_indiv])

    stop = False

    while(stop == False and iter_budget <= Total_budget):

        iteration = iteration + 1
        iter_budget = iter_budget + 1

        improvement = copy.copy(indiv)

        for i in range(size):
            for j in range(size):
                tmp = improvement[i]
                improvement[i] = improvement[j]
                improvement[j] = tmp

                if(mode == 'normal'):
                    improvement_cost = evaluation_QAP_individual(size, distance, flow, improvement)
                if(mode == 'jit'):
                    improvement_cost = evaluation_QAP_individual_jit(size, distance, flow, improvement)
                if(mode == 'parallel'):
                    improvement_cost = evaluation_QAP_individual_parallel(size, distance, flow, improvement)

                if improvement_cost < best_improvement_cost:
                    best_improvement_cost = improvement_cost
                    best_impropvement = copy.copy(improvement)

                improvement = copy.copy(indiv)

        if(best_improvement_cost < cost_indiv):
            cost_indiv = best_improvement_cost
            indiv = copy.copy(best_impropvement)
            history_search = np.append(history_search, best_improvement_cost)
        else:
            stop = True

    #plt.plot(history_search)
    #plt.show()
    #print(history_search)
    #print(iteration)

    return indiv, cost_indiv, iteration

def MS_Random_LS(indiv, cost_indiv, distance, flow, budget, mode, size):
    best_cost = infinie
    best_sol = np.zeros(size)
    current_budget = 0
    #history_search = np.array([cost_indiv])

    while(current_budget <= budget):
        LS_solution, LS_cost, sum_iteration = LS_best_improvement_permutation(indiv, cost_indiv, distance, flow, mode, size, budget, current_budget)
        if LS_cost < best_cost:
            best_cost = LS_cost
            best_sol = copy.copy(LS_solution)

        current_budget = current_budget + sum_iteration
        indiv = copy.copy(LS_solution)
        np.random.shuffle(indiv)
        cost_indiv = evaluation_QAP_individual(size, distance, flow, indiv)

    return best_sol, best_cost
