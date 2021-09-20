#coding:utf-8

import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # to graphics plot
import seaborn as sns # a good library to graphic plots

from QAP.evaluation import *
import QAP.LS_pack.LS as QAP_LS

def form_analysis(size, distance, flow):
    print("size of the problem :", size)
    print(type(size))
    print("\n")

    print("Distance :")
    #print(distance)
    print(type(distance))
    print(distance.shape)
    print("\n")

    print("Flow :")
    #print(flow)
    print(type(flow))
    print(flow.shape)
    print("\n")

    from scipy.special import factorial
    print("Number of possible solutions = ", factorial(size))

def content_analysis(size, distance, flow):
    print("\n")

    size_arcs = flow.shape[0]*flow.shape[1]
    print("Number of arcs in the problem :", size_arcs)

    print("\nMin distance = ", np.min(distance))
    print("Max distance = ", np.max(distance))
    print("Mean distance = ", np.mean(distance))
    print("Median distance = ", np.median(distance))
    print("\nMin flow = ", np.min(flow))
    print("Max flow = ", np.max(flow))
    print("Mean flow = ", np.mean(flow))
    print("Median flow = ", np.median(flow))

    x, y = distance.shape

    zero_f = 0
    zero_d = 0
    zero_cross = 0

    for i in range(x):
        for j in range(y):
            if distance[i,j] == 0:
                zero_d = zero_d + 1
            if flow[i,j] == 0:
                zero_f = zero_f + 1
            if flow[i,j] == 0 or distance[i,j] == 0:
                zero_cross = zero_cross + 1

    print("\nsparsity of distance :", (zero_d/size_arcs) * 100 )
    print("sparsity of flow :", (zero_f/size_arcs) * 100 )
    print("sparsity of cross :", (zero_cross/size_arcs) * 100 )

    #sns.heatmap(distance)
    #sns.heatmap(flow)
    #plt.show()

    for i in range(x):
        for j in range(y):
            if flow[i,j] > 80000 and i != j:
                print("Arc flow:", i, " - ", j)

    for i in range(x):
        for j in range(y):
            #if distance[i,j] == np.min(distance[distance!=0]):
            if distance[i,j] < 20 and i != j:
                print("Arc distance:", i, " - ", j)

def space_solutions_analysis(size, distance, flow):
    first_sol = np.arange(size)
    cost = evaluation_QAP_individual(size,distance,flow,first_sol)
    print("simple solution cost = ", cost)

    #try a simple movement or gluton solution
    sol = copy.copy(first_sol)
    tmp = sol[14]
    sol[14] = sol[16]
    sol[16] = tmp

    tmp = sol[15]
    sol[15] = sol[17]
    sol[17] = tmp

    cost = evaluation_QAP_individual(size,distance,flow,sol)
    print("improv solution cost = ", cost)

    #LS improvement
    sol = copy.copy(first_sol)
    cost = evaluation_QAP_individual(size,distance,flow,sol)
    LS_solution, LS_cost = QAP_LS.LS_best_improvement_permutation(sol, cost, distance, flow)
    print("LS---- solution cost = ", LS_cost)
    print(LS_solution)

    #LS pool
    LS_cost_pool = np.array([LS_cost])
    LS_sol_pool = np.array([LS_solution])
    size_pool = 99
    sol = copy.copy(first_sol)
    for i in range(size_pool):
        np.random.shuffle(sol)
        cost = evaluation_QAP_individual(size,distance,flow,sol)
        LS_solution, LS_cost = QAP_LS.LS_best_improvement_permutation(sol, cost, distance, flow)
        LS_cost_pool = np.append(LS_cost_pool, LS_cost)
        LS_sol_pool = np.vstack((LS_sol_pool, LS_solution))

    #print("LSPool solution cost = ", LS_cost_pool.min())
    #print("LSPool solution index cost = ", LS_cost_pool.argmin())
    print(LS_sol_pool[LS_cost_pool.argmin()])

    #plt.bar(np.arange(size_pool+1),LS_cost_pool)
    #plt.show()

    from collections import Counter
    id_facility = np.array([]).astype(int)
    frequency_facility = np.array([]).astype(int)
    for i in range(LS_sol_pool.shape[1]):
        count = Counter(LS_sol_pool[:, i])
        M_frequent_elem = count.most_common(1)
        #print(M_frequent_elem)
        id_facility = np.append(id_facility, M_frequent_elem[0][0]) #the facility
        frequency_facility = np.append(frequency_facility,M_frequent_elem[0][1]) #the frequency

    #print("max frequency = ", frequency_facility.max())
    #print("Location = ", frequency_facility.argmax())
    #print("facility = ", id_facility[frequency_facility.argmax()])

    #df = pd.DataFrame(data=LS_sol_pool, index=np.arange(size_pool+1), columns=np.arange(size))

    #Gloutone construction :
    frequency_facility_copy = copy.copy(frequency_facility)
    glouton_sol = np.full(size,-1)
    tabou = np.zeros(size)
    k = 0
    for i in range(size):
        F = id_facility[frequency_facility_copy.argmax()]
        if tabou[F] == 0:
            glouton_sol[k] = F
            k = k+1
            tabou[F] = 1
        frequency_facility_copy[frequency_facility_copy.argmax()] = 0

    for i in range(size):
        if tabou[i] == 0:
            glouton_sol[k] = i
            k = k+1
            tabou[i] = 1

    cost = evaluation_QAP_individual(size,distance,flow,glouton_sol)
    print("Glouton solution cost = ", cost)
    print(glouton_sol)
