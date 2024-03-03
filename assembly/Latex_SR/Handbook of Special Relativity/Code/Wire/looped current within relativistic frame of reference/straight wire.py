### need to transform coordinates from <p> to <lab> being carefull with time
### Vp_FRMe is small if ve and vp are close together so doesnt have big influence in transform
import SR_Functions as SR
import matplotlib.pyplot as plt
import numpy as np
import time
start_time = time.time()
### Constants ################################################################
if 0==0:
    N_y = 3
    N_x = 10
    N_length = 1000 #even # time taken is linearly increased
    Xline_length = 10000

    nansize = 0.3
    axis_x = 3
    axis_y = 1
    q_p = -1
    q_e = -1
    T0=0

    c = 1 ### all speeds are in terms of speed of light, and hence any equations using them
    Vp_MAG = 0.8
    Ve_MAG = 0.4
    Ve = np.array([0, Ve_MAG])
    Vp = np.array([0, Vp_MAG])
    GAM_Vp = 1/np.sqrt(1-Vp_MAG**2/c**2)
    GAM_Ve = 1/np.sqrt(1-Ve_MAG**2/c**2)

    Length_lab = 1
    LAM_lab = abs(q_e) / Length_lab ### what lenght is Length_lab?
    I = - LAM_lab * Ve_MAG ### this is correct from definition and from percells derivation

    dL = Xline_length/ N_length
    Eps0 = 8.854 * 10**(-12)
    CC_dE = ( dL * LAM_lab ) / ( 4 * np.pi * Eps0 )

    uu = np.linspace(-axis_x, axis_x, N_x)
    vv = np.linspace(-axis_y, axis_y, N_y)
    x_p,y_p = np.meshgrid(uu, vv)
    Dist_from_x = np.sqrt(x_p*x_p)

    Xline_data = np.zeros((N_length,2))
    Xe_FRMp_data = np.zeros((N_length,2))
    Xe_FRMe_data = np.zeros((N_length,2))
    Xi_FRMp_data = np.zeros((N_length,2))
    ions_FRMp_check = np.zeros((N_length,1))
    elec_FRMe_check = np.zeros((N_length,1))
    elec_FRMp_check = np.zeros((N_length,1))

    E_FRMp_x = np.zeros([N_y,N_x])
    E_FRMp_y = np.zeros([N_y,N_x])

############################## Velocity Transform ############################
DOT_UV = np.dot(Vp,Ve)
Vp_FRMe = SR.TRANS_Velocity( Vp, Ve, Ve_MAG, GAM_Ve, DOT_UV)
Vp_FRMe_MAG = Vp_FRMe[1]                                                       # as all velocities in z-direction
GAM_Vp_FRMe = SR.Gamma(Vp_FRMe_MAG)
CC_FRMpe = (GAM_Vp_FRMe-1)/Vp_FRMe_MAG**2
############################# CALCULATIONS ###################################
x_p = np.where(x_p**2 < nansize**2, nansize , x_p)
Xp = np.zeros([N_y,N_x,len(Vp)])
CC_FRMp = (GAM_Vp-1)/Vp_MAG**2
CC_FRMe = (GAM_Ve-1)/Ve_MAG**2

for j in range(N_x):
    for i in range(N_y):
    ### Positions: <lab> #####################################################
        Xp[i,j,:] = np.array( [ x_p[i,j], y_p[i,j] ] )

