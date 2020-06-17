from Ubike2_0_config import *
from Ubilke2_0_func import *
import pandas as pd

# Variable
V = [ [0 for j in range(PillarNum)] for i in range(Period +1)]

# for i in range(len(V)):												# set stop for every period
#     V[i] = [0] * (PillarNum)




# print_min_cost(V)
minimum_cost(Period, CostPerBike, CostPerStop, PillarNum,V)
# print_min_cost(V)
result_possible_value = pd.DataFrame(V, columns = [i for i in range(PillarNum)])
pd.set_option('display.max_columns', result_possible_value.shape[1],'display.max_rows', result_possible_value.shape[0])

print(pd.DataFrame(V))




