""" E-Field immeadiatly after transform to primed frame """

### Questions, how does the field now propegate from each point now?
###            must be able to transform each point later in time back to proper frame

import SR_Functions as SR
import matplotlib.pyplot as plt
import numpy as np

N_Y = 12
N_Z = 12
N_THETA = 1000 #even # time taken is linearly increased

NANSIZE = 0.2
RADIUS = 2
AXIS_Y = 3
AXIS_Z = 3

V = 0.9
c=1

uu = np.linspace(-AXIS_Y, AXIS_Y, N_Y)
vv = np.linspace(-AXIS_Z, AXIS_Z, N_Z)
y_p,z_p = np.meshgrid(uu, vv)
R_xy = np.sqrt(z_p*z_p + y_p*y_p)

Cos = z_p / R_xy
Sin = y_p / R_xy

GAM = SR.Gamma(V)

### proper transform field
z_p_proper = z_p
Uy = y_p        / np.sqrt( y_p**2 + z_p_proper**2 )
Uz = z_p_proper / np.sqrt( y_p**2 + z_p_proper**2 )
U_prime_y = Uy                   /  ( GAM * ( 1 - V * Uz ) )
U_prime_z = ( GAM * ( Uz - V ) ) /  ( GAM * ( 1 - V * Uz ) )

### retarded field
CC = GAM**2 * (V**2/c**2)
PP_z = z_p + CC * ( z_p + np.sqrt(z_p**2 +(y_p**2 + z_p**2)/CC))
cos_ret = PP_z / np.sqrt(PP_z**2 + y_p**2)
sin_ret = np.sign(y_p) * np.sqrt(1 - cos_ret**2)

### Transforming angle of propagating wave at each point #####################
Cos_PRM = SR.TRANS_CT(Cos, -V)
Sin_PRM = np.sign(y_p) * np.sqrt( 1 - Cos_PRM**2 )

### transforming Z-Coordinates ###############################################
z_p_PRM = SR.TRANS_Coords(z_p, 0, V, V, GAM, z_p*0.9)

### RETARDED FIELD ###########################################################
CC = 1- V**2
z = z_p
z_p = z_p  ###### /GAM why??????????????

t = - z_p*V/CC - np.sqrt( (V**2 * z_p**2)/CC**2 + (y_p**2 + z_p**2)/CC )
CT = (z_p - V * t) / np.sqrt(y_p**2 + (z_p - V * t)**2)
ST = np.sign(y_p) * np.sqrt( 1 - CT**2 )
##############################################################################

plt.figure(1,figsize=(7,7))
plt.title('Direction of E-field in primed frame')
plt.quiver(y_p,z_p_PRM,Sin_PRM,Cos_PRM)
plt.quiver(y_p,-z_p_PRM,U_prime_y,-U_prime_z, color='r')
plt.xlabel(r'$ Y\langle prime \rangle $')
plt.ylabel(r'$ Z\langle prime \rangle $')
plt.plot(0,0,'ro', markersize=12)
plt.quiver(0,0,0,1,scale=0.5, scale_units = 'xy',color='r')
#plt.axis('equal')

plt.figure(2,figsize=(7,7))
plt.title('Direction of Retarded E-field in primed frame')
plt.quiver(y_p,z_p_PRM,ST,CT)
plt.quiver(y_p,z_p_PRM,sin_ret,cos_ret, color='r')
plt.xlabel(r'$ Y\langle prime \rangle $')
plt.ylabel(r'$ Z\langle prime \rangle $')
plt.plot(0,0,'ro', markersize=12)
plt.quiver(0,0,0,1,scale=0.5, scale_units = 'xy',color='r')

plt.show()