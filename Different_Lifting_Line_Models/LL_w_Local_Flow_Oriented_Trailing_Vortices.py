from scipy.optimize import fsolve, root
import numpy as np
from functools import partial
from scipy import interpolate
import time
st=time.process_time()
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#-------------PUT BETWEEN THE LINES THE INPUT FILE-------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#GEOMETRIC INPUTS
#Vane specifications


#BELOW DATA IS FROM TOM STOKKERMANS TWIST AND NACA4409

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

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------


dl=semi_span/n_span

#Put geometric variables into separate lists
span_pos1=[]
for i in range(len(twist_distribut)):
    span_pos1.append(twist_distribut[i][0]+nacelle_radius)    
    
span_pos2=[]
for i in range(len(chord_distribut)):
    span_pos2.append(chord_distribut[i][0]+nacelle_radius)

twist=[]
for i in range(len(twist_distribut)):
    twist.append(twist_distribut[i][1])

chord=[]
for i in range(len(chord_distribut)):
    chord.append(chord_distribut[i][1])



#Interpolate between twist, leading edge offset and chord points

twist_dist = interpolate.interp1d(span_pos1,twist) #Twist as a function of span
chord_dist = interpolate.interp1d(span_pos2,chord) #chord length as a function of span


#Now do an interpolation for axial and tangential velocity:


tan_velocity_dist = interpolate.interp1d(nacelle_radius+np.array(wind_span_lst)*semi_span,np.array(v_tan)*v_inf)
ax_velocity_dist = interpolate.interp1d(nacelle_radius+np.array(wind_span_lst)*semi_span,np.array(v_ax)*v_inf)

#Polar properties for NACA4409:
alpha_0=-4.373*np.pi/180  # in radians
a_0=0.1094*180/(np.pi) # in /radians  # SEE PDF IN HONOURS RESOURCES FOR THIS DATA

#------------------------------------------------

#Centre point of all horseshoe vortices with y coordinates measured from the centre
lst=nacelle_radius+np.linspace(dl/2,semi_span-dl/2,n_span)

#-----------------------------------------------------
#NEW WRITTEN CODE: -----------------------------------
#-----------------------------------------------------


#Define induced velocity function yielding velocity induced by both the right and left trailing vortices at a point:
def v_ind_no_bound(a,b):
    j2=-(b[-1]-a[5])/((b[-1]-a[5])**2+(a[4]-b[-2])**2)*(1+(b[-3]-a[3])/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)) 
    k2=-(a[4]-b[-2])/((b[-1]-a[5])**2+(a[4]-b[-2])**2)*(1+(b[-3]-a[3])/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)) 
    #----
    j3=(b[-1]-a[2])/((b[-1]-a[2])**2+(a[1]-b[-2])**2)*(1+(b[-3]-a[0])/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2)) 
    k3=(a[1]-b[-2])/((b[-1]-a[2])**2+(a[1]-b[-2])**2)*(1+(b[-3]-a[0])/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2))
    j=(j2+j3)/(4*np.pi)
    k=(k2+k3)/(4*np.pi)
    return np.array([0,j,k])

induced_x_velocity_at_each_i=[]
induced_z_velocity_at_each_i=[]
for i in range(len(lst)):
    x_velocities_at_i=[]
    z_velocities_at_i=[]
    for j in range(len(lst)): 
        #Calculate velocities induced onto point i by the trailing vortices at both sides of point j
        psi_j=np.arctan(tan_velocity_dist(lst[j])/ax_velocity_dist(lst[j])) #EDIT THIS TO CHANGE SWIRL RECOVERY PERCENTAGE (MULTIPLY THIS LINE BY A NUMBER BETWEEN 0 AND 1)
        
        #Compute the velocity using the velocity function
        v_induced_rotated= v_ind_no_bound([0,lst[j]-dl/2,0,0,lst[j]+dl/2,0],[0,lst[i],0])   #Check order of point 1 and 2
        
        #Rotate velocity components      (since v_induced is in the frame of reference of the trailing vortices of point j, aligned with local swirl)
        #In addition, since all points lie on a straight line, velocities in x & y in the reference frame of the trailing vortex of point j is 0)
        #x_unrotated and z_unrotated are in the global coordinate frame where as components of v_induced_rotated are in the local frame of reference of trailing vortices of point j, with x aligned with trailing vortex
        x_unrotated = v_induced_rotated[-1]*np.sin(psi_j)*-1
        z_unrotated = v_induced_rotated[-1]*np.cos(psi_j)
    
        #Append to velocities at i
        x_velocities_at_i.append(x_unrotated)
        z_velocities_at_i.append(z_unrotated)
    
    induced_x_velocity_at_each_i.append(x_velocities_at_i)
    induced_z_velocity_at_each_i.append(z_velocities_at_i)
    


#Solve non-linear simoulataneous equations: (i is the point the equation is formulated about)
    
def f_point( circulations,i, z_weights, x_weights):
    V_in= np.sqrt((ax_velocity_dist(lst[i]))**2+(tan_velocity_dist(lst[i]))**2)
    psi=np.arctan(tan_velocity_dist(lst[i])/ax_velocity_dist(lst[i]))
    top = sum((z_weights[l]*np.cos(psi)-x_weights[l]*np.sin(psi)) * circulations[l]  for l in range(len(circulations)))
    bottom = sum((z_weights[l]*np.sin(psi)+x_weights[l]*np.cos(psi)) * circulations[l]  for l in range(len(circulations) ))
    
    some_result = -np.arctan((top)/(bottom+V_in)) + alpha_0 + 2*circulations[i]/(V_in*(chord_dist(lst[i]))*a_0) - twist_dist(lst[i]) - psi
    
    #When function is solved, some_result should be 0
    return some_result

functions = []
for i in range(n_span):
    z_weights = induced_z_velocity_at_each_i[i]
    x_weights = induced_x_velocity_at_each_i[i]
    functions.append(partial(f_point, i=i, z_weights = z_weights, x_weights = x_weights))

equations = lambda circulations: [func(circulations) for func in functions]

x0 = [1] * n_span

it=time.process_time()
print("The time upto but not including the solution finding", it-st)

solution = root(equations, x0)

kt=time.process_time()
print("Time for non-linear solver", kt-it)

#print(np.sum(abs(solution)))  For Checking 


#calculate thrust:------------------------------------------------
#List below gives elementary thrust at each interval
#Note that axial velocity and tangential velocity are interpolated separately
#rather than interpolating the total velocity to find total velocity at each circulation
thrust_at_dl=[]
for i in range(len(lst)):
    thrust_at_dl.append(tan_velocity_dist(lst[i])*solution.x[i])
    for j in range(len(lst)):
        thrust_at_dl.append(solution.x[i]*solution.x[j]*induced_z_velocity_at_each_i[i][j])
Thrust=4*rho*dl*sum(thrust_at_dl)


#--------------------------------------------
   
#Display Relevant Coefficients:
#You will assume that the change in Cp and Ct of propeller only is 0 when SRV is attached: See Stokkermans table 5, first three rows
#Using above assumptions, equation simplifies to:

#Enter D_p, J,Cp
n_s=v_inf/(J*D_p)
C_T_v=1*Thrust/(rho*(n_s**2)*(D_p**4))
delta_eta=J*(C_T_v)/Cp
et=time.process_time()
print("CPU time is", et-st)
print("Thrust coefficient of the vane is", C_T_v)
print("Change in efficiency is", delta_eta)
print("Thrust is", Thrust)
print("Total system efficiency:", delta_eta + J/Cp*CTP)

