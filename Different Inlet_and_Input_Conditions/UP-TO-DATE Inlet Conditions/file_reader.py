import numpy as np
import pandas as pd
import os 

df = pd.read_csv("sept_2022_speed_graph_readings.csv")

#For J=0.95:
Va=list(df.loc[:,"Va_J=1"])
Va=Va[1:]
for i in range(len(Va)):
    Va[i]=float(Va[i])

Vt=list(df.loc[:,"Vt_J=1"])
Vt=Vt[1:]
for i in range(len(Vt)):
    Vt[i]=float(Vt[i])

x=list(df.loc[:,"X_J=1"])
x=x[0:-1]






