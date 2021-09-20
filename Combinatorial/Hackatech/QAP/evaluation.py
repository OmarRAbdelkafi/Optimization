#coding:utf-8

def evaluation_QAP_individual(size_instance,distance,flow,individual):
    individual_cost = 0
    for i in range(size_instance):
        for j in range(size_instance):
            individual_cost = individual_cost + distance[i , j] * flow[individual[i], individual[j]]
    return individual_cost
