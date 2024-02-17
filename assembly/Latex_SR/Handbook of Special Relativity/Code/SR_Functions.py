""" Functions for Special Relativity ( c = 1 ) """
import numpy as np

################################# CONSTANTS ##################################

Eps = 8.854 * 10**(-12)
CC = 1 / ( 4 * np.pi * Eps )

def CC_dE(Q_or_Lamda):
    CC_dE = Q_or_Lamda * CC
    return CC_dE

def Beta(V):
    return V

def Gamma(V):
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - V_MAG**2)
    return gamma

def DOT(X,V):
    dot = np.dot(X,V)
    return dot

def Doppler(V_MAG, cos_theta):
    doppler = 1 / ( Gamma(V_MAG) * ( 1 - V_MAG * cos_theta  )  )   
    return doppler


######################## FAST GENERAL TRANSFORMATIONS #############################
def TRANS_3Position_fast(X, T, V_FRM, V_FRM_MAG, gamma, DOT_XV):
    X_prime = X + ( ((gamma-1)/V_FRM_MAG**2) * DOT_XV - gamma * T ) * V_FRM
    return X_prime

def TRANS_Time_fast(X, T, V, gamma, DOT_XV):
    T_prime = gamma * ( T - DOT_XV )
    return T_prime

def TRANS_Velocity_fast(U, V, V_MAG, gamma, DOT_UV):
    CC1 = 1 / (  gamma * ( 1 - DOT_UV )  )
    CC2 = ( ( gamma-1 ) / V_MAG**2 ) * DOT_UV - gamma
    U_prime = CC1 * (U + CC2 * V)
    return U_prime

######################## 1d TRANSFORMATIONS and TIME ################################

def TRANS_1Time(R, V_FRM, T):
    gamma = Gamma(V_FRM)
    T_prime = gamma * ( T - (R * V_FRM) )
    return T_prime

def TRANS_Z(R, V_FRM, T):
    gamma = Gamma(V_FRM)
    R_prime = np.zeros( ( len(R) ) )
    R_prime = R + ( ((gamma-1)/V_FRM**2) * (R*V_FRM) - gamma * T ) * V_FRM
    return R_prime

def TRANS_Z_simul(R, V_FRM, Vp_prime, T): # simultaneous 
    gamma = Gamma(V_FRM)
    R_prime_simul = np.zeros( ( len(R) ) )
    R_prime_simul = R + ( ((gamma-1)/V_FRM**2) * (R*V_FRM) - gamma * T ) * V_FRM + gamma * (R*V_FRM)  * Vp_prime
    return R_prime_simul  

def TRANS_1Velocity(U, V_FRM):
    gamma = Gamma(V_FRM)
    CC1 = 1 / (  gamma * ( 1 - U * V_FRM )  )
    CC2 = ( ( gamma-1 ) / V_FRM**2 ) * (U*V_FRM) - gamma
    U_prime = CC1 * (U + CC2 * V_FRM)
    return U_prime

######################## 3 VEC TRANSFORMATIONS and TIME ################################

def TRANS_Time(R3, V_FRM, T):
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    T_prime = gamma * ( T - np.dot(R3 , V_FRM) )
    return T_prime

def TRANS_3Position(R3, V_FRM, T):
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    R3_prime = np.zeros( ( len(R3) ) )
    R3_prime = R3 + ( ((gamma-1)/V_FRM_MAG**2) * np.dot(R3,V_FRM) - gamma * T ) * V_FRM
    return R3_prime

def TRANS_3Position_simul(R3, V_FRM, Vp_prime, T): # simultaneous 
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    R3_prime_simul = np.zeros( ( len(R3) ) )
    VdotR = np.dot(R3,V_FRM)
    R3_prime_simul = R3 + ( ((gamma-1)/V_FRM_MAG**2) * VdotR - gamma * T ) * V_FRM + gamma * VdotR  * Vp_prime
    return R3_prime_simul  

def TRANS_3Velocity(U3, V_FRM):
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    CC1 = 1 / (  gamma * ( 1 - np.dot(U3,V_FRM) )  )
    CC2 = ( ( gamma-1 ) / V_FRM_MAG**2 ) * np.dot(U3,V_FRM) - gamma
    U3_prime = CC1 * (U3 + CC2 * V_FRM)
    return U3_prime

def TRANS_2Acceleration(a2, U2, V_FRM):
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    Aber = gamma * ( 1 - np.dot(U2,V_FRM) )
    
    a2_prime_y = a2[0] / Aber**2 + ( gamma * np.dot(U2,V_FRM) * a2[1] ) / Aber**3
    a2_prime_z = a2[1] / Aber**3
    a2_prime = np.array([a2_prime_y,a2_prime_z])
    return a2_prime

######################## 4 VEC TRANSFORMATIONS ################################

def TRANS_4Position(R4, V_FRM):
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    R4_prime = np.zeros( ( 3 ) )
    R4_prime[0] = gamma * ( R4[0] - np.dot(R4[1:] , V_FRM) )
    R4_prime[1:] = R4[1:] + ( ((gamma-1)/V_FRM_MAG**2) * np.dot(R4[1:],V_FRM) - gamma * R4[0] ) * V_FRM
    return R4_prime

