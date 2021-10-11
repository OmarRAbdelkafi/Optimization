#coding:utf-8

#from random import *

import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # to graphics plot
import seaborn as sns # a good library to graphic plots

from QAP.evaluation import *
import QAP.LS_pack.LS as QAP_LS

from QAP.Genetic_Algorithm_pack.Mutation import *
from QAP.Genetic_Algorithm_pack.Crossover import *

BKS = 17212548 #Best known solution for els19

def random_init_population(size_instance, size_population):

    pop = np.zeros((size_population, size_instance)).astype(int)

    for p in range(size_population):
        indiv = np.arange(size_instance)
        np.random.shuffle(indiv)
        pop[p] = indiv

    return pop

def Hybrid_Genetic_Algorithm(size_instance, distance, flow):

    #The GA parameters
    size_population = 100;
    Number_of_generation = 100;

    Eval_pop = np.zeros(size_population)

    population = random_init_population(size_instance, size_population)

    for i in range(size_population):
        Eval_pop[i] = evaluation_QAP_individual(size_instance, distance, flow, population[i])

    best_index = Eval_pop.argmin()

    best_individual = population[best_index]
    best_individual_evaluation = Eval_pop[best_index]

    print("Best cost from first population:", best_individual_evaluation)
    print(best_individual)

    history_search = np.array([best_individual_evaluation])

    for g in range(Number_of_generation):

        #selection strategy : random selection
        select1 = randint(0,size_population-1)
        select2 = randint(0,size_population-1)

        #Crossover strategy
        child = OnePointCrossover(population[select1],population[select2], size_instance)

        #Mutation strategy
        Mutation_rate = randint(0,100)
        if Mutation_rate < 10:
            child = Low_Mutation(child, size_instance)

        cost_child = evaluation_QAP_individual(size_instance, distance, flow, child)
        Child_LS_solution, Child_LS_cost = QAP_LS.LS_best_improvement_permutation(child, cost_child, distance, flow)

        #replacement strategy : old individual
        population[size_population-1] = Child_LS_solution
        Eval_pop[size_population-1] = Child_LS_cost

        #New best
        if Child_LS_cost < best_individual_evaluation:
            best_individual = Child_LS_solution
            best_individual_evaluation = Child_LS_cost

        history_search = np.append(history_search, best_individual_evaluation)

    plt.plot(history_search)
    plt.show()

    print("Best cost individual after generations:", best_individual_evaluation)
    print(best_individual)
