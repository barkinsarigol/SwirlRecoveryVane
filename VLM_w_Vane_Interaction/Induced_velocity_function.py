import numpy as np
#Function that intakes left and right end of dl vector and the x,y,z of a point
#to give the induced velocity at x,y,z per circulation of a single dl.
##def v_ind(x1,y1,z1,x2,y2,z2,x,y,z):
##    i1=(y-y1)*(z-z2)-(y-y2)*(z-z1)
##    j1=(x-x1)*(z-z2)-(x-x2)*(z-z1)
##    k1=(x-x1)*(y-y2)-(x-x2)*(y-y1)
##    denom=i1**2+j1**2+k1**2
##    fac2_AB=((x2-x1)*(x-x1)+(y2-y1)*(y-y1)+(z2-z1)*(z-z1))/np.sqrt((x-x1)**2+(y-y1)**2+(z-z1)**2)-((x2-x1)*(x-x2)+(y2-y1)*(y-y2)+(z2-z1)*(z-z2))/np.sqrt((x-x2)**2+(y-y2)**2+(z-z2)**2)
##    i1=i1/denom*fac2_AB
##    j1=j1/denom*fac2_AB
##    k1=k1/denom*fac2_AB
##
##    j2=(z-z1)/((z-z1)**2+(y1-y)**2)*(1+(x-x1)/((x-x1)**2+(y-y1)**2+(z-z1)**2))
##    k2=(y1-y)/((z-z1)**2+(y1-y)**2)*(1+(x-x1)/((x-x1)**2+(y-y1)**2+(z-z1)**2))
##
##    j3=-(z-z2)/((z-z2)**2+(y2-y)**2)*(1+(x-x2)/((x-x2)**2+(y-y2)**2+(z-z2)**2))
##    k3=-(y2-y)/((z-z2)**2+(y2-y)**2)*(1+(x-x2)/((x-x2)**2+(y-y2)**2+(z-z2)**2))
##
##    i=i1/(4*np.pi)
##    j=(j1+j2+j3)/(4*np.pi)
##    k=(k1+k2+k3)/(4*np.pi)
##    return np.array([i,j,k])

#Take note that the array gives velocities induced by a single dl at one control point and velocity vector must be multiplied by the circulations
def v_ind(a,b):
    i1=(b[-2]-a[4])*(b[-1]-a[2])-(b[-2]-a[1])*(b[-1]-a[5])   #CORRECT
    j1=-1*((b[-3]-a[3])*(b[-1]-a[2])-(b[-3]-a[0])*(b[-1]-a[5])) #ADDED MINUS SIGN PREMULTIPLIER
    k1=(b[-3]-a[3])*(b[-2]-a[1])-(b[-3]-a[0])*(b[-2]-a[4])  #CORRECT
    denom=i1**2+j1**2+k1**2  #CORRECT

    if denom !=0:
        fac2_AB=((a[0]-a[3])*(b[-3]-a[3])+(a[1]-a[4])*(b[-2]-a[4])+(a[2]-a[5])*(b[-1]-a[5]))/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)-((a[0]-a[3])*(b[-3]-a[0])+(a[1]-a[4])*(b[-2]-a[1])+(a[2]-a[5])*(b[-1]-a[2]))/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2)
        i1=i1/denom*fac2_AB           #fac2_AB CORRECTED
        j1=j1/denom*fac2_AB
        k1=k1/denom*fac2_AB
    if denom ==0:
        i1=0
        j1=0
        k1=0
    
    j2=(b[-1]-a[5])/((b[-1]-a[5])**2+(a[4]-b[-2])**2)*(1+(b[-3]-a[3])/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)) #CORRECTED
    k2=(a[4]-b[-2])/((b[-1]-a[5])**2+(a[4]-b[-2])**2)*(1+(b[-3]-a[3])/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)) #CORRECTED
    #----
    j3=-(b[-1]-a[2])/((b[-1]-a[2])**2+(a[1]-b[-2])**2)*(1+(b[-3]-a[0])/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2)) #CORRECTED
    k3=-(a[1]-b[-2])/((b[-1]-a[2])**2+(a[1]-b[-2])**2)*(1+(b[-3]-a[0])/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2)) #CORRECTED

    i=i1/(4*np.pi)
    j=(j1+j2+j3)/(4*np.pi)
    k=(k1+k2+k3)/(4*np.pi)
    return np.array([i,j,k])
    
#An additional velocity function is required as only the trailing vortices induce a velocity on the point between the trailing vortices
#and not the bound vortex

def v_ind_no_bound(a,b):
    j2=(b[-1]-a[5])/((b[-1]-a[5])**2+(a[4]-b[-2])**2)*(1+(b[-3]-a[3])/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)) #CORRECTED
    k2=(a[4]-b[-2])/((b[-1]-a[5])**2+(a[4]-b[-2])**2)*(1+(b[-3]-a[3])/np.sqrt((b[-3]-a[3])**2+(b[-2]-a[4])**2+(b[-1]-a[5])**2)) #CORRECTED
    #----
    j3=-(b[-1]-a[2])/((b[-1]-a[2])**2+(a[1]-b[-2])**2)*(1+(b[-3]-a[0])/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2)) #CORRECTED
    k3=-(a[1]-b[-2])/((b[-1]-a[2])**2+(a[1]-b[-2])**2)*(1+(b[-3]-a[0])/np.sqrt((b[-3]-a[0])**2+(b[-2]-a[1])**2+(b[-1]-a[2])**2)) #CORRECTED
    j=(j2+j3)/(4*np.pi)
    k=(k2+k3)/(4*np.pi)
    return np.array([0,j,k])

    
