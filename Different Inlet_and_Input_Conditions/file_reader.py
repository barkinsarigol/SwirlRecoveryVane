import numpy as np
import pandas as pd
import os 

df = pd.read_csv("DefaDataset.csv")
##a = df.loc[:,"rad_pos"]
##b = df.loc[:,"pitch_in_rad"]
##c= df.loc[:,"norm_x"]
##d= df.loc[:,"norm_height"]

##pitch_angle_lst=[]
##for i in range(len(a)):
##    pitch_angle_lst.append([a[i],b[i]])   
##
##camber_lst=[]
##for i in range(len(c)):
##    camber_lst.append([c[i],d[i]])


#For J=1.3:
pos=list(df.loc[:,"J1.6,rad_pos"])
axial=list(df.loc[:,"J1.6,V_ax/V_inf"])
tangential=list(df.loc[:,"J1.6,V_tan/V_inf"])
