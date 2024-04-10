# remember that this is still in the relativistic frame at the moment
# is there relativistic affects due to accelleration?
from Coordinate_Transforms import (Gamma)
import matplotlib.pyplot as plt 
import numpy as np
import time
start_time = time.time()
##############################################################################
### Constants ###
save = 0
n=50 # even # every doubling gives increased time by factor of 4
m = 100 #even # time taken is linearly increased 
if 1 > 0:
    nansize = 0.1
    Radius = 2
    axis = 3
    q_p = -1
    q_e = -1
    c = 1
    Vp_MAG = 0.99#99 # in y direction
    Ve_MAG = 0.3 # magnitude only
    gamma_Vp = Gamma(Vp_MAG)
    gamma_Ve = Gamma(Ve_MAG) 
    Length_lab = 1
    LAM_lab = q_e / Length_lab ### what lenght is l_lab?
    I = LAM_lab * Ve_MAG
    
    dtheta = (2 * np.pi) / (m-1)
    dL = Radius * dtheta
    CC_dE = ( dL * LAM_lab ) / ( 4 * np.pi * 8.854 * 10**(-12) )
    
    uu = vv = np.linspace(-axis, axis, n)
    x_p,y_p = np.meshgrid(uu, vv)
    R_xy = np.sqrt(x_p*x_p + y_p*y_p)
    
    loop_xdata = np.zeros((m,1))
    loop_ydata = np.zeros((m,1))
    loop_FRMep_xdata = np.zeros((m,1))
    loop_FRMep_ydata = np.zeros((m,1))
    loop_FRMe_xdata = np.zeros((m,1))
    loop_FRMe_ydata = np.zeros((m,1))
    atom_FRMp_xdata = np.zeros((m,1))
    atom_FRMp_ydata = np.zeros((m,1))
    E_FRMp_MAG = np.zeros([n,n])
    E_FRMp_x = np.zeros([n,n])
    E_FRMp_y = np.zeros([n,n])
    E_FRMp_z = np.zeros([n,n])
    E_x = np.zeros([n,n])
    E_y = np.zeros([n,n])
    E_z = np.zeros([n,n])
    Ee_FRMep_x = np.zeros([n,n])
    Ee_FRMep_y = np.zeros([n,n])
    Ee_FRMep_z = np.zeros([n,n])
    Ea_FRMp_x = np.zeros([n,n])
    Ea_FRMp_y = np.zeros([n,n])
    x_p_FRMp = np.zeros([n,n])
    y_p_FRMp = np.zeros([n,n]) 
    
T0=0
Vp = np.array([0, Vp_MAG])
X_p = np.zeros([n,n,len(Vp)])
X_p_FRMp = np.zeros([n,n,len(Vp)])
T_FRMe = np.zeros([n,n,m])

CC_FRMp1 = (gamma_Vp-1)/Vp_MAG**2
CC_FRMp2 = gamma_Vp * T0
CC_FRMe1 = (gamma_Ve-1)/Ve_MAG**2
CC_FRMe2 = gamma_Ve * T0
n_STEP = ((2*axis)/(n-1))

##############################################################################
### Calculations ###

for j in range(n):
    for i in range(n):
        ### Positions: <lab> --> <p> 
        
        X_p[i,j,:] = np.array([ i * n_STEP - axis, j * n_STEP - axis]) ### is j and i right way around?
        X_p_FRMp[i,j,:] = X_p[i,j] + ( CC_FRMp1 * np.dot(Vp,X_p[i,j]) - CC_FRMp2 ) * Vp
        
for k in range(m):
    theta = k * dtheta 
    CT = np.cos(theta)
    ST = np.sin(theta)
    loop = np.array([Radius * CT, Radius * ST])
    Ve = np.array([- Ve_MAG * ST, Ve_MAG * CT])
        
    ### loop coords: <lab> --> <p>
    dot= np.dot(Vp,loop)
    #CC_FRMp3 = gamma_Vp * (dot/c**2)
    loop_FRMp = loop + ( CC_FRMp1 * dot - CC_FRMp2 ) * Vp

    ### loop coords: <lab> --> <e>
    CC1 = 1 / (  gamma_Ve * ( 1 - ( np.dot(Vp,Ve) / c**2 ) )  )
    CC2 = CC_FRMe1 * np.dot(Vp,Ve) - gamma_Ve  
    Vp_FRMe = CC1 * (Vp + CC2 * Ve) #### a minus ??? or Ve_FRMp?
    Vp_FRMe_MAG = np.linalg.norm(Vp_FRMe)
    gamma_Vep = 1/ np.sqrt(1 - (Vp_FRMe_MAG/c)**2)
    loop_FRMe = loop + ( CC_FRMe1 * np.dot(Ve,loop) - CC_FRMe2 ) * Ve
    #T00 = (1/gamma_Vep)*(np.dot(Vp_FRMe,loop_FRMe)/c**2) + np.dot(Ve,loop)/c**2
    T_loop_FRMe = gamma_Ve * ( T0 - np.dot(Ve,loop)/c**2 )
    
    # not needed as loop is perpendicular to Ve?
    
    ### loop coords: <e> --> <p>
    LT_X = loop_FRMe
    LT_T = T_loop_FRMe
    LT_V = Vp_FRMe
    CC_FRMep = (gamma_Vep-1)/Vp_FRMe_MAG**2 
    loop_FRMep = LT_X + ( CC_FRMep * np.dot(LT_V,LT_X) - gamma_Vep * LT_T) * LT_V
    
    loop_xdata[k,0] = loop[0]
    loop_ydata[k,0] = loop[1]    
    atom_FRMp_xdata[k,0] = loop_FRMp[0]
    atom_FRMp_ydata[k,0] = loop_FRMp[1]
    loop_FRMe_xdata[k,0] = loop_FRMe[0]
    loop_FRMe_ydata[k,0] = loop_FRMe[1]
    loop_FRMep_xdata[k,0] = loop_FRMep[0]
    loop_FRMep_ydata[k,0] = loop_FRMep[1]

    ### i and j arrangement???
    for j in range(n):
        for i in range(n):
            ##################################################################
            ### Atoms Field ###! CHECKED !###
            disp = X_p_FRMp[i,j,:] - loop_FRMp
            dE_a = - CC_dE * ( disp / np.linalg.norm(disp)**3 )
            
            ##################################################################
            ### Electrons field ###
            ### <lab> --> <e> ###
            X_p_FRMe = X_p[i,j] + ( CC_FRMe1 * np.dot(Ve,X_p[i,j]) - CC_FRMe2 ) * Ve
            T_FRMe = gamma_Ve * ( T0 - np.dot(Ve,X_p[i,j])/c**2 ) # for all points
            
            ### <e> --> <p> ###
            X_p_FRMep = X_p_FRMe + ( CC_FRMep * np.dot(Vp_FRMe,X_p_FRMe) - gamma_Vep * T_FRMe ) * Vp_FRMe                 
            
            ##################################################################
            ### Electron E-field: Frame <ep> ###! CHECKED !###
            disp = X_p_FRMep - loop_FRMep #X_p - loop
            dE_e = CC_dE * ( disp / np.linalg.norm(disp)**3 )
            
            ##################################################################
            ### Total E-Field ### ###! CHECKED !###
            E_FRMp_x[i,j] = E_FRMp_x[i,j] + dE_e[0] + dE_a[0]
            E_FRMp_y[i,j] = E_FRMp_y[i,j] + dE_e[1] + dE_a[1]
            ##################################################################
            
            
