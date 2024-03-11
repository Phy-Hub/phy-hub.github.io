""" E-Field immeadiatly after transform to primed frame """

### Questions, how does the field now propegate from each point now?
###            must be able to transform each point later in time back to proper frame

import SR_Functions as SR
import matplotlib.pyplot as plt
import numpy as np

NN =15 #315
N_Y = NN
N_Z = NN

NANSIZE = 0.1
RADIUS = 2
AXIS_Y = 4
AXIS_Z = 3

V = -0.9
Vp_prime = -V
c=1

uu = np.linspace(-AXIS_Y, AXIS_Y, N_Y)
vv = np.linspace(-AXIS_Z, AXIS_Z, N_Z)
y_p_prime,z_p_prime = np.meshgrid(uu, vv)
y_p_prime = np.where(y_p_prime**2+z_p_prime**2<NANSIZE, np.nan , y_p_prime) # ==0

GAM = SR.Gamma(V)

### proper transform field
z_p_proper = z_p_prime * GAM                                                   ### this is because all times in LAB/prime are = 0
y_p_proper = y_p_prime
Uy = y_p_proper   / np.sqrt( y_p_proper**2 + z_p_proper**2 )
Uz = z_p_proper   / np.sqrt( y_p_proper**2 + z_p_proper**2 )
U_prime_y = Uy                   /  ( GAM * ( 1 - V * Uz ) )
U_prime_z = ( GAM * ( Uz - V ) ) /  ( GAM * ( 1 - V * Uz ) )

R_MAG = np.sqrt( y_p_prime**2 + GAM**2 * z_p_prime**2 )
f = GAM * ( 1 - (V/c) * ( GAM * z_p_prime / R_MAG ) ) / (R_MAG**2)
R_MAG = np.sqrt( y_p_proper**2 + z_p_proper**2 )
f = GAM * ( 1 - (V/c) * ( z_p_proper / R_MAG ) ) / (R_MAG**2)


# =============================================================================
# ### retarded field
# alpha = z_p_prime * Vp_prime * GAM**2
# t_prime = - (  alpha + np.sqrt(alpha**2 + GAM**2 * (y_p_prime**2 + z_p_prime**2)) )
# z_ret = z_p_prime - Vp_prime * t_prime
#
# ret_mag = np.sqrt( y_p_prime**2 + z_ret**2 )
# y_hat = y_p_prime / ret_mag
# z_hat = z_ret / ret_mag
# 
# R = (y_p_prime**2 + z_p_prime**2)**(-0.0001)
# R = R.reshape(N_Y*N_Z)
# =============================================================================

### PLOTS ###
plt.figure(1)
plt.title('Field Propagation Direction in Charges Primed Frame')
#plt.quiver(y_p_prime,z_p_prime,y_hat,z_hat)#,R,cmap='autumn', color='r')
plt.quiver(y_p_prime,z_p_prime,U_prime_y,U_prime_z)#,f,cmap='jet')
plt.xlabel(r"$y'$")
plt.ylabel(r"$z'$")
plt.plot(0,0,'ro', markersize=7)
plt.quiver(0,0,0,Vp_prime,scale=1, scale_units = 'xy',color='r',headwidth=3.5,width=0.008)
#plt.axis('equal')
plt.savefig("output/Field_Directions_Aberrated.pdf")

plt.figure(2,figsize=(7,7))
plt.title('Direction of Propagating (-c) E-field in Frame with a Dynamic Charge')
#plt.quiver(y_p_prime,z_p_prime,-y_hat,-z_hat)#,R,cmap='autumn', color='r')
plt.quiver(y_p_prime,z_p_prime,-U_prime_y,-U_prime_z)
plt.xlabel(r'$ Y\langle d \rangle $')
plt.ylabel(r'$ Z\langle d \rangle $')
plt.plot(0,0,'ro', markersize=12)
plt.quiver(0,0,0,Vp_prime,scale=1, scale_units = 'xy',color='r')
#plt.axis('equal')

plt.figure(3)
plt.title('Field Strength' )
plt.contour( y_p_prime, z_p_prime, f, 200, cmap= 'jet')
plt.colorbar()
plt.xlim([-AXIS_Y, AXIS_Y])
plt.ylim([-AXIS_Z, AXIS_Z])

plt.figure(4)
plt.axis('off')
plt.quiver(y_p_prime,z_p_prime,U_prime_y,U_prime_z)#,f,cmap='jet')
plt.plot([0,0], [3.1,-3.1], '.', alpha=0)


plt.savefig("output/Pic_Field_Directions_Aberrated.pdf", bbox_inches='tight', format='pdf',transparent=True) # format='svg'

plt.show()