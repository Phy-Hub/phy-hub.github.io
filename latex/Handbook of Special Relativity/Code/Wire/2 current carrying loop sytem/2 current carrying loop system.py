# assuming no self force on 
# this is for E-field only on a frame dependent on the velocity of electrons on effected loop
## protons in affected loop experience no Efield, only moving electrons
# this also assumes effected loop has electrons equally distributed and surce loop doesnt efect that
import matplotlib.pyplot as plt 
import numpy as np
import time
start_time = time.time()

##############################################################################
### Setup ###
Radius_SL = 2
Radius_EL = 2
centreX_EL = 0
centreY_EL = 0
centreZ_EL = 1

c = 1
V_SL = 0.001
V_EL = 0.001


lambda_intial = 1
gamma_SL = 1 / np.sqrt(1 - (V_SL/c)**2)
const_lambda_t = lambda_intial * gamma_SL * (V_SL / c**2)
epsilon_0 = 8.854 * 10**(-12)
const_dE = (1/(4*np.pi*epsilon_0))

n_x = 3
n_z = 10
n_angle = 100
dangle = (2 * np.pi) / (n_angle-1)
#r_diff = np.zeros((n_angle,n_angle))

u = np.linspace(-2, 2, n_x)
v = np.linspace(2, 10, n_z)
centreX_EL, centreZ_EL = np.meshgrid(u, v)
E_TotalMag = 0 * centreZ_EL

##############################################################################
### Calculations ###

for k in range(n_z):
    for l in range(n_x):
        E_x = E_y = E_z = 0
        for i in range(n_angle):
            # point on source loop (SL)
            theta = i * dangle 
            CT = np.cos(theta)
            ST = np.sin(theta)
            
            x_SL = Radius_SL * CT
            y_SL = Radius_SL * ST
            z_SL = 0
            
            Vx_SL = V_SL * np.sin(theta)
            Vy_SL = V_SL * np.cos(theta)
            Vz_SL = 0
            
            for j in range(n_angle):
                # point on Effected loop (EL)
                PHI = j * dangle # point on ring's theta
                CP = np.cos(PHI)
                SP = np.sin(PHI)
                
                x_EL = Radius_EL * CP + centreX_EL[k,l]
                y_EL = Radius_EL * SP + centreY_EL
                z_EL = centreZ_EL[k,l]
                x_diff = x_EL - x_SL
                y_diff = y_EL - y_SL
                z_diff = z_EL - z_SL
                r_diff =  np.sqrt( x_diff**2 + y_diff**2 + z_diff**2 )
                hat_x_diff = x_EL - x_SL / r_diff
                hat_y_diff = y_EL - y_SL / r_diff
                hat_z_diff = z_EL - z_SL / r_diff # make sure r_diff != 0 at all points
                
                #Vx_EL = V_SL * np.sin(PHI)
                #Vy_EL = V_SL * np.cos(PHI)
                #Vz_EL = 0
                
                # velocity of current in the dL of effected loop parralel to dl of source loop
                V_parralel = V_SL * np.cos(PHI) * np.sin(theta) +  \
                             V_SL * np.sin(PHI) * np.cos(theta)                                       
                lambda_t = const_lambda_t * V_parralel  # line charge density       
                dQ_SL = lambda_t * Radius_SL * dangle
                dE = const_dE * dQ_SL / r_diff**2
                
                dE_x = dE * hat_x_diff
                dE_y = dE * hat_y_diff
                dE_z = dE * hat_z_diff
                   
                E_x = E_x + dE_x
                E_y = E_y + dE_y
                E_z = E_z + dE_z
                
        E_TotalMag[k,l] = np.sqrt(E_x*E_x + E_y*E_y + E_z*E_z)
        #print(E_TotalMag)

##############################################################################
### Save Files ###
np.savetxt("centreX_EL.txt", centreX_EL)
np.savetxt("centreZ_EL.txt", centreZ_EL)
np.savetxt("E_TotalMag.txt", E_TotalMag)#E_x = np.loadtxt("E_x.txt")
##############################################################################
### PLOT ###

plt.figure(1, figsize=(15,6))
plt.subplot(121)
plt.title('E_TotalMag' )
plt.contourf(centreX_EL, centreZ_EL, E_TotalMag, 100, cmap= 'bwr')
plt.colorbar()
plt.show()

# =============================================================================
plt.figure(2,figsize=(6,6))
plt.title('E with loop centred on y axis' )
plt.plot(centreZ_EL[:,1], E_TotalMag[:,1])
plt.plot(centreZ_EL[:,1], 2* 7100 / (centreZ_EL[:,1]))
plt.plot(centreZ_EL[:,1], 4* 7100 / (centreZ_EL[:,1]**2))
plt.show()
# =============================================================================



print(" Run time: %s seconds" % (time.time() - start_time))
##############################################################################
##############################################################################