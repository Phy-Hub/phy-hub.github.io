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
plt.axis('off') #plt.axis('square') #fig.patch.set_alpha(0.)
Axis_max = 30
plt.xlim( - 5 , 5 )
plt.ylim( -4 , Axis_max )
camera = Camera(fig)
##############################################################################
Theta_init = np.pi/2
radi = 3
Vp_MAG = 0.99
period = 2 * np.pi * radi / Vp_MAG


c = 1
V = np.array([ 0 , -0.9 ])
beta = - V[1]
gamma = 1 / np.sqrt(  1 - ( V[1]/c )**2  )

runtime = 30 # must be interger # 12
framerate = 2#10
N_t = framerate * runtime # number of time steps

Rp_PRM  =  np.empty( ( N_t , 2 ) ) 
Rp_PRM.fill(np.nan)


#Vp_PRM = SR.TRANS_3Velocity( Vp, V )
#doppler  = SR.Doppler(V[1], Vp_PRM[1])
Vp_PRM = np.array([ 0 , 0 ]) #############################
doppler = SR.Doppler(V[1], Vp_PRM[1]) #######################



cm = mpl.cm.rainbow
sc = 0.7 # arrow scale        
###############################################################################
### retarded ###
#Looping the data and capturing frame at each iteration
dt = (1 / framerate)
#T_PRM_diff = gamma * beta * z2 
for i in range(N_t):       
    for m in range(N_t): 
        t_PRM = m / framerate
        if (m <= i):  ## make == if only want 1 arrow
                        
            theta = (m/framerate) * 2 * np.pi / period  +  np.pi/2 # gamma * (m/framerate) ??? #### this proper theta is dependant on primed time... # or is this the theta corresponding to this primed position
            t = t_PRM/gamma + V[1] * radi * np.cos(theta) ## can it be got from circular motion formula??
            Vp = Vp_MAG * np.array([ np.cos(theta) , - np.sin(theta) ])
            Vp_PRM = SR.TRANS_3Velocity(Vp, V)

            Rp_PRM[m] =  np.array([ radi * np.sin(theta)  , gamma * (radi * np.cos(theta) - V[1]* t )  ]) ### later t is used after itteration hence arrows move with circle
            
            doppler = SR.Doppler(V[1], Vp_PRM[1])

            plt.quiver(Rp_PRM[m,0], Rp_PRM[m,1] , sc * Vp_PRM[0], sc * Vp_PRM[1], 
                angles="xy" , zorder=1, pivot="mid",
                alpha=0.5,width=0.005, scale=5, scale_units='inches', animated=True,
                color=cm(doppler))

    #circle = plt.Circle((0, 0), radi ,edgecolor='grey', facecolor='none', alpha=0.5, linewidth=6)
    ellipse = mpl.patches.Ellipse((0, -V[1]*(i/framerate)), 2*radi, 2*radi/gamma ,edgecolor='grey', facecolor='none', alpha=0.1, linewidth=6)
    #plt.gca().add_patch(circle)
    plt.gca().add_patch(ellipse)
    
    camera.snap()
        
###############################################################################    
animation = camera.animate(interval = 1000/framerate)# this is 50 frames a second #interval = 800, repeat = True, repeat_delay = 500)
animation.save('output/Animations/Animation_Uniform_Circular_Motion.mp4',dpi=400)
print(" Run time: %s seconds" % (time.time() - start_time))