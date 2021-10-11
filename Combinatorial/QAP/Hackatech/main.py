#coding:utf-8

import numpy as np

import QAP.read_data as RD
from QAP.evaluation import *
import QAP.EDA as EDA
import QAP.Genetic_Algorithm_pack.Genetic_Algorithm as QAP_GA
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
#arr = np.arange(size)
#np.random.shuffle(arr)

#cost = evaluation_QAP_individual(size,distance,flow,arr)
#print("Random solution cost = ", cost)


"""
EDA (Exploratory Data Analysis)
"""
#EDA.form_analysis(size, distance, flow)
#EDA.content_analysis(size, distance, flow)
#EDA.space_solutions_analysis(size, distance, flow)

QAP_GA.Hybrid_Genetic_Algorithm(size, distance, flow)
