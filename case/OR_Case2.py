from gurobipy import*
import pandas as pd
from plotnine import *

# initiation
m               = Model('case2')
demandFile      = pd.read_csv("Demand.csv", header=None)
minDemandFile   = pd.read_csv("minRequire.csv", header=None)
shiftTime       = pd.read_csv("shiftTime.csv", header = None)


# parameter
s   = [ i for i in range(14)]                                                                        # shift
t   = [ i for i in range(31)]                                                                        # day
p   = [ i for i in range(24)]                                                                       # period
D   = [ row.tolist() for index, row in demandFile.iterrows() ]                       # demand 
Mt  = minDemandFile.iloc[:,0].tolist()                                                        # requested shift, min demend, day
Ms  = minDemandFile.iloc[:,1].tolist()                                                        # shift
M   = minDemandFile.iloc[:,2].tolist()                                                        # number
T   = [ row.tolist() for index, row in shiftTime.iterrows() ]                           # shift period


# for question 4 different employee
# every row in datafram represent different number of employee, we will get the objective value at the end of the program
emplo_num = pd.DataFrame(columns = ('emploNum' , 's0_equal', 'sNight_max', 'sAfn_max','obj'))
for i in range(35,46):
    diff_emplo = pd.Series({  'emploNum'          :i,
                                        's0_equal'              :int(8*i),
                                        'sNight_max'          :int(31/7*i),
                                        'sAfn_max'             :int(31/7*i)*2,
                                        'obj'                       :0})
    emplo_num = emplo_num.append(diff_emplo,ignore_index=True)


# optimize program with different number of employee
for index,row in emplo_num.iterrows() :
    
    # variable
    X         = m.addVars(len(s), len(t), name = "ActualShift")
    W         = m.addVars(len(p), len(t), name = "ObjectiveFunction")

    m.update()

    # objective function

    obj       = quicksum(W[i,j] for i in range(len(p)) for j in range(len(t)))
    m.setObjective(obj, GRB.MINIMIZE)
    
    # constraint 
    
    for i in range(len(t)):
        m.addConstr(quicksum(X[j,i] for j in range(len(s))) == row['emploNum'])                                             # every day emplo ==40


    for i in range(len(p)):                                                                                                                             # objective function
        for j in range(len(t)):
            m.addConstr(W[i,j] >= D[i][j] - quicksum(X[z,j]*T[z][i] for z in range(len(s))))
            m.addConstr(W[i,j] >= 0)


    m.addConstr(quicksum(X[0,i] for i in range(len(t))) == row['s0_equal'])                                                      # shift 0 = 320

    for i in range(len(Mt)):                                                                                                                            # shift request
        m.addConstr(X[Ms[i],Mt[i]] >= M[i])


    m.addConstr(quicksum(X[shift,day] for day in range(len(t)) for shift in range(11,14)) <= row['sNight_max'])   # night shift <=177
    m.addConstr(quicksum(X[shift,day] for day in range(len(t)) for shift in range(7,11)) <= row['sAfn_max'])       # afternoon shift <=354


    for i in range(len(t)-6):
        m.addConstr(quicksum(X[0,day] for day in range(i,i+6)) >= row['emploNum'])                                      # no 7 consect day work

    # optimize
    m.optimize()
    emplo_num.iloc[index,4] = int(m.objVal)

# the end of the optimization


# plot the employee number and thier objective value

(ggplot(emplo_num, aes(x ='emploNum', y = 'obj'))
 + geom_point()
 + stat_smooth(method='lm')
 + labs(title='emplo_num and thier objective', x='employee number', y='Objective value')
)

