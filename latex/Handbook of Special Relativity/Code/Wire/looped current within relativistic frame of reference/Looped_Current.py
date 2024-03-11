### need to transform coordinates from <p> to <lab> being carefull with time
### Vp_FRMe is small if ve and vp are close together so doesnt have big ...
### influence in transform
### check all vectors using previous MAG of vector have right signage
""" This code calculates the relativistic electric field's force of a looped
    current, from the given input """
import time
import matplotlib.pyplot as plt
import numpy as np
start_time = time.time()
### Constants ################################################################
N_Y = 50
N_X = 50
N_THETA = 1000 #even # time taken is linearly increased

NANSIZE = 0.2
RADIUS = 2
AXIS_X = 3
AXIS_Y = 3
Q_p = -1
Q_e = -1

c = 1 ### all speeds/equations are in terms of speed of light
Vp_MAG = 0.99
Ve_MAG = 0.4
Vp = np.array([0, Vp_MAG,0])
gamma_Vp = 1/np.sqrt(1-Vp_MAG**2/c**2)
gamma_Ve = 1/np.sqrt(1-Ve_MAG**2/c**2)

LENGTH_lab = 1
LAM_lab = abs(Q_e) / LENGTH_lab
I = - LAM_lab * Ve_MAG

dtheta = (2 * np.pi) / (N_THETA-1)
dL = RADIUS * dtheta
EPS0 = 8.854 * 10**(-12)
CC_dE = ( dL * LAM_lab ) / ( 4 * np.pi * EPS0 )

uu = np.linspace(-AXIS_X, AXIS_X, N_X)
vv = np.linspace(-AXIS_Y, AXIS_Y, N_Y)
x_p,y_p = np.meshgrid(uu, vv)
R_xy = np.sqrt(x_p*x_p + y_p*y_p)

Xloop_data = np.zeros((N_THETA,3))
Xe_FRMp_data = np.zeros((N_THETA,3))
Xe_FRMe_data = np.zeros((N_THETA,3))
Xi_FRMp_data = np.zeros((N_THETA,3))

E_FRMp_x = np.zeros([N_Y,N_X])
E_FRMp_y = np.zeros([N_Y,N_X])
E_FRMp_z = np.zeros([N_Y,N_X])

############################# CALCULATIONS ###################################
Xp = np.zeros([N_Y,N_X,len(Vp)]) * np.nan
CC_FRMp = (gamma_Vp-1)/Vp_MAG**2
CC_FRMe = (gamma_Ve-1)/Ve_MAG**2

for j in range(N_X):
    for i in range(N_Y):
    ### Positions: <lab> #####################################################
        if R_xy[i,j] > RADIUS + NANSIZE or R_xy[i,j] < RADIUS - NANSIZE:
            Xp[i,j,:] = np.array( [ x_p[i,j], y_p[i,j],0 ] )

for k in range(N_THETA):
    theta = k * dtheta
    CT = np.cos(theta)
    ST = np.sin(theta)
    Xloop = np.array([RADIUS * CT, RADIUS * ST,0])
    Ve = np.array([- Ve_MAG * ST, Ve_MAG * CT,0])

    ### Velocity Transform ###################################################
    VDOT = np.dot(Vp,Ve)
    Vp_FRMe = ( Vp - Ve*gamma_Ve + ( (gamma_Ve-1) * VDOT / Ve_MAG**2 ) * Ve )\
            / ( gamma_Ve * ( 1-VDOT/c**2 ) )
    Vp_FRMe_MAG = np.linalg.norm(Vp_FRMe)
    gamma_Vpe = 1 / np.sqrt(1 - (Vp_FRMe_MAG/c)**2)

    ### ions coords: <lab> --> <p> ###########################################
    DOTi = np.dot(Vp,Xloop)
    Ti = DOTi/c**2 # ions are stationary in <lab> (time doesnt change position)
    Xi_FRMp = Xloop + ( CC_FRMp * DOTi - gamma_Vp * Ti ) * Vp
    Ti_FRMp = gamma_Vp * ( Ti - DOTi/c**2 )

    ### electron coords: <lab> --> <e> #######################################
    DOTe1 = np.dot(Ve, Xloop) # this = 0
    Te = 0
    Xe_FRMe = Xloop + ( CC_FRMe * DOTe1 - gamma_Ve * Te ) * Ve
    #Te_FRMe = gamma_Ve * ( Te - DOTe1/c**2 ) ###

    ### electron coords: <e> --> <p> #########################################
    DOTe2 = np.dot(Vp_FRMe,Xe_FRMe)
    Te_FRMe = DOTe2 / c**2
    CC_FRMpe = (gamma_Vpe-1) / Vp_FRMe_MAG**2
    Xe_FRMp = Xe_FRMe + ( CC_FRMpe * DOTe2 - gamma_Vpe * Te_FRMe) * Vp_FRMe
    ###### why does it give figure of 8??
    #Te_FRMp = gamma_Vpe * ( Te_FRMe - DOT/c**2 )

    ### Plot Data ###
    Xloop_data[k,:] = Xloop[:]
    Xi_FRMp_data[k,:] = Xi_FRMp[:]
    Xe_FRMe_data[k,:] = Xe_FRMe[:]
    Xe_FRMp_data[k,:] = Xe_FRMp[:]

    for j in range(N_X):
        for i in range(N_Y):
            if np.isnan(Xp[i,j,0]):
                continue
            ### Atoms Field: frame <p> #######################################
            DOT_Xp = np.dot(Vp,Xp[i,j])
            Ti = DOT_Xp/c**2 #(Ti_FRMp / gamma_Vp) + DOT_Xp/c**2
            Xp_FRMp = Xp[i,j] + ( CC_FRMp * DOT_Xp - gamma_Vp * Ti ) * Vp
            Delta_i = Xp_FRMp - Xi_FRMp
            dE_i_FRMp = CC_dE * ( Delta_i / np.linalg.norm(Delta_i)**3 )

            ### Electrons field: frame <p> ###################################
            DOTe1 = np.dot(Ve,Xp[i,j])
            Te = 0
            Xp_FRMe = Xp[i,j] + ( CC_FRMe * DOTe1 - gamma_Ve * Te ) * Ve
            DOTe2 = np.dot(Vp_FRMe,Xp_FRMe)
            Te_FRMe = DOTe2 / c**2#(Te_FRMp / gamma_Vp) + DOTe2 / c**2
            Xp_FRMep = Xp_FRMe + ( CC_FRMpe * DOTe2 - gamma_Vpe * Te_FRMe ) * Vp_FRMe
            Delta_e = Xp_FRMep - Xe_FRMp #Xp - Xloop
            dE_e_FRMp = - CC_dE * ( Delta_e / np.linalg.norm(Delta_e)**3 )

            ### Total E-Field ################################################
            E_FRMp_x[i,j] = E_FRMp_x[i,j] + (dE_e_FRMp[0] + dE_i_FRMp[0])
            E_FRMp_y[i,j] = E_FRMp_x[i,j] + (dE_e_FRMp[1] + dE_i_FRMp[1])

