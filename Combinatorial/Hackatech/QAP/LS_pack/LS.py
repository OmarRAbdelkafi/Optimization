#coding:utf-8

import copy

import numpy as np
import matplotlib.pyplot as plt # to graphics plot
from random import *


from QAP.evaluation import *

BKS = 17212548 #Best known solution for els19
infinie = 99999999999

def LS_best_improvement_permutation(indiv, cost_indiv, distance, flow):

    best_improvement_cost = infinie
    iteration = 0
    history_search = np.array([cost_indiv])

    stop = False

    while(stop == False):

        iteration = iteration + 1
        improvement = copy.copy(indiv)

        for i in range(len(indiv)):
            for j in range(len(indiv)):
                tmp = improvement[i]
                improvement[i] = improvement[j]
                improvement[j] = tmp
                improvement_cost = evaluation_QAP_individual(len(indiv), distance, flow, improvement)
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

    return indiv, cost_indiv
