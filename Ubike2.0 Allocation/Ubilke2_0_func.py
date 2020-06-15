from Ubike2_0_config import *
# from gurobipy import*

def minimum_cost(Period, CostPerBike, CosrPerStop, PillarNum,V):
    for t in range(1, Period + 1): 
        y_max = PillarNum * 2/3
        y_min = PillarNum  * 1/3
        for y in range(int(y_min), int(y_max+1)):
            x_min = y + D[t] - y_max
            x_max = y + D[t] - y_min


            min_cost = 9999999
            opt_x = -1
            for x in range(int(x_min),int( x_max)+1):
                if (x == 0):
                    cost = 0
                else:
                    cost = CostPerBike  * abs(x) + CosrPerStop
                if cost < min_cost: 
                    min_cost = cost
                    opt_x = x

            V[t][y] = min_cost



def print_min_cost(V):
    for t in range(len(V)):
        for y in range(len(V[0])):
            print(V[t][y], end = " ")
        print()
    print()
