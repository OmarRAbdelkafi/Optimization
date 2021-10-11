#coding:utf-8

from random import *

def Low_Mutation(child, size_instance):

    point = randint(0,size_instance-1)
    Gen_one = randint(0,point)
    Gen_two = randint(point,size_instance-1)

    tmp = child[Gen_one]
    child[Gen_one] = child[Gen_two]
    child[Gen_two] = tmp

    return child