def TRANS_4Velocity(U4, V, gamma):
    V_MAG = np.linalg.norm(V)
    CC1 = 1 / (  gamma * ( 1 - np.dot(U4[1:],V) )  )
    CC2 = ( ( gamma-1 ) / V_MAG**2 ) * np.dot(U4[1:],V) - gamma
    U_prime = CC1 * (U4 + CC2 * V)
    return U_prime

######################## Multi 4 VEC TRANSFORMATIONS ##########################
def TRANS_Multi_R4(R4, V_FRM):
    V_FRM_MAG = np.linalg.norm(V_FRM)
    gamma = Gamma(V_FRM_MAG)
    R4_prime = np.zeros( ( len(R4) , 3 ) )
    for i in range(len(R4)):
        R4_prime[i,0] = gamma * ( R4[i,0] - np.dot(R4[i,1:] , V_FRM) )
        R4_prime[i,1:] = R4[i,1:] + ( ((gamma-1)/V_FRM_MAG**2) * np.dot(R4[i,1:],V_FRM) - gamma * R4[i,0] ) * V_FRM
    return R4_prime

def TRANS_Multi_V4(U4,R4, V):
    V_MAG = np.linalg.norm(V)
    gamma = Gamma(V_MAG)
    
    U_prime = np.zeros( ( len(U4) , 3 ) )
    for i in range(len(U4)):       
        CC1 = 1 / (  gamma * ( 1 - np.dot(U4[i,1:],V) )  )
        CC2 = ( ( gamma-1 ) / V_MAG**2 ) * np.dot(U4[i,1:],V) - gamma
        U_prime[i,0] = gamma * ( R4[i,0] - np.dot(R4[i,1:] , V ) )
        U_prime[i,1:] = CC1 * (U4[i,1:] + CC2 * V)
    return U_prime


##################### ANGLE TRANSFORMATION OF LIGHT ##########################
def TRANS_CT( COS_THETA, V_MAG ):
    ### particle and frame is in Z_axis, theta being angle from Z axis
    COS_THETA_prime = ( COS_THETA - V_MAG ) / ( 1 - V_MAG * COS_THETA )
    return COS_THETA_prime

def Relative_FLUX(COS_THETA_prime, V_MAG ): ### in non proper frame
    ###  can inverse by using using cos_THETA_proper and -V instead and dividing by expression
    ### could use gamma as the variable instead for when loops are neeeded
    Relative_FLUX = ( 1 + V_MAG * COS_THETA_prime )**2 / ( 1 - V_MAG**2 )
    return Relative_FLUX

####################### WIRE: E_FIELD infinite wire TRANSFORMATION ###########
### for lAB:::
def E_FIELD_LAB(LAM, V, GAM_V, d,Vp_minus, GAM_Vp): # transforms E_field from proper frame for infinite wire
    ### works for proper frame V=0 ### LAM is from non proper frame
    Ey = (2/15)*( 3*V**2*Vp_minus**2 + 5*(V**2 + Vp_minus**2) + 20*V*Vp_minus + 15)
    Ez = np.pi * (Vp_minus + V) * ( 3*Vp_minus*V + 4 ) / 4
    E_prime = LAM * CC * GAM_V**2 * GAM_Vp**2 * np.array([0, Ey / d, Ez / d],
                                dtype=object)
    return E_prime

####################### WIRE: E_FIELD with dopler shift TRANSFORMATION #######
### particle frame:::
def E_FIELD_PROPER(LAM_proper, d, V_MAG, GAM_V): # transforms E_field from proper frame for infinite wire
    ### works for proper frame V=0 ### LAM is from non proper frame
    Ey = 2 * (V_MAG**2 + 1)
    Ez = 0 ### still need to change ####
    E_particle = LAM_proper * CC * GAM_V**3 * np.array([0, Ey / d, Ez / d], dtype=object)
    return E_particle

####################### WIRE: total E_FIELD TRANSFORMATION ###################
### particle frame:::
def E_FIELD_PRIME(LAM_prime, d, V_MAG, GAM_V): # transforms E_field from proper frame for infinite wire
    ### works for proper frame V=0 ### LAM is from non proper frame
    Ey = 2 * (V_MAG**2 + 1)
    Ez = 0 ### still need to change ####
    E_particle = LAM_prime * CC * GAM_V**3 * np.array([0, Ey / d, Ez / d], dtype=object)
    return E_particle

####################### CONTRACTION TRANSFORMATIONS ##########################
def TRANS_Delta_Coords(delta_X, delta_T, V):
    V_MAG = np.linalg.norm(V)
    gamma = Gamma(V)
    CC = ( (gamma-1) / V_MAG**2 ) * np.dot(V,delta_X) - gamma * delta_T
    delta_X_prime = delta_X + CC * V
    return delta_X_prime

def TRANS_Delta_Time(delta_X0, delta_T0, V):
    gamma = Gamma(V)
    T0_prime = gamma * ( delta_T0 - np.dot(V,delta_X0) )
    return T0_prime

##########################

### TESTS ###
# =============================================================================
# X = np.array([1,2,3])
# T = 0
# U = np.array([0.5,0.2,0.2])
# V = np.array([0.3,0.4,0.5])
# V_MAG = V_MAG(V)
# gamma = Gamma(V_MAG)
# DOT_XV = DOT(X,V)
# print(TRANS_Coords(X, T, V, V_MAG, gamma, DOT_XV))
# =============================================================================
