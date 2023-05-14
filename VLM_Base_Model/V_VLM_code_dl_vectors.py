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
span_lst=np.linspace(0,semi_span,n_span+1)

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

#Show vane in space (just for verification)
final_lst=points_lst
X=[]
Y=[]
Z=[]
for i in range(len(final_lst)):
    X.append(final_lst[i][6])
    Y.append(final_lst[i][7])
    Z.append(final_lst[i][8])

# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter3D(X,Y,Z,marker=".")
# plt.show()
#----------------------------------------------------------------------------
#Create a list of dl(s) for each vane: (You still need to check this).
dl_vane1=[]
i=0
dl_ends_vane1=[]
while i < n_chord*(n_span+1)-n_chord:
    dl_x=points_lst[i+n_chord][-3]-points_lst[i][-3]
    dl_y=points_lst[i+n_chord][-2]-points_lst[i][-2]
    dl_z=points_lst[i+n_chord][-1]-points_lst[i][-1]
    dl_vane1.append([dl_x,dl_y,dl_z])
    
    dl_ends_vane1.append([points_lst[i+n_chord][-3],points_lst[i+n_chord][-2],points_lst[i+n_chord][-1],points_lst[i][-3],points_lst[i][-2],points_lst[i][-1]])
    i=i+1

total_dl_lst=dl_vane1
total_dl_ends_lst=dl_ends_vane1
#Note that the dl vector goes from point 1 to 2, from root to tip for all vanes
#Every vector in dl ends has the form: [x2,y2,z2,x1,y1,z1]
    



    
    




