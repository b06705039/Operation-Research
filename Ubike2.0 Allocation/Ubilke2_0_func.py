from Ubike2_0_config import *
import pandas as pd

# from gurobipy import*

def minimum_cost(Period, CostPerBike, CostPerStop, PillarNum,V):
    logDF = pd.DataFrame(columns = ['t','y','x','x_min','x_max','min_cost','opt_x','cost'])
    for t in range(1, Period + 1): 
        y_max = int(PillarNum * 2/3)
        y_min = int(PillarNum  * 1/3)
        for y in range(y_min, y_max+1):
            x_min = y_min - y + D[Period - t]
            x_max = y_max - y + D[Period - t]


            min_cost = 9999999
            opt_x = -1
            for x in range(x_min,x_max+1):
                if (x == 0):
                    cost = V[Period - t][y + x - D[Period - t]]
                else:
                    cost = CostPerBike  * abs(x) + CostPerStop + V[Period - t][y + x - D[Period - t]]
                if cost < min_cost: 
                    min_cost = cost
                    opt_x = x
                newS = pd.Series({'t':t,
                                            'y' :y,
                                            'D[Period - t]':D[Period - t],
                                           'x' :x,
                                           'x_min':x_min,
                                           'x_max':x_max,
                                           'min_cost' :min_cost,
                                           'opt_x' :opt_x,
                                           'cost' :cost
                                           })
                logDF = logDF.append(newS, ignore_index=True)
            V[t][y] = min_cost
    pd.set_option('display.max_columns', logDF.shape[1],'display.max_rows', logDF.shape[0])
    print(logDF)




def print_min_cost(V):
    for t in range(len(V)):
        for y in range(len(V[0])):
            print(V[t][y], end = " ")
        print()
    print()
