import time
st=time.process_time()

import matplotlib.pyplot as plt
import numpy as np
import Induced_velocity_function as l
import Speed_vector_lst as m
import V_VLM_code_chordwise_vectors as n
import V_VLM_code_dl_vectors as o
import V_VLM_code_dl_vectors_at075c as p
import V_VLM_code_Horshoe_Locations as q 
import V_VLM_code_surface_normals as r
import V_VLM_code_Tangency_Locations as s


#Creating the 'b' vector:
b=np.zeros((q.n_chord*q.n_span,1))
for i in range(len(m.v_vec_total)):
    b[i]=-np.dot(m.v_vec_total[i],r.normals_lst[i])

#Creating the 'A' matrix:
A=np.zeros((q.n_chord*q.n_span,q.n_chord*q.n_span))
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
Thrust_loading=[]            ####ADDED

for i in range(int(q.n_span*q.n_chord)):
    ith_element_Thrust=q.rho*circulations[i]*(sum_of_all_velocity_at_all_locations_lst[i][1]*o.total_dl_lst[i][2]-sum_of_all_velocity_at_all_locations_lst[i][2]*o.total_dl_lst[i][1])
    Thrust=Thrust+ith_element_Thrust
    Thrust_loading.append(ith_element_Thrust)    ####ADDED
    

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

et=time.process_time()
print("CPU time", et-st)
print("Thrust coefficient of the vane is", C_T_v)
print("Change in efficiency is", delta_eta)



########Thrust Loading##############

local_thrust=[]
for i in range(q.n_span):
	local_thrust.append(sum(Thrust_loading[q.n_chord*i:q.n_chord*(i+1)]))
thrust_loading=np.array(local_thrust)*(-1)/(q.semi_span/q.n_chord)
thrust_loading=np.vstack((np.zeros(1),thrust_loading,np.zeros(1)))

span_array=np.linspace(1/q.n_span*0.5,q.semi_span-1/q.n_span*0.5,int(q.n_span))
span_array=np.hstack((np.zeros(1),span_array,np.array([q.semi_span])))

plt.plot(span_array,thrust_loading)
plt.xlabel('Semi span of one SRV blade, excluding nacelle radius (m)')
plt.ylabel('Thrust loading (N/m)')
plt.show()









