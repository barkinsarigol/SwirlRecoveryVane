import numpy as np
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

wind_span_lst=[0.0, 0.059377116, 0.140148951, 0.223279169, 0.304028436, 0.389550891, 0.465560821, 0.546321372, 0.629451591, 0.707842473, 0.793353645, 0.876483864, 0.957244414, 1.0]
v_tan=[-0.0285, -0.0405, -0.0165, 0.0105, 0.03, 0.048, 0.06, 0.069, 0.0735, 0.0735, 0.069, 0.06, 0.0435, 0.027]
v_ax=[0.782278481, 0.949367089, 0.967088608, 0.984810127, 1.002531646, 1.02278481, 1.037974684, 1.053164557, 1.065822785, 1.073417722, 1.075949367, 1.073417722, 1.048101266, 1.02278481]

#Prop specifications
J=1.8  #Propeller advance ratio
D_p=0.5  #Propeller diameter in m
Cp=1    # NOT TRUE, IN REALITY, THIS IS NOT GIVEN
CTP=1   # NOT TRUE, IN REALITY THIS IS NOT GIVEN

    
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

d_axiale = 0.25*(2-0.9) #since the SRV in the CFD simulations is located 2*Rp away from the propeller but the speed is measured 0.9*Rp behind the propeller.
#Hence 1.1*R_p must be used for the correction distance when accounting for the lack of axial infinity.

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


#create the LHS matrix:-------------------------------------------
A=np.zeros((n_span,n_span))

#Add the Gamma_j terms:
for i in range(n_span):
    velocity_tot= np.sqrt((ax_velocity_dist(lst[i]))**2+(tan_velocity_dist(lst[i]))**2)
    for j in range(n_span):       
        A[i][j]=-1/(4*np.pi*velocity_tot)*(-1/(lst[j]-lst[i]+dl/2)+1/(lst[j]-lst[i]-dl/2))

#Add Gamma_i terms to the diagonals:
for i in range(n_span):
    velocity_tot= np.sqrt((ax_velocity_dist(lst[i]))**2+(tan_velocity_dist(lst[i]))**2)
    A[i][i]=A[i][i]+2/(velocity_tot*(chord_dist(lst[i]))*a_0)

#create the RHS Column vector:------------------------------------
b=np.zeros((n_span,1))
for i in range(n_span):
    psi_i=np.arctan(tan_velocity_dist(lst[i])/ax_velocity_dist(lst[i]))
    b[i][0]=twist_dist(lst[i])+psi_i-alpha_0 -a_0*chord_dist(lst[i])*(twist_dist(lst[i])+psi_i-alpha_0)/(4*np.pi*d_axiale)

#solve for circulations:------------------------------------------
circulations=np.linalg.solve(A, b)  

#calculate thrust:------------------------------------------------
#List below gives elementary thrust at each interval
#Note that axial velocity and tangential velocity are interpolated separately
#rather than interpolating the total velocity to find total velocity at each circulation
thrust_at_dl=[]
for i in range(len(lst)):
    thrust_at_dl.append(tan_velocity_dist(lst[i])*circulations[i])
    for j in range(len(lst)):
        thrust_at_dl.append(circulations[i]*circulations[j]/(4*np.pi)*(-1/(lst[j]-lst[i]+dl/2)+1/(lst[j]-lst[i]-dl/2)))

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

#WHOLE CODE VERIFIED, VALIDATION NECESSARY!
