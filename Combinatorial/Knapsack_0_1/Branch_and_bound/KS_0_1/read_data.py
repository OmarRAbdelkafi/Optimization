#coding:utf-8

import numpy as np

def data_KS():
    fic = open("KS_0_1/data/KP_10_1.in","r")

    size = int(fic.readline())
    p_w = np.zeros((4,size,))
    for i in range(size):
        line = fic.readline().split()
        p_w[0,i] = int(line[0]) #index
        p_w[1,i] = int(line[1]) #profit
        p_w[2,i] = int(line[2]) #weight
        p_w[3,i] = p_w[1,i] / p_w[2,i] # ratio profit by weight

    limit = int(fic.readline())

    fic.close()
    return size, p_w, limit

def sort_by_ratio(p_w):
    #sort data with ratio of profit by weight
    p_w[3, :] = -p_w[3, :] #to have a descending sort
    p_w = p_w[:, p_w[3, :].argsort()]
    p_w[3, :] = -p_w[3, :]

    return p_w
