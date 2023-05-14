#INPUTS TO BE DIRECTLY COPIED:
#GEOMETRIC INPUTS
#Vane specifications


#BELOW DATA IS FROM TOM STOKKERMANS TWIST AND NACA4409

camber_distribut=[[0.0, 0.0], [0.017223684, 0.005], [0.037019737, 0.008], [0.051881579, 0.011], [0.070671053, 0.013], [0.091473684, 0.017], [0.116203947, 0.02], [0.138960526, 0.023], [0.158756579, 0.026], [0.180506579, 0.028], [0.20425, 0.031], [0.224006579, 0.032], [0.246763158, 0.035], [0.268493421, 0.036], [0.291210526, 0.037], [0.315901316, 0.038], [0.345526316, 0.039], [0.390940789, 0.04], [0.418572368, 0.04], [0.461973684, 0.039], [0.507368421, 0.039], [0.546822368, 0.038], [0.601039474, 0.035], [0.654289474, 0.033], [0.700611842, 0.03], [0.740026316, 0.027], [0.776480263, 0.024], [0.817848684, 0.02], [0.900585526, 0.012], [1.0, 0.0]]
twist_distribut=[[0.0, -0.093125782], [0.003019187, -0.092876449], [0.007420993, -0.091754452], [0.011822799, -0.090258456], [0.015886005, -0.08838846], [0.020626411, -0.085895132], [0.025705418, -0.083027806], [0.032138826, -0.079038482], [0.039926637, -0.07392716], [0.047037246, -0.06981317], [0.054147856, -0.065823846], [0.058888262, -0.063330519], [0.063628668, -0.061460523], [0.068707675, -0.059465861], [0.074125282, -0.057845198], [0.078527088, -0.057221866], [0.081574492, -0.056723201], [0.089362302, -0.056598534], [0.09511851, -0.057346533], [0.099520316, -0.058343864], [0.103922122, -0.059465861], [0.111032731, -0.062208521], [0.11780474, -0.065574513], [0.123560948, -0.069189838], [0.135750564, -0.077293153], [0.146585779, -0.084773135], [0.129994357, -0.073179162], [0.141168172, -0.080908477], [0.153696388, -0.089011792], [0.161145598, -0.093375115], [0.158775395, -0.092253118], [0.166224605, -0.09561911], [0.171303612, -0.097364439], [0.175366817, -0.098112437], [0.179430023, -0.098237104], [0.183493228, -0.097738438], [0.1875, -0.096491774]]
semi_span=0.1875   #Propeller radius minus nacelle radius
nacelle_radius=0.0625

#This part of geometry is a bit different than Stokkermans
chord_distribut=[[0,0.0455],[0.12,0.0455],[0.1875,0.0455]]  #[span,chord length]
le_offset_distribut=[[0,0],[0.12,0],[0.24,0]] #[span,leading edge offset]

#Enter number of data points along span and chord
n_chord=40
n_span=40

#Air specification
rho=1.225
v_inf=70     #in m/s
wind_span_lst=[0.0, 0.051886792, 0.146226415, 0.221698113, 0.316037736, 0.391509434, 0.471698113, 0.551886792, 0.632075472, 0.70754717, 0.806603774, 0.948113208, 1.0] #radial locations list, starting at 0 and going to 1 
v_tan=[0.231, 0.3285, 0.417, 0.4575, 0.492, 0.516, 0.5295, 0.5295, 0.513, 0.501, 0.5445, 0.228, 0.0915] #tangential velocity as a fraction v_inf
v_ax=[1.174683544, 1.313924051, 1.412658228, 1.491139241, 1.569620253, 1.632911392, 1.691139241, 1.741772152, 1.789873418, 1.812658228, 1.62278481, 1.02278481, 0.936708861] #axial velocity is obtained as a percentage of v_inf

#Prop specifications
J=0.95  #Propeller advance ratio
D_p=0.48  #Propeller diameter in m
Cp=1.042  #Propeller power coefficient
