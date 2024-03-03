""" this is not general and will also initially neglect full frame transformations"""
### c = 1
### double checking theta's and frame changes
import SR_Functions as SR
import matplotlib.pyplot as plt
import numpy as np
import time
start_time = time.time()
print("start time = ", time.strftime("%H:%M:%S"))
### Constants ################################################################
N_x = 30
N_Line = 10000                                                                 #even
Line_Len = 1000
axis_y = 3
y_data = np.linspace(0, axis_y, num=N_x ) + 0.1

Vp_MAG = 0.008
Ve_MAG = 0.0000000004
Ve = np.array([0,0, Ve_MAG])
Vp = np.array([0,0, Vp_MAG])
GAM_Vp = SR.Gamma(Vp_MAG)
GAM_Ve = SR.Gamma(Ve_MAG)

q_p = -1
q_e = -1
Length_lab = 1
LAM_lab = abs(q_e) / Length_lab
I = - LAM_lab * Ve_MAG                                                         ### minus here? LAM_lab is always possitive due to abs()
dL_lab = Line_Len/ N_Line
Q_dl = dL_lab * LAM_lab                                                        # same as dL_FRMp * LAM_FRMp

E_FRMp_x = np.zeros([N_x])
E_FRMp_y = np.zeros([N_x])
E_FRMp_z = np.zeros([N_x])
print('gammas:',GAM_Ve,GAM_Vp)
print("N_x =",N_x,"N_Line =",N_Line)

############################## Velocity Transform ############################
DOT_UV = np.dot(Vp,Ve)
Vp_FRMe = SR.TRANS_Velocity( Vp, Ve, Ve_MAG, GAM_Ve, DOT_UV)
Vp_FRMe_MAG = Vp_FRMe[2]                                                       # as all velocities in z-direction
GAM_Vp_FRMe = SR.Gamma(Vp_FRMe_MAG)

############################## Numerical Transform ###########################
nansize = 0.0001
E_FRMp_y = np.where(y_data**2 < nansize, np.nan, E_FRMp_y)
CC_dE = SR.CC_dE(LAM_lab)
for i_y in range(N_x):
    y =  0.1 + ( i_y * axis_y ) / ( N_x - 1 )
    y_data[i_y] = y
    #continue###
    for i_dl in range(N_Line):                                                # for each frame we will use lab's time as T_lab = 0
        X_dl_FRMp_z = ( i_dl * Line_Len ) / (N_Line-1) - Line_Len / 2
        Delta_FRMp_MAG = np.sqrt( y**2 + X_dl_FRMp_z**2 )
        cosT_FRMp = - X_dl_FRMp_z / Delta_FRMp_MAG

        ### angles<p> in <ions> and <electrons> ##############################
        cosTi_proper = SR.TRANS_CT( cosT_FRMp , -Vp_MAG )
        cosTe_proper = SR.TRANS_CT( cosT_FRMp , -Vp_FRMe_MAG )

        ### intensity/density weighting ######################################
        dE_MAG = CC_dE * (np.array([0, y, - X_dl_FRMp_z]) / Delta_FRMp_MAG**3)
        dE_FRMp = dE_MAG * ( SR.Relative_FLUX( cosTi_proper , Vp_MAG ) -      \
                             SR.Relative_FLUX( cosTe_proper , Vp_FRMe_MAG) )

        ### Total E-Field ####################################################
        E_FRMp_y[i_y] = E_FRMp_y[i_y] + dE_FRMp[1]
        E_FRMp_z[i_y] = E_FRMp_z[i_y] + dE_FRMp[2]
F_lab_y = ( q_p * E_FRMp_y ) / GAM_Vp
#F_lab_z = ( q_p * E_FRMp_z ) / GAM_Vp  whats the transform of a force paralell????

############################ Beaming force <LAB> #############################
LAM_i_FRMprp = LAM_lab
LAM_e_FRMprp = - LAM_lab / ( GAM_Ve**3 * ( Ve_MAG**2 + 1 ) ) #/ ( ( 1 + Ve_MAG**2 ) * GAM_Ve**3 ))/ GAM_Vp_FRMe  ### or is LAM_e_lab what we should be using in magnetic field equation
E_i_FRMi = SR.E_FIELD_PROPER(LAM_i_FRMprp, y_data, Vp_MAG     , GAM_Vp)
E_e_FRMe = SR.E_FIELD_PROPER(LAM_e_FRMprp, y_data, Vp_FRMe_MAG, GAM_Vp_FRMe)

E_LAB = E_i_FRMi + E_e_FRMe * GAM_Ve
F_LAB = q_p * E_LAB

##################### Beaming force from <particle> ##########################
LAM_i_FRMp = LAM_lab / GAM_Vp
LAM_e_FRMp = - (LAM_lab / ( ( 1 + Ve_MAG**2 ) * GAM_Ve**3 ))/ GAM_Vp_FRMe  ### or is LAM_e_lab what we should be using in magnetic field equation
E_i_FRMp = SR.E_FIELD_PRIME(LAM_i_FRMp, y_data, Vp_MAG     , GAM_Vp)
E_e_FRMp = SR.E_FIELD_PRIME(LAM_e_FRMp, y_data, Vp_FRMe_MAG, GAM_Vp_FRMe)

E_PARTICLE = E_i_FRMp + E_e_FRMp
F_PARTICLE = q_p * E_PARTICLE / GAM_Vp                                       ### will it actually be GAM_Vp or using transform for t_prime = 0 for both

############################### B Force ######################################
B_Field = - I / (2 * np.pi * SR.Eps * y_data)
F_B = q_p * B_Field * Vp_MAG                                                   # check if cross product leads minus sign
F_ratio  = F_PARTICLE[1] / F_B
print("F_E/F_B", F_ratio , "max-min=", (np.max(F_ratio)-np.min(F_ratio))/2)

### PLOTS ####################################################################
plt.figure(1)
plt.title('E_z field')
#plt.plot(y_data,E_FRMp_z, 'x')
plt.plot(y_data,F_PARTICLE[2]/q_p, '.', c='r')
plt.xlabel("distance from wire")
plt.ylabel("E_z ")

plt.figure(2)
plt.title('F_lab_y field')
plt.scatter(y_data,F_lab_y, c=np.sign(F_lab_y), cmap="bwr")
plt.plot(y_data,F_B,'-')
#plt.plot(y_data,F_LAB[1],'x')
plt.plot(y_data,F_PARTICLE[1],'x',c='g')
plt.xlabel("distance from wire")
plt.ylabel("F_y ")

plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))
##############################################################################
########################################################################## END