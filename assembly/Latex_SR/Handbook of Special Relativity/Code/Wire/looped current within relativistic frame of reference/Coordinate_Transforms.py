### Lorentz Transforms ###
# for Transforming general Position, X, Time, T, and Velocity, U, 
# to a Frame with Relative Velocity, V
# X, U, and V may be 3 dimensional vectors

import numpy as np

def Gamma(V):
    c = 1
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - (V_MAG/c)**2)
    return gamma
    
def TRANS_Coords(X, T, V):
    c = 1
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - (V_MAG/c)**2)
    X_prime = X + ( ((gamma-1)/V_MAG**2) * np.dot(V,X) - gamma * T ) * V
    return X_prime

def TRANS_Time(X, T, V):
    c = 1
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - (V_MAG/c)**2)
    T_prime = gamma * ( T - np.dot(V,X)/c**2 )
    return T_prime

def TRANS_Velocity(U, V):
    c = 1
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - (V_MAG/c)**2)
    CC1 = 1 / (  gamma * ( 1 - ( np.dot(U,V) / c**2 ) )  )
    CC2 = ( (gamma-1) / V_MAG**2 ) * np.dot(U,V) - gamma
    U_prime = CC1 * (U + CC2 * V)
    return U_prime

def TRANS_Delta_Coords(delta_X, delta_T, V):
    c = 1
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - (V_MAG/c)**2)
    CC = ( (gamma-1) / V_MAG**2 ) * np.dot(V,delta_X) - gamma * delta_T 
    delta_X_prime = delta_X + CC * V
    return delta_X_prime

def TRANS_Delta_Time(delta_X0, delta_T0, V): 
    c = 1
    V_MAG = np.linalg.norm(V)
    gamma = 1/ np.sqrt(1 - (V_MAG/c)**2)
    T0_prime = gamma * ( delta_T0 - np.dot(V,delta_X0)/c**2 )
    return T0_prime