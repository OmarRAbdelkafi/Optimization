#coding:utf-8

import numpy as np

import KS_0_1.read_data as RD
from KS_0_1.evaluation import *
from KS_0_1.BandB import *
import KS_0_1.EDA as EDA


"""
1. Problem description :
- The 0/1 knapsack problem is a problem in combinatorial optimization, Given a set of items, each with a weight and a value, determine
the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value
is as large as possible.
"""

"""
Input data :
- list of profit
- list of weight
- size of the Knapsack
"""

"""
Read data
"""
size, p_w, limit = RD.data_KS()
p_w = RD.sort_by_ratio(p_w)
#print(p_w)

"""
Objectif function : maximizing the sum of profit without breaking the limit of the knapsack.
"""
#Greedy solution
Greedy_sol = np.zeros(size)
for i in range(size):
    Greedy_sol[i] = 1
    profit, weight = evaluation_KS_individual(size, limit, p_w, Greedy_sol)
    if weight > limit:
        Greedy_sol[i] = 0 #put back the object

"""
EDA (Exploratory Data Analysis)
"""
#EDA.form_analysis(size, limit, p_w, Greedy_sol)
#EDA.content_analysis(size, limit, p_w)

"""
Solve with exact method :
"""
Branch_and_Bound(size, limit, p_w, Greedy_sol)
