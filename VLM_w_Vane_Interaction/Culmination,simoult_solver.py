import time as time
st=time.process_time()

import numpy as np
import matplotlib.pyplot as plt
import Induced_velocity_function as l
import Speed_vector_lst as m
import V_VLM_code_chordwise_vectors as n
import V_VLM_code_dl_vectors as o
import V_VLM_code_dl_vectors_at075c as p
import V_VLM_code_Horshoe_Locations as q 
import V_VLM_code_surface_normals as r
import V_VLM_code_Tangency_Locations as s

#Creating the 'b' vector:
b=np.zeros((q.n_chord*q.n_span*4,1))
for i in range(len(m.v_vec_total)):
    b[i]=-np.dot(m.v_vec_total[i],r.normals_lst[i])

#Creating the 'A' matrix:
A=np.zeros((q.n_chord*q.n_span*4,q.n_chord*q.n_span*4))
for i in range(len(s.final_lst)):
    for j in range(len(o.total_dl_lst)):
        induced_velocity=l.v_ind(o.total_dl_ends_lst[j],s.final_lst[i])
        A[i,j]=np.dot(induced_velocity,r.normals_lst[i])
print(A)

kt=time.process_time()
print("CPU time for upto linear algebra solution", kt-st)

circulations=np.linalg.solve(A, b)


#Computing the Thrust force, Fx:

#First compute total velocity vectors at every circulation location on Vane 1
sum_of_all_velocity_at_all_locations_lst=[]
for i in range(len(q.points_lst)):
    total_velocity_at_ith_circulation=np.zeros(3)

    for j in range(len(o.total_dl_lst)):
        if i != j:
            induced_velocity_at_circ=l.v_ind(o.total_dl_ends_lst[j],q.final_lst[i][-3:])*circulations[j]
            total_velocity_at_ith_circulation=total_velocity_at_ith_circulation+induced_velocity_at_circ

        if i==j:
        #Add the induced velocity of the trailing vortices around the point:
            no_bound_velocity=l.v_ind_no_bound(o.total_dl_ends_lst[i],q.final_lst[i])*circulations[i]           
            total_velocity_at_ith_circulation=total_velocity_at_ith_circulation+no_bound_velocity

    #Add the inflow velocity vector:
    total_velocity_at_ith_circulation=total_velocity_at_ith_circulation+m.v_vec_total[i]
    sum_of_all_velocity_at_all_locations_lst.append(total_velocity_at_ith_circulation)

#Get thrust of vane 1: #Fx_i=rho*Circulation_i*(Vy*dl_z-V_z*dl_y) for Vane 1.
Thrust=0
for i in range(int(q.n_span*q.n_chord)):
    ith_element_Thrust=q.rho*circulations[i]*(sum_of_all_velocity_at_all_locations_lst[i][1]*o.total_dl_lst[i][2]-sum_of_all_velocity_at_all_locations_lst[i][2]*o.total_dl_lst[i][1])
    Thrust=Thrust+ith_element_Thrust

#Get total thrust, 4 times the thrust of each vane.
Thrust=4*Thrust
print("Thrust is", Thrust*-1, "Newtons. Note: + indicates desirable force")


#--------------------------------------------

#Display Relevant Coefficients:
#You will assume that the change in Cp and Ct of propeller only is 0 when SRV is attached: See Stokkermans table 5, first three rows
#Using above assumptions, equation simplifies to:

#Enter D_p, J,Cp
n_s=q.v_inf/(q.J*q.D_p)
C_T_v=-1*Thrust/(q.rho*(n_s**2)*(q.D_p**4))
delta_eta=q.J*(C_T_v)/q.Cp
print("Thrust coefficient of the vane is", C_T_v)
print("Change in efficiency is", delta_eta)


#######WAKE MODELLING############

#####WAKE MODELLING#####
x_value_of_modelling_surface=0.5
modelling_boundary=0.32
number_of_points_in_one_direction=30
y_coord=np.linspace(-modelling_boundary,modelling_boundary,number_of_points_in_one_direction)
z_coord=np.linspace(-modelling_boundary,modelling_boundary,number_of_points_in_one_direction)

total_y_array=[]
total_z_array=[]
total_array=[]
for i in range(len(y_coord)):
    for j in range(len(z_coord)):
        total_y_array.append(y_coord[i])
        total_z_array.append(z_coord[j])
        total_array.append([y_coord[i],z_coord[j]])

y_velocity_at_array_points=[]
z_velocity_at_array_points=[]
for i in range(int(len(total_array))):
        velocity_due_to_circulation_induction=np.zeros(3)

        for j in range(len(o.total_dl_lst)):
            wake_velocity=l.v_ind(o.total_dl_ends_lst[j],[x_value_of_modelling_surface,total_array[i][0],total_array[i][1]])*circulations[j]
            velocity_due_to_circulation_induction=velocity_due_to_circulation_induction+wake_velocity

          
#####################UNCOMMENT THE NEXT REGION IF YOU WANT TO ALSO SEE THE PROPELLER VELOCITY IN THE WAKE
##        radius=np.sqrt(total_array[i][0]**2+total_array[i][1]**2)                     #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
##        if (radius<q.nacelle_radius) or (radius>(q.nacelle_radius+q.semi_span)):          #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
##            total_vel_at_array_pnt=velocity_due_to_circulation_induction                   #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
##
##        else:          #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
##            tangential_propeller_velocity_unit_vector=np.array([0,-total_array[i][1],total_array[i][0]])/radius   #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
##            prop_vel=np.array([m.v_dist_ax(radius-q.nacelle_radius),0,0])+tangential_propeller_velocity_unit_vector*m.v_dist(radius-q.nacelle_radius)  #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
##            total_vel_at_array_pnt=velocity_due_to_circulation_induction+prop_vel  #COMMENT IF YOU DON'T WANT PROP INDUCED VELOCITIES
                                                           
        total_vel_at_array_pnt=velocity_due_to_circulation_induction  ##COMMENT OUT THIS PART IF YOU WANT TO ALSO SEE PROPELLER VELOCITY IN THE WAKE
        y_velocity_at_array_points.append(total_vel_at_array_pnt[1])
        z_velocity_at_array_points.append(total_vel_at_array_pnt[2])
        
    
#ONLY ADD THE Y AND Z COMPONENT OF TOTAL VELOCITY TO LOOK AT THE ROTATION
plt.clf()
w=np.sqrt(np.array(y_velocity_at_array_points)**2+np.array(z_velocity_at_array_points)**2)

normalized_y_velocity=np.array(y_velocity_at_array_points)/w
normalized_z_velocity=np.array(z_velocity_at_array_points)/w

qq=plt.quiver(total_y_array,total_z_array,normalized_y_velocity,normalized_z_velocity,w,cmap=plt.cm.jet)
plt.colorbar(qq, cmap=plt.cm.jet, label='Velocity induced by vortices (m/s)')
plt.xlabel('y direction (m)')
plt.ylabel('z direction (m)')
plt.show()



