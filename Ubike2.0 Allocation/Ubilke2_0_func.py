from Ubike2_0_config import *
from gurobipy import*

def minimum_cost(Period, StopNum, CostPerBike, CosrPerStop, PillarNum):
    for t in range(1, Period + 1):                                                                                                           # 4 個時間點（先考慮一個站）
        # initiation
        m = Model('FindStop_NeedToAccess')
        # variable
        z  = m.addVars(StopNum, max(PillarNum), name = "z")
         # objective function
        obj  = quicksum(W[i,j] for i in range(len(p)) for j in range(len(t)))

        for s in range(StopNum):
            for x in range(PillarNum[s]):
                if t == 1:


                                                                                                                                                            # yi 為某站的可借車輛數，<= '可停車上限'
            min_qty = max(D[T - t] - y, 0)                                                                                                   # xi upper  <=  '可停車上限' -Yi + Di
            max_qty = total_demand - y + D[T - t]                                                                                      # xi lower >=  '可停車下限' -Yt + Di

            if t == 1:
                min_cost = 9999999 
                opt_x = -1
                for x in range(min_qty, max_demand + 1):                                                                                       # x 去找(lower, upper bound) 裡 cost可以最小的值
                    cost = C[T - t] * x + H * (y + x - D[T - t])                                                                                  # x 迴圈裡決定Z, (要不要到這個站)
                    if cost < min_cost:                                                                                                                     # Z 決定K, （卡車要不要移動）
                        min_cost = cost                                                                                                                    
                        opt_x = x
            else: 
                min_cost = 9999999
                opt_x = -1
                for x in range(min_qty, max_qty + 1):
                    cost = V[t - 1][y + x - D[T - t]] + C[T - t] * x + H * (y + x - D[T - t])
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