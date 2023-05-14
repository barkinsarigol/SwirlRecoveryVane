from scipy import interpolate
import numpy as np
from mpl_toolkits import mplot3d 
# Axes3D import has side effects, it enables using projection='3d' in add_subplot
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------------------
#GEOMETRIC INPUTS
#Vane specifications
#You NO LONGER need the same amount of points for twist, chord and le_offset lists

camber_distribut=[[0.0, 0.0], [0.017223684, 0.005], [0.037019737, 0.008], [0.051881579, 0.011], [0.070671053, 0.013], [0.091473684, 0.017], [0.116203947, 0.02], [0.138960526, 0.023], [0.158756579, 0.026], [0.180506579, 0.028], [0.20425, 0.031], [0.224006579, 0.032], [0.246763158, 0.035], [0.268493421, 0.036], [0.291210526, 0.037], [0.315901316, 0.038], [0.345526316, 0.039], [0.390940789, 0.04], [0.418572368, 0.04], [0.461973684, 0.039], [0.507368421, 0.039], [0.546822368, 0.038], [0.601039474, 0.035], [0.654289474, 0.033], [0.700611842, 0.03], [0.740026316, 0.027], [0.776480263, 0.024], [0.817848684, 0.02], [0.900585526, 0.012], [1.0, 0.0]]
twist_distribut=[[0.0, -0.093125782], [0.003019187, -0.092876449], [0.007420993, -0.091754452], [0.011822799, -0.090258456], [0.015886005, -0.08838846], [0.020626411, -0.085895132], [0.025705418, -0.083027806], [0.032138826, -0.079038482], [0.039926637, -0.07392716], [0.047037246, -0.06981317], [0.054147856, -0.065823846], [0.058888262, -0.063330519], [0.063628668, -0.061460523], [0.068707675, -0.059465861], [0.074125282, -0.057845198], [0.078527088, -0.057221866], [0.081574492, -0.056723201], [0.089362302, -0.056598534], [0.09511851, -0.057346533], [0.099520316, -0.058343864], [0.103922122, -0.059465861], [0.111032731, -0.062208521], [0.11780474, -0.065574513], [0.123560948, -0.069189838], [0.135750564, -0.077293153], [0.146585779, -0.084773135], [0.129994357, -0.073179162], [0.141168172, -0.080908477], [0.153696388, -0.089011792], [0.161145598, -0.093375115], [0.158775395, -0.092253118], [0.166224605, -0.09561911], [0.171303612, -0.097364439], [0.175366817, -0.098112437], [0.179430023, -0.098237104], [0.183493228, -0.097738438], [0.1875, -0.096491774]]
semi_span=0.1875   #Propeller radius minus nacelle radius
nacelle_radius=0.0625

#This part of geometry is a bit different than Stokkermans
chord_distribut=[[0,0.029512],[0.016271,0.031028],[0.032154,0.032541],[0.046488,0.035187],[0.06495,0.038974],[0.079416,0.041622],[0.09375,0.044269],[0.110795,0.046541],[0.123192,0.048055],[0.136365,0.049188],[0.149923,0.049568],[0.164256,0.048433],[0.175878,0.046156],[0.1875,0.039352]]  #[span,chord length]
le_offset_distribut=[[0,0],[0.12,0],[0.24,0]] #[span,leading edge offset]

#Enter number of data points along span and chord
n_chord=40
n_span=40

#Air specification
rho=1.203
v_inf=68     #in m/s

wind_span_lst=[0.0, 0.057007448, 0.140137666, 0.220898217, 0.30403972, 0.384800271, 0.46793049, 0.546321372, 0.631832543, 0.712593094, 0.793353645, 0.871744527, 0.954874746, 1.0]
v_tan=[0.018, 0.018, 0.0465, 0.075, 0.0975, 0.1125, 0.126, 0.132, 0.1335, 0.1275, 0.1185, 0.105, 0.0795, 0.051]
v_ax=[0.815189873, 0.979746835, 1.007594937, 1.032911392, 1.058227848, 1.083544304, 1.108860759, 1.126582278, 1.139240506, 1.146835443, 1.149367089, 1.141772152, 1.086075949, 1.030379747]


#Prop specifications
J=1.6  #Propeller advance ratio
D_p=0.5  #Propeller diameter in m
Cp=0.510  #Propeller power coefficient
CTP=0.245

#-----------------------------------------------------------------------------------------

#Put variables into separate lists
span_pos1=[]
for i in range(len(twist_distribut)):
    span_pos1.append(twist_distribut[i][0])
    
span_pos2=[]
for i in range(len(chord_distribut)):
    span_pos2.append(chord_distribut[i][0])
    
span_pos3=[]
for i in range(len(le_offset_distribut)):
    span_pos3.append(le_offset_distribut[i][0])

