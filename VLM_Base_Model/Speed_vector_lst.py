import V_VLM_code_Horshoe_Locations as c
from scipy import interpolate
import numpy as np 
#Inputs 
v_inf=c.v_inf     
span_lst=np.array(c.wind_span_lst)*c.semi_span
v_tan=np.array(c.v_tan)*v_inf
v_ax=np.array(c.v_ax)*v_inf

#------------------------------------------------
    
v_dist = interpolate.interp1d(span_lst,v_tan)

v_lst=[]
for i in range(len(c.points_lst)):
    v_lst.append(v_dist(c.points_lst[i][0]))

#----------------------------------------------------
    
v_dist_ax = interpolate.interp1d(span_lst,v_ax)

v_lst_ax=[]
for i in range(len(c.points_lst)):
    v_lst_ax.append(v_dist_ax(c.points_lst[i][0]))

#-----------------------------------------------
#Speed vectors of Vane 1
v_vec_vane1=[]
for l in range(len(v_lst)):
    v_vec_vane1.append(np.array([v_lst_ax[l],0,v_lst[l]]))      

v_vec_total=v_vec_vane1



    
