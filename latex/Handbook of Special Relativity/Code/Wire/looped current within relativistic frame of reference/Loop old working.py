# remember that this is still in the relativistic frame at the moment
# is there relativistic affects due to accelleration?
from Coordinate_Transforms import (Gamma, TRANS_Coords, TRANS_Time,
                                   TRANS_Velocity)
import matplotlib.pyplot as plt 
import numpy as np
import time
start_time = time.time()
##############################################################################
### Constants ###
save = 0
n=100 # even
m = 1000 #even
if 1 > 0:
    Radius = 2
    axis = 3
    Eps0 = 8.854 * 10**(-12)
    zrange = 10
    q_p = -1
    q_e = -1
    c = 1
    Vp_MAG = 0.99#99 # in y direction
    Ve_MAG = 0.3 # magnitude only
    Vp = np.array([0, Vp_MAG, 0])
    L_lab = 1
    LAM_lab = q_e / L_lab ### what lenght is l_lab?
    gamma_Vp = Gamma(Vp_MAG)
    gamma_Ve = Gamma(Ve_MAG)
    ####### should it not be the Vp and Ve vectors or is that used later
    CC_LAM = LAM_lab * gamma_Vp * Vp_MAG * Ve_MAG / (c**2)
    CC_dQ = CC_LAM * Radius
    CC_dE_rel = 1 / (4 * np.pi * Eps0) 
    CC_dE = CC_dQ * CC_dE_rel
    I = Ve_MAG * LAM_lab ####### change to same for relativistic Version
    Mu0 = 1 / (Eps0 * c**2)
    CC_BF = (Mu0 * I * Radius) / (4 * np.pi)
    
    ##############################################################################
    ### Dimension and Iteration Setup ###
    l = 1 #odd
    dtheta = (2 * np.pi) / (m-1)
    rxdata = np.zeros((m,1))
    rydata = np.zeros((m,1))
    rpxdata = np.zeros((m,1))
    rpydata = np.zeros((m,1))
    rexdata = np.zeros((m,1))
    reydata = np.zeros((m,1))
    ratomxdata = np.zeros((m,1))
    ratomydata = np.zeros((m,1))
    
    uu = vv = np.linspace(-axis, axis, n)
    x_p,y_p = np.meshgrid(uu, vv)
    R_xy = np.sqrt(x_p*x_p + y_p*y_p)
        
    E_TotalMagnitude = np.zeros([n,n])
    E_x = np.zeros([n,n])
    E_y = np.zeros([n,n])
    E_z = np.zeros([n,n])
    dB_z = np.zeros([n,n])
    dB_y = np.zeros([n,n])
    dB_x = np.zeros([n,n])
    B_x = np.zeros([n,n])
    B_y = np.zeros([n,n])
    B_z = np.zeros([n,n])
    F_B_x = np.zeros([n,n])
    F_B_y = np.zeros([n,n])
    F_B_z = np.zeros([n,n])
    
##############################################################################
### Calculations ###
for j in range(l):
    if l == 1:
        Z = 0
    else:
        Z =  zrange * (2*(j)/(l-1) - 1) 
    #print(Z)
    for i in range(m):
        theta = i * dtheta # point on ring's theta
        CT = np.cos(theta)
        ST = np.sin(theta)
        
        # displacement from ring 
        ############## need to change S_ into p frame later!!!!!!!!!!!!!!!!!!!
        S_x = x_p - Radius * CT
        S_y = y_p - Radius * ST
        S_z = -Z
        
        # points distance from ring
        S_MAG = np.sqrt( S_x*S_x + S_y*S_y + S_z*S_z )
        
        cos_Zangle = S_z / S_MAG
        sin_Zangle = np.sqrt(1 - cos_Zangle*cos_Zangle)
        
        dE_x = CC_dE * ( S_x * CT ) / S_MAG**3 * dtheta / sin_Zangle
        dE_y = CC_dE * ( S_y * ST ) / S_MAG**3 * dtheta / sin_Zangle
        if S_z !=0:
            dE_z = CC_dE * CT * dtheta * cos_Zangle / S_MAG**2
        else:
            dE_z = 0
          
        E_x = E_x + dE_x
        E_y = E_y + dE_y
        E_z = E_z + dE_z
        
        ######################################################################
        ######################################################################
        ### B Field ###
        # B field with use of  dl x S cross product 
        dB_x = CC_BF * dtheta * (CT * S_z) / S_MAG**3
        dB_y = CC_BF * dtheta * (ST * S_z) / S_MAG**3
        dB_z = CC_BF * dtheta * (- ST * S_y - CT * S_x) / S_MAG**3
        B_x = B_x + dB_x
        B_y = B_y + dB_y
        B_z = B_z + dB_z      
        
        ######################################################################
        ######################################################################
        ### Vector transforms ###
        T = 0        
        R  = np.array([Radius * CT,  Radius * ST, 0])
        Ve = np.array([- Ve_MAG * ST, Ve_MAG * CT,0])

        ### current loop element's position in frame of current element ### checked
        ### this should be same position r_x, r_y as velocity is perpendicular to position vector        
        R_FRMe = TRANS_Coords(R,T,Ve)
        T_FRMe = TRANS_Time(R,T,Ve)
        
        ### Electron Frame: velocity of particle ### checked
        Vp_FRMe = TRANS_Velocity(Vp,Ve)
        
        ### Particle Frame: position of length element ### 
        Vep_sq = np.linalg.norm(Vp_FRMe)**2
        if Vep_sq < 10**-10:
            Vep_sq = np.nan 
        else:
            R_FRMp = TRANS_Coords(R_FRMe,T_FRMe,Vp_FRMe)
            T_FRMp   = TRANS_Time(R_FRMe,T_FRMe,Vp_FRMe)
 
        rxdata[i,0] = R[0]
        rydata[i,0] = R[1]
        rpxdata[i,0] = R_FRMp[0]
        rpydata[i,0] = R_FRMp[1]
        rexdata[i,0] = R_FRMe[0]
        reydata[i,0] = R_FRMe[1]
        ratomxdata[i,0] = R[0]
        ratomydata[i,0] = gamma_Vp * R[1] 
        
