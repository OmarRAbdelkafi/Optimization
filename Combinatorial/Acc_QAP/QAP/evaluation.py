#coding:utf-8
from numba import jit, prange

def evaluation_QAP_individual(size_instance,distance,flow,individual):
    individual_cost = 0
    for i in range(size_instance):
        for j in range(size_instance):
            individual_cost = individual_cost + distance[i , j] * flow[individual[i], individual[j]]
    return individual_cost

@jit(nopython=True)
def evaluation_QAP_individual_jit(size_instance,distance,flow,individual):
    individual_cost = 0
    for i in range(size_instance):
        for j in range(size_instance):
            individual_cost = individual_cost + distance[i , j] * flow[individual[i], individual[j]]
    return individual_cost

@jit(nopython=True, parallel=True)
def evaluation_QAP_individual_parallel(size_instance,distance,flow,individual):
    individual_cost = 0
    for i in prange(size_instance):
        for j in range(size_instance):
            individual_cost = individual_cost + distance[i , j] * flow[individual[i], individual[j]]
    return individual_cost
