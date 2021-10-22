#coding:utf-8

def evaluation_KS_individual(size, limit, p_w, individual):
    sum_profit = 0
    sum_weight = 0
    for i in range(size):
        sum_profit = sum_profit + (individual[i] * p_w[1,i])
        sum_weight = sum_weight + (individual[i] * p_w[2,i])
    return sum_profit, sum_weight

def compute_upper_bound(size, limit, p_w, individual, x):
    sum_profit = 0
    sum_weight = 0
    for i in range(size):
        sum_profit = sum_profit + (individual[i] * p_w[1,i])
        sum_weight = sum_weight + (individual[i] * p_w[2,i])

    for i in range(size):
        if i != x and individual[i] == 0:
            individual[i] = 1
            sum_profit = sum_profit + p_w[1,i]
            sum_weight = sum_weight + p_w[2,i]

            if sum_weight > limit:
                #put back the object
                individual[i] = 0
                sum_profit = sum_profit - p_w[1,i]
                sum_weight = sum_weight - p_w[2,i]

    return sum_profit, sum_weight, individual


def compute_cost(profit, weight, size, limit, p_w, individual, x):
    rest = limit - weight
    #return the first object non included
    found = False
    first_obj_not_included = 0
    while not(found) and first_obj_not_included < size:
        if first_obj_not_included != x and individual[first_obj_not_included] == 0:
            found = True
        else:
            first_obj_not_included = first_obj_not_included+1

    if rest <= p_w[2, first_obj_not_included]:
        cost = profit + (p_w[1, first_obj_not_included] / p_w[2, first_obj_not_included]) * rest
    else:
        cost = profit + p_w[1, first_obj_not_included]

    return cost
