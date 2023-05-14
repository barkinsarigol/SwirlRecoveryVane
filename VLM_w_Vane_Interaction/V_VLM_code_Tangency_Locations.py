from V_VLM_code_Horshoe_Locations import *
import numpy as np

#Defining the spanwise and the chordwise positions of the tangency points

#Elements positions along the chord and span
span_lst_tan=np.linspace(span_element_width/2,semi_span-span_element_width/2,n_span)
normalized_chord_lst_tan=np.linspace(0.75*chord_element_width,1-0.25*chord_element_width,n_chord)

#Label all points and assign them  properties:[span_posz,chordwise_pos,camber,twist,local_chord,le_offset] and the points into a list.
points_lst=[]
for i in range(len(span_lst_tan)):
    for j in range(len(normalized_chord_lst_tan)):
        points_lst.append([span_lst_tan[i],normalized_chord_lst_tan[j],camber_dist(normalized_chord_lst_tan[j]),twist_dist(span_lst_tan[i]),chord_dist(span_lst_tan[i]),le_offset_dist(span_lst_tan[i])])
print(points_lst)


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
#plt.show()  -->UNCOMMENT IF NECESSARY
