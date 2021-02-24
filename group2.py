import numpy as np
import pandas as pd
import csv
data1 = open('2016-17.csv','r')
reader = csv.reader(data1)

#the matrix for the given data of an year 
data2 = np.empty((13,11))

#considering the following types of students making the decision
#economically weak(TES), general category(TGS), seeking doctoral(TDS), male(TMS), female(TFS)
#we can have individual criteria scores for each DM.
TES = []
TGS = []
TDS = []
TFS = []
TMS = []

weights = np.empty((5,11))
next(reader)
i=0
for line in reader:
  if i<13:
    for j in range(11):
      data2[i][j]=float(line[j+1])
    TGS.append(float(line[4]))
    TDS.append(float(line[8]))
    TES.append(float(line[3]))
    TFS.append(float(line[1]))
    TMS.append(float(line[2]))
  #individual criteria scores by DMs 
  elif i>=13:
    for j in range(11):
      weights[i-13][j]=float(line[j+1])
  i=i+1

#Normalise data2
dataNormalised = data2/np.sqrt(np.power(data2,2).sum(axis=0))
print(dataNormalised)

#for cost criteria we will replace those columns by 1-columns
for i in range(13):
  dataNormalised[i][5]=1-dataNormalised[i][5]
  dataNormalised[i][8]=1-dataNormalised[i][8]

#normalised population of each DM for each college
#we can provide different weights for each decision maker depending upon their population in each college.
#EX- weight of DM economically backward(E) = TES in that college/(Total population of DMs in that college)
A_w=np.empty((5,13))
for i in range(13):
  A_w[0][i] = TES[i]/(TES[i]+TGS[i]+TES[i]+TMS[i]+TFS[i])
  A_w[1][i] = TGS[i]/(TES[i]+TGS[i]+TES[i]+TMS[i]+TFS[i])
  A_w[2][i] = TDS[i]/(TES[i]+TGS[i]+TES[i]+TMS[i]+TFS[i])
  A_w[3][i] = TFS[i]/(TES[i]+TGS[i]+TES[i]+TMS[i]+TFS[i])
  A_w[4][i] = TMS[i]/(TES[i]+TGS[i]+TES[i]+TMS[i]+TFS[i])

W_final = np.empty((13,11))
#Wij matrix
for i in range(13):
#for each criteria
  for j in range(5): 
  #loop over all the DMs and find their weighted average of the criteria scores for each college
    for k in range(11):   
      W_final[i][k]+=A_w[j][i]*weights[j][k]

#final normalised Wij
W_final_norm = W_final/np.sqrt(np.power(W_final,2).sum(axis=0))
print(W_final_norm)

#final decision matrix
D_final = np.empty((13,11))
for i in range(13):
  for j in range(11):
    D_final[i][j]=dataNormalised[i][j]*W_final_norm[i][j]
print(D_final)