### E-Field Force  ###########################################################
F_FRMp_x = E_FRMp_x * Q_p
F_FRMp_y = E_FRMp_y * Q_p

Vp_UNIT = Vp / Vp_MAG ### or should this be Vp_FRMe and done for every theta
CC_Vp = 1/np.sqrt(1+(Vp_UNIT[0]**2/Vp_UNIT[1]**2))
Vp_perp_UNIT = np.array([CC_Vp, -(Vp_UNIT[0]/Vp_UNIT[1])*CC_Vp,0])
##### is it perpendicular to this or do we need perpendicular to each Vp_FRMe #####

F_FRMp_para = Vp_UNIT[0] * F_FRMp_x + Vp_UNIT[1] * F_FRMp_y
F_FRMp_perp = Vp_perp_UNIT[0] * F_FRMp_x + Vp_perp_UNIT[1] * F_FRMp_y
F_para = F_FRMp_para
F_perp = F_FRMp_perp / gamma_Vp

F_x = F_para * Vp_UNIT[0] + F_perp * Vp_perp_UNIT[0]
F_y = F_para * Vp_UNIT[1] + F_perp * Vp_perp_UNIT[1]

### coordinates: frame <p> ###################################################
x_p_FRMp = np.zeros([N_Y,N_X])
y_p_FRMp = np.zeros([N_Y,N_X])
for j in range(N_X):
    for i in range(N_Y):
        coord = np.array([x_p[i,j] , y_p[i,j],0])
        coord = coord + ( ((gamma_Vp-1)/Vp_MAG**2) * np.dot(Vp,coord) ) * Vp
        x_p_FRMp[i,j] = coord[0]
        y_p_FRMp[i,j] = coord[1]

### nan large E values #######################################################
E_FRMp_xnan = np.where(R_xy < RADIUS + NANSIZE, np.nan, E_FRMp_x)
E_FRMp_x = np.where(R_xy < RADIUS - NANSIZE, E_FRMp_x, E_FRMp_xnan)
E_FRMp_ynan = np.where(R_xy < RADIUS + NANSIZE, np.nan, E_FRMp_y)
E_FRMp_y = np.where(R_xy < RADIUS - NANSIZE, E_FRMp_y, E_FRMp_ynan)
F_FRMp_xnan = np.where(R_xy < RADIUS + NANSIZE, np.nan, F_FRMp_x)
F_FRMp_x = np.where(R_xy < RADIUS - NANSIZE, F_FRMp_x, F_FRMp_xnan)
F_FRMp_ynan = np.where(R_xy < RADIUS + NANSIZE, np.nan, F_FRMp_y)
F_FRMp_y = np.where(R_xy < RADIUS - NANSIZE, F_FRMp_y, F_FRMp_ynan)
F_xnan = np.where(R_xy < RADIUS + NANSIZE, np.nan, F_x)
F_x = np.where(R_xy < RADIUS - NANSIZE, F_x, F_xnan)
F_ynan = np.where(R_xy < RADIUS + NANSIZE, np.nan, F_y)
F_y = np.where(R_xy < RADIUS - NANSIZE, F_y, F_ynan)

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

