#coding:utf-8

import numpy as np

def size_data_QAP():
    fic = open("QAP/data/kra32.dat","r")

    size = int(fic.readline())

    fic.close()

    return size


def distance_data_QAP():
    fic = open("QAP/data/kra32.dat","r")

    size = int(fic.readline())
    line_empty = fic.readline()

    all_f = fic.read().split()

    distance = [[0] * size,] #init
    for i in range(size-1):
        distance.append([0] * size)

    k = 0
    for i in range(size):
        for j in range(size):
            distance[i][j] = int(all_f[k])
            k = k+1

    distance = np.asarray(distance)

    fic.close()

    return distance



def flow_data_QAP():
    fic = open("QAP/data/kra32.dat","r")

    size = int(fic.readline())
    line_empty = fic.readline()

    all_f = fic.read().split()

    flow = [[0] * size,] #init
    for i in range(size-1):
        flow.append([0] * size)

    k = (size * size)
    for i in range(size):
        for j in range(size):
            flow[i][j] = int(all_f[k])
            k = k+1

    flow = np.asarray(flow)

    fic.close()

    return flow
