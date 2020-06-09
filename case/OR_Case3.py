#!/usr/bin/env python
# coding: utf-8

# In[16]:


from gurobipy import*
import pandas as pd
from plotnine import *
import sys

# initiation

m               = Model('case3')
demandFile      = pd.read_csv("Demand.csv", header=None)
shiftTime       = pd.read_csv("shiftTime.csv", header = None)
emploAttri      = pd.read_csv("managerRequest.csv", header = 0)
requestShift    = {(24,5,9)     :1
                  ,(34,6,16)    :1
                  ,(20,13,26)   :1
                  ,(17,0,0)     :1
                  ,(17,0,1)     :1
                  ,(17,0,2)     :1
                  ,(10,0,13)    :1
                  ,(21,0,19)    :1
                  ,(11,0,14)    :1
                  ,(30,0,2)     :1
                  ,(34,0,18)    :1
                  ,(34,0,19)    :1
                  ,(28,0,30)    :1}

AMRequest       = {(0,11)       :1                                                    # (day,shift)
                  ,(9,7)        :2
                  ,(14,11)      :1
                  ,(27,11)      :1}

MRequest        = {(21,11)      :1}

S1              = {(0,19)       :0.45                                                 # (start day(weekday),
                  ,(0,20)       :0.45
                  ,(0,21)       :0.45
                  ,(0,22)       :0.45
                  ,(0,23)       :0.45
                  ,(2,19)       :0.3
                  ,(2,20)       :0.3
                  ,(2,21)       :0.3
                  ,(2,22)       :0.3
                  ,(2,23)       :0.3}                                                        

S2              = {(2,0)        :0.55                                                 # (start day(weekday),
                  ,(2,1)        :0.55
                  ,(2,2)        :0.55
                  ,(2,3)        :0.55
                  ,(2,4)        :0.55
                  ,(2,5)        :0.55
                  ,(3,19)       :0.3 
                  ,(3,20)       :0.3 
                  ,(3,21)       :0.3 
                  ,(3,22)       :0.3 
                  ,(3,23)       :0.3 
                  ,(4,19)       :0.3 
                  ,(4,20)       :0.3 
                  ,(4,21)       :0.3 
                  ,(4,22)       :0.3                                                 
                  ,(4,23)       :0.3}



# parameter
p               = [ i for i in range(24)]                                              # period
s               = [ i for i in range(14)]                                              # shift
t               = [ i for i in range(31)]                                              # day
e               = [ i for i in range(40)]                                              # employee index
D               = [ row.tolist() for index, row in demandFile.iterrows() ]             # demand 
T               = [ row.tolist() for index, row in shiftTime.iterrows() ]              # shift period
ENum            = 40
DayOffNum       = 8

is_manager      = emploAttri['is_manager']                                             # employee attribute
is_ass_mag      = emploAttri['is_ass_mag']                                             # employee attribute
seniority1      = emploAttri['seniority>=1']                                           # employee attribute
seniority2      = emploAttri['seniority>=2']                                           # employee attribute


# In[ ]:


# with diff emplo

    
# variable
X         = m.addVars(len(e),len(s),len(t), name = "IfOnSpecificShift")
W         = m.addVars(len(p), len(t), name = "ObjectiveFunction")

m.update()

# objective function

obj       = quicksum(W[i,j] for i in range(len(p)) for j in range(len(t)) )

m.setObjective(obj, GRB.MINIMIZE)

# constraint 

for i in range(len(e)):
    for j in range(len(s)):
        for z in range(len(t)):
            m.addConstr(X[i,j,z]<=1)
            m.addConstr(X[i,j,z]>=0) 

for i in range(len(e)):
    m.addConstr(quicksum(X[i,0,j] for j in range(len(t))) == DayOffNum)                                       # every emplo have 8 day off

for i in range(len(e)):
    for j in range(len(s)):
        for z in range(len(t)):
            if (i,j,z) in requestShift.keys():
                m.addConstr(X[i,j,z] == requestShift[(i,j,z)])                                                 # shift request

for j in range(len(s)):
    for z in range(len(t)):
        if (z,j) in AMRequest.keys():
            if(j==11):
                m.addConstr(quicksum(X[i,shift,z]*is_ass_mag[i] for i in range(len(e)) for shift in range(11,14)) >= AMRequest[(z,j)])# assistant or above request
            elif(j==7):
                m.addConstr(quicksum(X[i,shift,z]*is_ass_mag[i] for i in range(len(e)) for shift in range(7,11)) >= AMRequest[(z,j)])
                
for j in range(len(s)):
    for z in range(len(t)):
        if (z,j) in MRequest.keys():
            if(j==11):
                m.addConstr(quicksum(X[i,shift,z]*is_manager[i] for i in range(len(e)) for shift in range(11,14)) >= MRequest[(z,j)])# manager request
            elif(j==7):
                m.addConstr(quicksum(X[i,shift,z]*is_manager[i] for i in range(len(e)) for shift in range(7,11)) >= MRequest[(z,j)])
                  
for i in range(len(t)):
    for j in range (len(p)):                                                                                  # S1 request
        if (i,j) in S1.keys():
            m.addConstr(quicksum(X[z,k,i]*T[k][pe]*seniority1[z] for pe in range(len(p)) for z in range(len(e)) for k in range(len(s)))/ENum >= S1[(i,j)])
            
            
for i in range(len(t)):
    for j in range (len(p)):                                                                                  # S2 request
        if (i,j) in S2.keys():
            m.addConstr(quicksum(X[z,k,i]*T[k][pe]*seniority2[z] for pe in range(len(p)) for z in range(len(e)) for k in range(len(s)))/ENum >= S2[(i,j)])


            
for i in range(len(t)-6):
    for j in range(len(e)):
        m.addConstr(quicksum(X[j,shift,day] for shift in range(11,14) for day in range(i,i+6)) <= 1)          # only 1 nightS in 7 consective day
  
          
for i in range(len(t)-6):
    for j in range(len(e)):
        m.addConstr(quicksum(X[j,shift,day] for shift in range(6,11) for day in range(i,i+6)) <= 2)           # only 2 afternoonS in 7 consective day
                             
for i in range(len(t)-6):
    for j in range(len(e)):
        m.addConstr(quicksum(X[j,0,day]  for day in range(i,i+6)) >= 1)                                       # at lest 1 dayoff in 7 consective day
          
                        
for i in range(len(p)):                                                                                       # objective function
    for j in range(len(t)):
        m.addConstr(W[i,j] >= D[i][j] - quicksum(quicksum(X[emplo,z,j] for emplo in range(len(e)))*T[z][i] for z in range(len(s))))
        m.addConstr(W[i,j] >= 0)
                    


    
# optimize
m.optimize()


resultList = list()
for v in m.getVars():
    resultList.append(int(v.x))
resultList


index = 0
data = []

for i in range(len(e)):
    EmploShift = [list() for k in range(len(s))]
    for j in range(len(s)):
        for k in range(len(t)):
            EmploShift[j].append(resultList[index])
            index         += 1
    data.append(pd.DataFrame(EmploShift))
    print(data[i])
#     data[i].to_excel("case3_EmployeeShift.xlsx",sheet_name = str(i))
    with pd.ExcelWriter('case3_EmployeeShift.xlsx',engine="openpyxl", mode='a') as writer:  
        data[i].to_excel(writer, sheet_name=str(i))
    

        
        

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

# print('Obj: %g' % m.objVal)