plt.figure(2, figsize=(15,6))
plt.subplot(121)
plt.title('F_x' )
plt.contourf(x_p,y_p, F_x, 100, cmap= 'bwr')
plt.colorbar()
plt.subplot(122)
plt.title('F_y')
plt.contourf(x_p,y_p, F_y, 100, cmap= 'bwr')
plt.colorbar()

plt.figure(3)
plt.title('electron and ion positions in different frames')
plt.plot(Xloop_data[:,0], Xloop_data[:,1], '.', label="both FRMlab")
plt.plot(Xe_FRMe_data[:,0], Xe_FRMe_data[:,1], '.', label="Electons FRMe")
plt.plot(Xe_FRMp_data[:,0], Xe_FRMp_data[:,1], '.', label="Electons FRMp")
plt.plot(Xi_FRMp_data[:,0], Xi_FRMp_data[:,1], '.', label="Atoms FRMp")
plt.ylabel('y')
plt.legend(loc='best')

plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))

### Save Files ###############################################################
#    np.savetxt("./Save files/Wire_x_p.txt", x_p)
#    np.savetxt("./Save files/Wire_y_p.txt", y_p)
#    np.savetxt("./Save files/Wire_E_FRMp_x.txt", E_FRMp_x)
#    np.savetxt("./Save files/Wire_E_FRMp_y.txt", E_FRMp_y)
#E_x = np.loadtxt("E_x.txt")

### starting all with t=0

# =============================================================================
#     ### ions coords: <lab> --> <p> ###########################################
#     DOT = np.dot(Vp,Xloop)
#     Ti = 0#DOT/c**2 # ions are stationary in <lab> (time doesnt change position)
#     Xi_FRMp = Xloop + ( CC_FRMp * DOT - gamma_Vp * Ti ) * Vp
#     Ti_FRMp = gamma_Vp * ( Ti - DOT/c**2 )
#
#     ### electron coords: <lab> --> <e> #######################################
#     DOT = np.dot(Ve, Xloop) # this = 0
#     Te = 0
#     Xe_FRMe = Xloop + ( CC_FRMe * DOT - gamma_Ve * Te ) * Ve
#     Te_FRMe = gamma_Ve * ( Te - DOT/c**2 ) ###
#
#     ### electron coords: <e> --> <p> #########################################
#     DOT = np.dot(Vp_FRMe,Xe_FRMe)
#     #Te_FRMe = DOT / c**2
#     CC_FRMpe = (gamma_Vpe-1) / Vp_FRMe_MAG**2
#     Xe_FRMp = Xe_FRMe + ( CC_FRMpe * DOT - gamma_Vpe * Te_FRMe) * Vp_FRMe
#     ###### why does it give figure of 8??
#     Te_FRMp = gamma_Vpe * ( Te_FRMe - DOT/c**2 )
#
#     ### Plot Data ###
#     Xloop_data[k,:] = Xloop[:]
#     Xi_FRMp_data[k,:] = Xi_FRMp[:]
#     Xe_FRMe_data[k,:] = Xe_FRMe[:]
#     Xe_FRMp_data[k,:] = Xe_FRMp[:]
#
#     for j in range(N_X):
#         for i in range(N_Y):
#             if np.isnan(Xp[i,j,0]):
#                 continue
#             DOT_Xp = np.dot(Vp,Xp[i,j])
#             ### Atoms Field: frame <p> #######################################
#             Ti = 0#(Ti_FRMp / gamma_Vp) + DOT_Xp/c**2
#             Xp_FRMp = Xp[i,j] + ( CC_FRMp * DOT_Xp - gamma_Vp * Ti ) * Vp
#             Delta_i = Xp_FRMp - Xi_FRMp
#             dE_i_FRMp = CC_dE * ( Delta_i / np.linalg.norm(Delta_i)**3 )
#
#             ### Electrons field: frame <p> ###################################
#             DOTe1 = np.dot(Ve,Xp[i,j])
#             Xp_FRMe = Xp[i,j] + ( CC_FRMe * DOTe1 - gamma_Ve * Te ) * Ve
#             DOTe2 = np.dot(Vp_FRMe,Xp_FRMe)
#             Te_FRMe = gamma_Ve * ( Te - DOTe1/c**2 )# (Te_FRMp / gamma_Vp) + DOTe2 / c**2
#             Xp_FRMep = Xp_FRMe + ( CC_FRMpe * DOTe2 - gamma_Vpe * Te_FRMe ) * Vp_FRMe
#             Delta_e = Xp_FRMep - Xe_FRMp #Xp - Xloop
#             dE_e_FRMp = - CC_dE * ( Delta_e / np.linalg.norm(Delta_e)**3 )
# =============================================================================