E_TotalMag = np.sqrt(E_x*E_x + E_y*E_y + E_z*E_z)

F_B_x = q_p * (Vp[1]*B_z - Vp[2]*B_y)
F_B_y = q_p * (Vp[2]*B_x - Vp[0]*B_z) # remember V is in terms of C
F_B_z = q_p * (Vp[0]*B_y - Vp[1]*B_x)

##############################################################################
### nan large E values ###
if 1 > 0:
    nansize = 0.1
    #if Z < nansize:
    E_xnan = np.where(R_xy < Radius + nansize, np.nan, E_x)
    E_x = np.where(R_xy < Radius - nansize, E_x, E_xnan)
    E_ynan = np.where(R_xy < Radius + nansize, np.nan, E_y)
    E_y = np.where(R_xy < Radius - nansize, E_y, E_ynan)
    #E_znan = np.where(R_xy < Radius + nansize, np.nan, E_z)
    #E_z = np.where(R_xy < Radius - nansize, E_z, E_znan)
    E_TotalMagnan = np.where(R_xy < Radius + nansize, np.nan, E_TotalMag)
    E_TotalMag = np.where(R_xy < Radius - nansize, E_TotalMag, E_TotalMagnan)
    
    B_znan = np.where(R_xy < Radius + nansize, np.nan, B_z)
    B_z = np.where(R_xy < Radius - nansize, B_z, B_znan)
    F_B_znan = np.where(R_xy < Radius + nansize, np.nan, F_B_z)
    F_B_z = np.where(R_xy < Radius - nansize, F_B_z, F_B_znan)
    F_B_ynan = np.where(R_xy < Radius + nansize, np.nan, F_B_y)
    F_B_y = np.where(R_xy < Radius - nansize, F_B_y, F_B_ynan)
    F_B_xnan = np.where(R_xy < Radius + nansize, np.nan, F_B_x)
    F_B_x = np.where(R_xy < Radius - nansize, F_B_x, F_B_xnan)
    
##############################################################################
### Change of Coordinates ###
if 1 < 0:      
    #R_xy = np.where(R_xy < nansize, np.nan, R_xy)
    # 
    # phi = np.arccos(E_x/E_TotalMagnitude)
    # psi = np.arccos(x_p / R_xy)
    # angle = phi - psi
    # 
    # E_R =       E_TotalMagnitude * np.cos(angle) 
    # E_theta =   E_TotalMagnitude * np.sin(angle) 
    # 
    # diff = np.sqrt(E_R**2 + E_theta**2) - E_TotalMagnitude
    print("meow")
##############################################################################

### Save Files ###
if save == 1:
    np.savetxt("./Save files/x_p.txt", x_p)
    np.savetxt("./Save files/y_p.txt", y_p)
    np.savetxt("./Save files/E_x.txt", E_x)
    np.savetxt("./Save files/E_y.txt", E_y) #E_x = np.loadtxt("E_x.txt")
    np.savetxt("./Save files/E_z.txt", E_z)
    np.savetxt("./Save files/B_x.txt", B_x)
    np.savetxt("./Save files/B_y.txt", B_y)
    np.savetxt("./Save files/B_z.txt", B_z)
##############################################################################
### PLOT ###

plt.figure(1, figsize=(15,6))
plt.subplot(121)
plt.title('E_x' )
plt.contourf(x_p,y_p, E_x, 100, cmap= 'bwr')
plt.colorbar() #plt.ylim(-5, 5)

plt.subplot(122)
plt.title('E_y')
plt.contourf(x_p,y_p, E_y, 100, cmap= 'bwr')
plt.colorbar() #plt.ylim(-5, 5)

plt.figure(2)
plt.title('E_Total')
plt.contourf(x_p,y_p, E_TotalMag, 100, cmap= 'bwr')
plt.colorbar() #plt.ylim(-5, 5)

plt.figure(3) 
plt.title('B_z')
plt.contourf(x_p,y_p, B_z, 100, cmap= 'bwr')
plt.colorbar()

