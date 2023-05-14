from scipy import interpolate
import numpy as np
from mpl_toolkits import mplot3d 
# Axes3D import has side effects, it enables using projection='3d' in add_subplot
import matplotlib.pyplot as plt
import V_VLM_code_Horshoe_Locations as ho

camber_distribut=ho.camber_distribut
twist_distribut=ho.twist_distribut
chord_distribut=ho.chord_distribut
le_offset_distribut=ho.le_offset_distribut
semi_span=ho.semi_span
nacelle_radius=ho.nacelle_radius
n_chord=ho.n_chord
n_span=ho.n_span

#----------------------------------------------------------------------

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
normalized_chord_lst=np.linspace(0,1,n_chord+1)


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
#plt.show() -->UNCOMMENT FOR DISPLAY

#-----------------------------------------------------------------------------------------------
#Create a list of dc(s) that correspond to the dl(s): (You still need to check this)

dc_vane1=[]
for i in range((n_chord+1)*(n_span)-1): 
    if (i+1)%(n_chord+1) !=0:
        dc_x=points_lst[i+1][-3]-points_lst[i][-3]
        dc_y=points_lst[i+1][-2]-points_lst[i][-2]
        dc_z=points_lst[i+1][-1]-points_lst[i][-1]
        dc_vane1.append([dc_x,dc_y,dc_z])

dc_vane2=[]
for i in range((n_chord+1)*(n_span)-1): 
    if (i+1)%(n_chord+1) !=0:
        dc_x=second_lst[i+1][-3]-second_lst[i][-3]
        dc_y=second_lst[i+1][-2]-second_lst[i][-2]
        dc_z=second_lst[i+1][-1]-second_lst[i][-1]
        dc_vane2.append([dc_x,dc_y,dc_z])

dc_vane3=[]
for i in range((n_chord+1)*(n_span)-1): 
    if (i+1)%(n_chord+1) !=0:
        dc_x=third_lst[i+1][-3]-third_lst[i][-3]
        dc_y=third_lst[i+1][-2]-third_lst[i][-2]
        dc_z=third_lst[i+1][-1]-third_lst[i][-1]
        dc_vane3.append([dc_x,dc_y,dc_z])

dc_vane4=[]
for i in range((n_chord+1)*(n_span)-1): 
    if (i+1)%(n_chord+1) !=0:
        dc_x=fourth_lst[i+1][-3]-fourth_lst[i][-3]
        dc_y=fourth_lst[i+1][-2]-fourth_lst[i][-2]
        dc_z=fourth_lst[i+1][-1]-fourth_lst[i][-1]
        dc_vane4.append([dc_x,dc_y,dc_z])

total_dc_lst=dc_vane1+dc_vane2+dc_vane3+dc_vane4
