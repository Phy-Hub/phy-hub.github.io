import SR_Functions as SR
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from celluloid import Camera
import time
start_time = time.time()
print("start time = ", time.strftime("%H:%M:%S"))
#Creating matplotlib figure and camera object
fig = plt.figure(frameon=False)
plt.axis('equal')
#plt.axis('off') #plt.axis('square') #fig.patch.set_alpha(0.)
Axis_max = 30
plt.xlim( -10 , 10 )
plt.ylim( -5 , Axis_max )
camera = Camera(fig)
##############################################################################
c = 1
Vp = 0.8
V = np.array([ 0 , - Vp ])
gamma = SR.Gamma(V)

runtime = 10 # must be interger # 12
framerate = 2#10
N_t = framerate * runtime # number of time steps
N_ang = 6 # even number of angles

C       =  np.empty( ( N_ang, 2 ) )
C_PRM   =  np.empty( ( N_ang, 2 ) )
doppler =  np.empty( ( N_ang ) )
ang = np.linspace( np.pi/N_ang , 2*np.pi - np.pi/N_ang , N_ang)

cm = mpl.cm.rainbow
sc = 0.7 # arrow scale        
###############################################################################
### retarded ###
#Looping the data and capturing frame at each iteration
for I_a in range(N_ang):
    C[I_a]       = c * np.array([  np.sin(ang[I_a]) ,  np.cos(ang[I_a]) ])
    C_PRM[I_a]   = SR.TRANS_3Velocity( C[I_a], V )    
    doppler[I_a] = SR.Doppler(V[1], C_PRM[I_a,1])

N_R = 3
R_range = 10
Ry = np.linspace(  -R_range/2 , R_range/2 , N_R)
Rz = np.linspace(  0 , R_range , N_R)

Rs = np.empty( ( N_R*N_R, 2 ) )
for i in range(N_R):
    for j in range(N_R):
        Rs[i*N_R + j] = np.array([Ry[i],Rz[j]])

dt = (1 / framerate)
for I_t in range(N_t):      
    t = I_t * dt
       
    for I_s in range(len(Rs)):
        Rs_PRM_pulseEvent = SR.TRANS_3Position(Rs[I_s], V, 0)
        Rs_PRM = SR.TRANS_3Position_simul(Rs[I_s], V, -V, t)
        for I_a in range(N_ang):
                                   
            Rc     = Rs[I_s] + I_t * C[I_a] * dt 
            Rc_PRM = SR.TRANS_3Position_simul(Rc, V, C_PRM[I_a], t)             
        
            if ( np.dot( C[I_a] , Rc_PRM - Rs_PRM[:] ) < 0 ):
                Rc_PRM[:] = np.nan
                    
            plt.quiver(Rc_PRM[0], Rc_PRM[1], sc * C_PRM[I_a,0], sc * C_PRM[I_a,1], 
                    angles="xy" , zorder=1, pivot="mid",
                    alpha=0.5,width=0.005, scale=5, scale_units='inches', animated=True,
                    color=cm(doppler[I_a])) 
        # source:
        plt.scatter( Rs_PRM_pulseEvent[0] , Rs_PRM_pulseEvent[1] , color = 'grey' , s = 30, animated=True, alpha=0.5)
        plt.scatter( Rs_PRM[0] , Rs_PRM[1] , color = 'black' , s = 30, animated=True)
        
    camera.snap()       
###############################################################################    
plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))