camber_pos=[]
for i in range(len(camber_distribut)):
    camber_pos.append(camber_distribut[i][0])

camber=[]
for i in range(len(camber_distribut)):
    camber.append(camber_distribut[i][1])

twist=[]
for i in range(len(twist_distribut)):
    twist.append(twist_distribut[i][1])

chord=[]
for i in range(len(chord_distribut)):
    chord.append(chord_distribut[i][1])

le_offset=[]
for i in range(len(le_offset_distribut)):
    le_offset.append(le_offset_distribut[i][1])


#Interpolate between camber, twist, leading edge offset and chord points

camber_dist = interpolate.interp1d(camber_pos,camber) #Mean Camber at chordwise points (when chord normalized to 1))
twist_dist = interpolate.interp1d(span_pos1,twist) #Twist as a function of span
chord_dist = interpolate.interp1d(span_pos2,chord) #chord length as a function of span
le_offset_dist = interpolate.interp1d(span_pos3,le_offset) #leading edge offset at spanwise positions


#Elements positions along the chord and span
span_element_width=semi_span/n_span
span_lst=np.linspace(span_element_width/2,semi_span-span_element_width/2,n_span)

chord_element_width=1/n_chord
normalized_chord_lst=np.linspace(0.25*chord_element_width,1-0.75*chord_element_width,n_chord)


#Label all points and assign them  properties:[span_posz,chordwise_pos,camber,twist,local_chord,le_offset] and the points into a list.
points_lst=[]
for i in range(len(span_lst)):
    for j in range(len(normalized_chord_lst)):
        points_lst.append([span_lst[i],normalized_chord_lst[j],camber_dist(normalized_chord_lst[j]),twist_dist(span_lst[i]),chord_dist(span_lst[i]),le_offset_dist(span_lst[i])])
print(points_lst)
print("DONE \n")

#Turn previous properties into X-Y-Z POSITIONS OF POINTS ON A GIVEN VANE GEOMETRY and append x,y,z coordinates to points_lst:
for i in range(len(points_lst)):
    x=(points_lst[i][1])*(points_lst[i][4])*np.cos(points_lst[i][3])+np.sin(points_lst[i][3])*(points_lst[i][2])*(points_lst[i][4])+points_lst[i][5]
    y=points_lst[i][0]+nacelle_radius
    z=-1*(points_lst[i][1]-0.25)*(points_lst[i][4])*np.sin(points_lst[i][3])+np.cos(points_lst[i][3])*(points_lst[i][2])*(points_lst[i][4])
    points_lst[i]=points_lst[i]+[x]+[y]+[z]

#Charcterize Vane 2 (On opposite side of vane 1) and append to points_lst:
#This means multiplying y by -1 to get new y and multiplying z by -1 to get new z
second_lst=[]
for i in range(len(points_lst)):
    new_z=-points_lst[i][8]
    new_y=-points_lst[i][7]
    second_element=[points_lst[i][0]]+[points_lst[i][1]]+[points_lst[i][2]]+[points_lst[i][3]]+[points_lst[i][4]]+[points_lst[i][5]]+[points_lst[i][6]]+[new_y]+[new_z]
    second_lst.append(second_element)

#Characterize Vane 3 (Its span lies on the positive z-axis):
#With reference to vane 1, new z= old y, and the new y equals the negative of the previous z coordinate
third_lst=[]
for i in range(len(points_lst)):
    new_z=points_lst[i][7]
    new_y=-points_lst[i][8]
    third_element=[points_lst[i][0]]+[points_lst[i][1]]+[points_lst[i][2]]+[points_lst[i][3]]+[points_lst[i][4]]+[points_lst[i][5]]+[points_lst[i][6]]+[new_y]+[new_z]
    third_lst.append(third_element)

#Characterize Vane 4 (Its span lies on the negative z-axis):
#With reference to vane 1, new z= minus old y, and the new y equals the previous z coordinate
fourth_lst=[]
for i in range(len(points_lst)):
    new_z=-points_lst[i][7]
    new_y=points_lst[i][8]
    fourth_element=[points_lst[i][0]]+[points_lst[i][1]]+[points_lst[i][2]]+[points_lst[i][3]]+[points_lst[i][4]]+[points_lst[i][5]]+[points_lst[i][6]]+[new_y]+[new_z]
    fourth_lst.append(fourth_element)
 
#Show vane in space (just for verification)
final_lst=points_lst+second_lst+third_lst+fourth_lst #Be careful with this!!
X=[]
Y=[]
Z=[]
for i in range(len(final_lst)):
    X.append(final_lst[i][6])
    Y.append(final_lst[i][7])
    Z.append(final_lst[i][8])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(X,Y,Z,marker=".")
plt.show()

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
#Find circulations (Simoulataneous Equations)
#Find force




