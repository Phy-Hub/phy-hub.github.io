"""
could change to thin dots instead of arrows with smaller time
between emanating pulses and maybe add arrows after
( could also make line larger at points of high radial density)
"""
import Paths as path
import SR_Functions as SR
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
start_time = time.time()
print("start time = ", time.strftime("%H:%M:%S"))
# Creating matplotlib figure object ###########################################
lim = 10
def PlotStyle():
    #plt.figure(frameon=False)
    plt.axis('equal')
    plt.axis('off')
    plt.axis('square')
    plt.xlim([-lim, lim])
    plt.ylim([-lim,lim])
###############################################################################
c = 1
U_prm_z = 0.9
U_prm = np.array([0,-U_prm_z])
gamma = 1 / np.sqrt(  1 - ( U_prm_z/c )**2  )

N_t = 100 # 40 #number of time steps # not number of arrows
T_step = 44/N_t
N_ang = 70 # even
ang = np.linspace( np.pi/N_ang , 2*np.pi - np.pi/N_ang , N_ang)

###############################################################################
C_wave      =  np.empty( ( N_ang, 2 ) )
C_wave_prm  =  np.empty( ( N_ang, 2 ) )
doppler     =  np.empty( ( N_ang ) )
Rc          =  np.empty( ( N_t, N_ang , 2 ) )
Rc_prm      =  np.empty( ( N_ang , 2 ) )
###############################################################################
#Looping the data
sc = 0.7 #arrow scale
cm = mpl.cm.rainbow

for i in range(len(ang)):
    C_wave[i]       = np.array([ np.sin(ang[i]) , np.cos(ang[i]) ])
    C_wave_prm[i,:] = SR.TRANS_3Velocity( C_wave[i], U_prm )
    doppler[i]      = SR.Doppler(U_prm[1], C_wave_prm[i,1])

###############################################################################

### escape velocities

### patch .....

R_escape =  np.empty( ( N_t, N_ang , 2 ) )

plt.figure(4,frameon=False)
PlotStyle()

u_escape     = # np.empty( ( N_ang, 2 ) ) ############# need u escape

for I_t in range(N_t):
    R_escape[I_t] = I_t * T_step  * C_wave

    for I_ang in range(N_ang):
        if R_escape[I_t,I_ang,0]**2 < (lim + 0.3)**2 and Rc[I_t,I_ang,1]**2 < (lim + 0.3)**2:
                plt.quiver(R_escape[I_t,I_ang,0], R_escape[I_t,I_ang,1], sc * C_wave[I_ang,0], sc * C_wave[I_ang,1],
                        angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005, scale=5,
                        scale_units='inches', color='red') #,headwidth=1)


### patch ....



###############################################################################
plt.figure(1,frameon=False)
PlotStyle()
for I_t in range(N_t):
    Rc[I_t] = I_t * T_step  * C_wave

    for I_ang in range(N_ang):
        if Rc[I_t,I_ang,0]**2 < (lim + 0.3)**2 and Rc[I_t,I_ang,1]**2 < (lim + 0.3)**2:
                plt.quiver(Rc[I_t,I_ang,0], Rc[I_t,I_ang,1], sc * C_wave[I_ang,0], sc * C_wave[I_ang,1],
                        angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005, scale=5,
                        scale_units='inches', color='red') #,headwidth=1)
plt.scatter( 0 ,0, color = 'black' , s = 30, animated=True)

