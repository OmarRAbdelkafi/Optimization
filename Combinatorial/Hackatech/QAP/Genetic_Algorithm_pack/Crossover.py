#coding:utf-8

from random import *
import copy
import numpy as np

def OnePointCrossover(indiv_1,indiv_2, size_instance):
    point = randint(0,size_instance-1)

    child = np.full(size_instance, -1)
    selected_index = np.zeros(size_instance)

    for i in range(point+1):
        child[i] = indiv_1[i]
        selected_index[indiv_1[i]] = 1

    for i in range(point+1, size_instance):
        if selected_index[indiv_2[i]] == 0:
            child[i] = indiv_2[i]
            selected_index[indiv_2[i]] = 1

    k = 0
    for i in range(size_instance):
        if child[i] == -1:
            replace = False
            while(not replace):
                if selected_index[k] == 0:
                    replace = True
                    selected_index[k] = 1
                    child[i] = k
                else:
                    k = k+1
    return child