plt.figure(4)
plt.title('loops in different frames')
plt.plot(rxdata, rydata, '.', label="Electons FRMlab")
#plt.plot(rexdata, reydata, label="Electons FRMe")
plt.plot(rpxdata, rpydata, '.', label="Electons FRMp")
plt.plot(ratomxdata, ratomydata, '.', label="Atoms FRMp")
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='best')

plt.figure(5)
plt.title('F_B_x' )
plt.contourf(x_p,y_p, F_B_x, 100, cmap= 'bwr')
plt.colorbar() #plt.ylim(-5, 5)



print(" Run time: %s seconds" % (time.time() - start_time))

#waste
if 1 < 0:
    # =============================================================================
    # nan large E values 
    #for i in range(len(R_xy)):
    #       for j in range(len(R_xy[i])):
    #           if Radius-0.1 < R_xy[i,j] < Radius+0.1:
    #               E_x[i,j] = E_y[i,j] = np.nan
    # =============================================================================
    
    # =============================================================================
    #         ### LENGTH ELEMENTS ###
    #         ### LAB Frame: general length element ### 
    #         L0lab_x = - L_lab * ST
    #         L0lab_y =   L_lab * CT
    #         L0lab_z =   0
    #         L0_x = L0lab_x / gamma_Ve
    #         L0_y = L0lab_y / gamma_Ve
    #         L0_z = 0
    #         
    #         ### Particle Frame: electron's length element ###
    #         L0DOTVp_FRMe = L0_x*Vp_FRMe_x + L0_y*Vp_FRMe_y + L0_z*Vp_FRMe_z
    #         CC_L0e = ( gamma_Vep - 1 ) / Vep_sq - gamma_Vep / c**2
    #         L0e_FRMp_x = L0_x + ( CC_L0e * L0DOTVp_FRMe ) * Vp_FRMe_x
    #         L0e_FRMp_y = L0_y + ( CC_L0e * L0DOTVp_FRMe ) * Vp_FRMe_y
    #         L0e_FRMp_z = L0_z + ( CC_L0e * L0DOTVp_FRMe ) * Vp_FRMe_z
    #         L0e_FRMp_MAG = np.sqrt( L0e_FRMp_x**2 + L0e_FRMp_y**2 + L0e_FRMp_z**2 )
    #         
    #         ### Particle Frame: atom's length element ###
    #         L0DOTVp = L0_x*Vp_x + L0_y*Vp_y + L0_z*Vp_z
    #         CC_L0a = ( gamma_Vp - 1 ) / Vp_MAG**2 - gamma_Vp / c**2
    #         L0a_FRMp_x = L0lab_x + ( CC_L0a * L0DOTVp ) * Vp_x
    #         L0a_FRMp_y = L0lab_y + ( CC_L0a * L0DOTVp ) * Vp_y
    #         L0a_FRMp_z = L0lab_z + ( CC_L0a * L0DOTVp ) * Vp_z
    #         L0a_FRMp_MAG = np.sqrt( L0a_FRMp_x**2 + L0a_FRMp_y**2 + L0a_FRMp_z**2 )        
    #         
    #         ### LAMBDA CALCULATIONS (particle frame) ### 
    #         LAMe_FRMp = ( L_lab / L0e_FRMp_MAG ) * LAM_lab
    #         LAMa_FRMp = - ( L_lab / L0a_FRMp_MAG ) * LAM_lab
    #         
    #         ### CHARGE ELEMENT (particle's frame) ###
    #         dL_FRMp = dL * ( L0a_FRMp_MAG / L_lab )
    #         ########## should i not keep dQ seperate as they have different locations in _FRMp       
    #         ######### check if you can get negative dQ
    #         dQ = dL_FRMp * ( LAMe_FRMp + LAMa_FRMp )
    #         dQa = 00000000
    #         
    #         ### E-FIELD ELEMENT (particle frame) ### 
    #         dE_rel_x = CC_dE_rel * dQ * (S_x / S_MAG**3) 
    #         dE_rel_y = CC_dE_rel * dQ * (S_y / S_MAG**3) 
    #         if S_z !=0:
    #             dE_rel_z = CC_dE_rel * dQ * (S_z / S_MAG**3)
    #         else:
    #             dE_rel_z = 0 
    #         
    #         E_rel_x = E_rel_x + dE_rel_x
    #         E_rel_y = E_rel_y + dE_rel_y
    #         E_rel_z = E_rel_z + dE_rel_z
    # =============================================================================
    
    # =============================================================================
    # E_rel_MAG = np.sqrt(E_rel_x*E_rel_x + E_rel_y*E_rel_y + E_rel_z*E_rel_z)
    # =============================================================================
    
    # =============================================================================
    # E_rel_MAG_nan = np.where(R_xy < Radius + nansize, np.nan, E_rel_MAG)
    # E_rel_MAG = np.where(R_xy < Radius - nansize, E_rel_MAG, E_rel_MAG_nan)
    # =============================================================================
    print("meow")