for k in range(N_length):
    Xline = np.array([0,  k * dL - Xline_length/2 ])

    ### ions coords: <lab> --> <p> ###########################################
    DOT = np.dot(Vp,Xline)

    Ti = DOT/c**2 # ions are stationary in lab frame therefore time doesnt change position in this frame
    Xi_FRMp = Xline + ( CC_FRMp * DOT - GAM_Vp * Ti ) * Vp
    Ti_FRMp = GAM_Vp * ( Ti - DOT/c**2 )

    ### electron coords: <lab> --> <e> #######################################
    DOT = np.dot(Ve,Xline)
    Te = 0
    Xe_FRMe = Xline + ( CC_FRMe * DOT - GAM_Ve * Te ) * Ve
    #Te_FRMe = GAM_Ve * ( Te - DOT/c**2 ) ###

    ### electron coords: <e> --> <p> #########################################
    DOT = np.dot(Vp_FRMe,Xe_FRMe) ## is this
    Te_FRMe = DOT/c**2
    Xe_FRMp = Xe_FRMe + ( CC_FRMpe * DOT - GAM_Vp_FRMe * Te_FRMe) * Vp_FRMe
    Te_FRMp = GAM_Vp_FRMe * ( Te_FRMe - DOT/c**2 )

    ### Plot Data ###
    Xline_data[k,:] = Xline[:]
    Xi_FRMp_data[k,:] = Xi_FRMp[:]
    Xe_FRMe_data[k,:] = Xe_FRMe[:]
    Xe_FRMp_data[k,:] = Xe_FRMp[:]

    for j in range(N_x):
        for i in range(N_y):
            DOT_Xp = np.dot(Vp,Xp[i,j])

            ### Atoms Field: frame <p> #######################################
            Ti = (Ti_FRMp / GAM_Vp) + DOT_Xp/c**2
            Xp_FRMp = Xp[i,j] + ( CC_FRMp * DOT_Xp - GAM_Vp * Ti ) * Vp
            Delta_i = Xp_FRMp - Xi_FRMp
            dE_i = CC_dE * ( Delta_i / np.linalg.norm(Delta_i)**3 )

## check if using theta or theta prime
            #DOT_i_FRMp = np.dot(Xp_FRMp, - Vp)  ### this is not general should really be transformed z axis (0,0,1)
            #cos_i = DOT_i_FRMp / (Vp_MAG*np.linalg.norm(Xp_FRMp))
           # dE_i = ((1-Vp_MAG**2/c**2) / (1+(Vp_MAG/c)*cos_i)**2 ) *dE_i ### which velocity mag is V

            ### Electrons field: frame <p> ################################### this might not be correct, but just roughly
            DOTe1 = np.dot(Ve,Xp[i,j])
            Xp_FRMe = Xp[i,j] + ( CC_FRMe * DOTe1 - GAM_Ve * Te ) * Ve
            DOTe2 = np.dot(Vp_FRMe,Xp_FRMe)
            Te_FRMe = DOTe2 / c**2 #Te = (Te_FRMp / GAM_Vp) + DOT_Xp / c**2
            Xp_FRMep = Xp_FRMe + ( CC_FRMpe * DOTe2 - GAM_Vp_FRMe * Te_FRMe ) * Vp_FRMe
            Delta_e = Xp_FRMep - Xe_FRMp #Xp - Xline
            dE_e = - CC_dE * ( Delta_e / np.linalg.norm(Delta_e)**3 )

# =============================================================================
#             DOT_e_FRMp = np.dot(Xp_FRMep, - Vp_FRMe)
#             cos_e = DOT_e_FRMp / (Vp_FRMe_MAG*np.linalg.norm(Xp_FRMep)) # DOTe1 or e2? Vp_MAGor Vp_FRMe
#             dE_e = ((1-Vp_FRMe_MAG**2/c**2) / (1+(Vp_FRMe_MAG/c)*cos_e)**2 ) *dE_e ### which velocity mag is V
# =============================================================================

            ### Total E-Field ################################################
            E_FRMp_x[i,j] += dE_e[0] + dE_i[0]
            E_FRMp_y[i,j] += dE_e[1] + dE_i[1]

F_E_x = E_FRMp_x * q_p / GAM_Vp