##### have to transform each coordniate twice immeadiatly from electron to particle and then take dE??
E_FRMp_MAG = np.sqrt(E_FRMp_x*E_FRMp_x + E_FRMp_y*E_FRMp_y + E_FRMp_z*E_FRMp_z)

### coordinates: frame <p>
for j in range(n):
    for i in range(n):
        ### Positions: <lab> --> <p> 
        coord = np.array([x_p[i,j] , y_p[i,j]])
        coord = coord + ( ((gamma_Vp-1)/Vp_MAG**2) * np.dot(Vp,coord) - gamma_Vp * T0 ) * Vp
        x_p_FRMp[i,j] = coord[0]
        y_p_FRMp[i,j] = coord[1]
        
##############################################################################
### nan large E values ###
if 1 > 0:
    #if Z < nansize:
    E_FRMp_xnan = np.where(R_xy < Radius + nansize, np.nan, E_FRMp_x)
    E_FRMp_x = np.where(R_xy < Radius - nansize, E_FRMp_x, E_FRMp_xnan)
    E_FRMp_ynan = np.where(R_xy < Radius + nansize, np.nan, E_FRMp_y)
    E_FRMp_y = np.where(R_xy < Radius - nansize, E_FRMp_y, E_FRMp_ynan)
    E_FRMp_MAGnan = np.where(R_xy < Radius + nansize, np.nan, E_FRMp_MAG)
    E_FRMp_MAG = np.where(R_xy < Radius - nansize, E_FRMp_MAG, E_FRMp_MAGnan)

##############################################################################
### Save Files ###
if save == 1:
    np.savetxt("./Save files/x_p.txt", x_p)
    np.savetxt("./Save files/y_p.txt", y_p)
    np.savetxt("./Save files/E_FRMp_x.txt", E_FRMp_x)
    np.savetxt("./Save files/E_FRMp_y.txt", E_FRMp_y) #E_x = np.loadtxt("E_x.txt")
    np.savetxt("./Save files/E_FRMp_MAG.txt", E_FRMp_MAG)
##############################################################################
### PLOT ###

plt.figure(1, figsize=(15,6))
plt.subplot(121)
plt.title('E_FRMp_x' )
plt.contourf(x_p_FRMp,y_p_FRMp, E_FRMp_x, 100, cmap= 'bwr')
plt.colorbar()

plt.subplot(122)
plt.title('E_FRMp_y')
plt.contourf(x_p_FRMp,y_p_FRMp, E_FRMp_y, 100, cmap= 'bwr')
plt.colorbar() #plt.ylim(-5, 5)
#plt.axhline(y=0, color='k')
#plt.axvline(x=0, color='k')

plt.figure(2)
plt.title('E_Total')
plt.contourf(x_p_FRMp,y_p_FRMp, E_FRMp_MAG, 100, cmap= 'bwr')
plt.colorbar() 

plt.figure(3)
plt.title('loops in different frames')
plt.plot(loop_xdata, loop_ydata, '.', label="both FRMlab")
plt.plot(loop_FRMep_xdata, loop_FRMep_ydata, '.', label="Electons FRMp/ep")
plt.plot(loop_FRMe_xdata, loop_FRMe_ydata, '.', label="Electons FRMe (element)")
plt.plot(atom_FRMp_xdata, atom_FRMp_ydata, '.', label="Atoms FRMp")
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='best')

plt.show()

print(" Run time: %s seconds" % (time.time() - start_time))
##############################################################################
##############################################################################
#Ea_FRMp_x[i,j] = Ea_FRMp_x[i,j] + dE_a[0]
#Ea_FRMp_y[i,j] = Ea_FRMp_y[i,j] + dE_a[1]
#E_FRMp_x = Ea_FRMp_x + Ee_FRMep_x
#E_FRMp_y = Ea_FRMp_y + Ee_FRMep_y