#coding:utf-8

import numpy as np
import time

import QAP.read_data as RD
from QAP.evaluation import *
import QAP.LS_pack.LS as QAP_LS

"""
1. Problem description :
- The quadratic assignment problem (QAP) is one of the fundamental combinatorial optimization problems in the branch of optimization or operations research in mathematics.
- The problem models the following real-life problem:
There are a set of n facilities and a set of n locations. For each pair of locations, a distance is specified and for each pair of facilities a weight or flow is specified
(e.g., the amount of supplies transported between the two facilities).
2. Objectif :
The problem is to assign all facilities to different locations with the goal of minimizing the sum of the distances multiplied by the corresponding flows.
3. Constraint :
Each facility is assign to only one location
"""

"""
Input data :
- Matrix of distance
- Matrix of flow
"""

"""
Read data
"""
size = RD.size_data_QAP()
distance = RD.distance_data_QAP()
flow = RD.flow_data_QAP()

"""
Objectif function : minimizing the sum of the distances multiplied by the corresponding flows.
"""
#Random solution
arr = np.arange(size)
np.random.shuffle(arr)

cost = evaluation_QAP_individual(size,distance,flow,arr)
print("Random solution cost = ", cost)
print(arr)

budget = 100

start = time.time()
mode = 'normal'
MS_LS_solution, MS_LS_cost = QAP_LS.MS_Random_LS(arr, cost, distance, flow, budget, mode, size)
print("MS LS solution cost normal = ", MS_LS_cost)
print(MS_LS_solution)
end = time.time()
print("Execution time of the normal mode: ", end - start)

start = time.time()
mode = 'jit'
MS_LS_solution, MS_LS_cost = QAP_LS.MS_Random_LS(arr, cost, distance, flow, budget, mode, size)
print("MS LS solution cost jit = ", MS_LS_cost)
print(MS_LS_solution)
end = time.time()
print("Execution time of the jit mode: ", end - start)

start = time.time()
mode = 'parallel'
MS_LS_solution, MS_LS_cost = QAP_LS.MS_Random_LS(arr, cost, distance, flow, budget, mode, size)
print("MS LS solution cost parallel = ", MS_LS_cost)
print(MS_LS_solution)
end = time.time()
print("Execution time of the parallel mode: ", end - start)