### CHECKS ###################################################################
B_Field = - I / (2 * np.pi * Eps0 * c**2 * x_p) ### double check minus sign
F_B = q_p * B_Field * Vp_MAG
F_book = (q_p * Vp_MAG * Ve_MAG * LAM_lab ) / (2 * np.pi * Eps0 * c**2 * x_p)
print(F_E_x-F_B) ## want this to be zero ###

ions_FRMp_check = Xline_data[:,1] / GAM_Vp
elec_FRMe_check = Xline_data[:,1] * GAM_Ve
elec_FRMp_check = Xline_data[:,1] * (GAM_Ve/ GAM_Vp_FRMe)

### coordinates: frame <p> ###################################################
x_p_FRMp = np.zeros([N_y,N_x])
y_p_FRMp = np.zeros([N_y,N_x])
for j in range(N_x):
    for i in range(N_y):
        coord = np.array([x_p[i,j] , y_p[i,j]])
        coord = coord + ( ((GAM_Vp-1)/Vp_MAG**2) * np.dot(Vp,coord) - GAM_Vp * T0 ) * Vp #t0?
        x_p_FRMp[i,j] = coord[0]
        y_p_FRMp[i,j] = coord[1]

### nan large E values #######################################################
E_FRMp_x = np.where(Dist_from_x < nansize, np.nan, E_FRMp_x)
E_FRMp_y = np.where(Dist_from_x < nansize, np.nan, E_FRMp_y)
F_B = np.where(Dist_from_x < nansize, np.nan, F_B)
F_E_x = np.where(Dist_from_x < nansize, np.nan, F_E_x)

### PLOT #####################################################################
plt.figure(1, figsize=(15,6))
plt.subplot(121)
plt.title('E_FRMp_x' )
plt.contourf(x_p_FRMp,y_p_FRMp, E_FRMp_x, 100, cmap= 'bwr')
plt.colorbar()
plt.subplot(122)
plt.title('E_FRMp_y')
plt.contourf(x_p_FRMp,y_p_FRMp, E_FRMp_y, 100, cmap= 'bwr')
plt.colorbar()

plt.figure(2)
plt.title('electron and ion positions in different frames')
plt.plot(Xline_data[:,0], Xline_data[:,1], '.', label="both FRMlab")
plt.plot(Xe_FRMe_data[:,0]+0.04, Xe_FRMe_data[:,1], '.', label="Electons FRMe")
plt.plot(Xe_FRMe_data[:,0]+0.042, elec_FRMe_check, '.', label="Elec FRMe !check!")
plt.plot(Xe_FRMp_data[:,0]+0.08, Xe_FRMp_data[:,1], '.', label="Electons FRMp")
plt.plot(Xi_FRMp_data[:,0]+0.082, elec_FRMp_check, '.', label="Elec FRMp !check!")
plt.plot(Xi_FRMp_data[:,0]+0.11, Xi_FRMp_data[:,1], '.', label="Atoms FRMp")
plt.plot(Xi_FRMp_data[:,0]+0.112, ions_FRMp_check, '.', label="Ions FRMp !check!")
plt.ylabel('y')
plt.legend(loc='best')

plt.figure(3, figsize=(15,6))
plt.subplot(121)
plt.title('Magnetic Force F_B')
plt.contourf(x_p,y_p, F_B, 100, cmap= 'bwr')
plt.colorbar()
plt.subplot(122)
plt.title('Electric Force F_E_FRMp')
plt.contourf(x_p_FRMp,y_p_FRMp, F_E_x, 100, cmap= 'bwr')
plt.colorbar()

plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))

### Save Files ###############################################################
#    np.savetxt("./Save files/Wire_x_p.txt", x_p)
#    np.savetxt("./Save files/Wire_y_p.txt", y_p)
#    np.savetxt("./Save files/Wire_E_FRMp_x.txt", E_FRMp_x)
#    np.savetxt("./Save files/Wire_E_FRMp_y.txt", E_FRMp_y) #E_x = np.loadtxt("E_x.txt")