plt.savefig(path.svg +"Field_Rest_Frame.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf +"Field_Rest_Frame.pdf",bbox_inches='tight', format='pdf',transparent=True)
###############################################################################
plt.figure(2,frameon=False)
PlotStyle()

for I_t in range(N_t):
    for I_ang in range(N_ang):
        Rc_prm[I_ang] = SR.TRANS_3Position_simul(Rc[I_t,I_ang,:], U_prm, C_wave_prm[I_ang], 0)

        if Rc_prm[I_ang,0]**2 < (lim + 0.3)**2 and Rc_prm[I_ang,1]**2 < (lim + 0.3)**2:
                plt.quiver(Rc_prm[I_ang,0], Rc_prm[I_ang,1], sc * C_wave_prm[I_ang,0], sc * C_wave_prm[I_ang,1],
                        angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005, scale=5,
                        scale_units='inches', color=cm(doppler[I_ang]))
    if U_prm_z * I_t < lim and U_prm_z * I_t > 0:
        plt.plot(0, - U_prm_z * I_t, marker='o', color='gray', linestyle='none',ms=1)

plt.scatter( 0 ,0, color = 'black' , s = 30, animated=True)
plt.quiver(0, 0.5, 0, 1, angles="xy", pivot="mid", width=0.008, scale=4,
           scale_units='inches', color='black' , headwidth=4)

plt.savefig(path.svg +"Field_Moving_Frame_Doppler.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf +"Field_Moving_Frame_Doppler.pdf",bbox_inches='tight', format='pdf',transparent=True)
###############################################################################
plt.figure(3,frameon=False)
PlotStyle()

for I_t in range(N_t):
    for I_ang in range(N_ang):
        Rc_prm[I_ang] = SR.TRANS_3Position_simul(Rc[I_t,I_ang,:], U_prm, C_wave_prm[I_ang], 0)

        if Rc_prm[I_ang,0]**2 < (lim + 0.3)**2 and Rc_prm[I_ang,1]**2 < (lim + 0.3)**2:
                plt.quiver(Rc_prm[I_ang,0], Rc_prm[I_ang,1], sc * C_wave_prm[I_ang,0], sc * C_wave_prm[I_ang,1],
                        angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005, scale=5,
                        scale_units='inches', color=cm(doppler[I_ang]))

    if U_prm_z * I_t < lim and U_prm_z * I_t > 0:
        plt.plot(0, - U_prm_z * I_t, marker='o', color='gray', linestyle='none',ms=1)

for I_t in range(N_t):
    circle = plt.Circle((0, - U_prm_z * I_t),  c * I_t  , color='black', fill=False)
    plt.gca().add_patch(circle)

plt.scatter( 0 ,0, color = 'black' , s = 30, animated=True)
plt.quiver(0, 0.5, 0, 1, angles="xy", pivot="mid", width=0.008, scale=4,
           scale_units='inches', color='black' , headwidth=4)

plt.savefig(path.svg +"Field_Moving_Frame_Doppler_circles.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf +"Field_Moving_Frame_Doppler_circles.pdf",bbox_inches='tight', format='pdf',transparent=True)
###############################################################################

# fig = plt.figure(4, figsize =(18, 8),frameon=False)
# ax = fig.add_subplot(111)

# # Plotting the streamlines with
# # proper color and arrow
# #color = 2 * np.log(np.hypot(Ex, Ey))
# nx, ny = 8, 8
# x = np.linspace(-2, 2, nx)
# y = np.linspace(-2, 2, ny)
# X, Y = np.meshgrid(x, y)

# sin = gamma * X / np.sqrt(X**2 + Y**2)
# cos = gamma * Y / np.sqrt(X**2 + Y**2)
# cos_prm = 0
# Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))

# print(cos)

# ax.streamplot(x, y, sin, cos, #color = color,
#               linewidth = 1, cmap = plt.cm.inferno,
#               density = 2, arrowstyle ='->',
#               arrowsize = 1.5)

# #ax.add_artist(Circle((0,0), 0.05, color = "black"))

# ax.set_xlabel('X-axis')
# ax.set_ylabel('X-axis')
# ax.set_xlim(-2, 2)
# ax.set_ylim(-2, 2)
# ax.set_aspect('equal')
# ax.set_axis_off()

print(" Run time: %s seconds" % (time.time() - start_time))
plt.show()