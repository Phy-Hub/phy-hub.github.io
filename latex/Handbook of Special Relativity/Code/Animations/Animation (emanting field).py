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
Axis_max = 10
plt.xlim( -Axis_max , Axis_max )
plt.ylim( -Axis_max , Axis_max )
camera = Camera(fig)
##############################################################################
retarded = 0
Vp = 0.9
c = 1
gamma = SR.Gamma(-Vp)

runtime = ( 2 - retarded ) * 6 # must be interger
framerate = 20

R0 = - ( 2 - retarded ) * Axis_max # intial position # double for single pulse
T0 = R0 / Vp # was c ####    # intial time
N_t = framerate * runtime # number of time steps
T_step = - T0 / N_t #1 #.5 # interval between each arrow
N_ang = 100
N_waves = 7
skip = round( N_t / N_waves )

Time = np.linspace(0, - T0 , N_t) # time after intial time
sc = 0.7 # arrow scale

Theta = np.linspace( np.pi/N_ang , 2*np.pi - np.pi/N_ang , N_ang)#np.linspace( 0  , 2*np.pi , N_ang ) 
COS_p   = np.zeros( ( len(Theta) ) )
SIN_p   = np.zeros( ( len(Theta) ) )
doppler = np.zeros( ( len(Theta) ) )
for i in range(len(Theta)):
    COS_p[i] =  SR.TRANS_CT( np.cos(Theta[i]), -Vp )#( np.cos(Theta[i]) + Vp )  /  ( 1 + Vp * np.cos(Theta[i]) )
    SIN_p[i] = np.sign(-(Theta[i]-np.pi)) * np.sqrt(1-COS_p[i]**2) 
    doppler[i] = SR.Doppler(-Vp, COS_p[i])

cm = mpl.cm.rainbow
###############################################################################
### single pulse ###
if retarded == 0:
    q = 0
    if Vp != 0 :
        for t in Time:
            if q % 2 == 0:
                plt.scatter( 0 ,Vp * (t/2) - Vp*Axis_max , color = 'black' , s = 30, animated=True)
                camera.snap()
            q = q + 1
        
    for t in Time:           
        y = c * t * SIN_p[:] 
        z = c * t * COS_p[:]
        if t == 0: 
            continue
        
        plt.quiver( y , z , sc * c*SIN_p[:] , sc * c*COS_p[:] , 
                 angles="xy" , zorder=1 , pivot="mid" , alpha=1 , width=0.005 , 
                 scale=5 , scale_units='inches' , animated=True , color=cm(doppler[:])  )
        # particle:
        plt.scatter( 0 ,Vp * (t) , color = 'black' , s = 30, animated=True)
        
        camera.snap()
###############################################################################
### retarded ###
if retarded == 1:
    #Looping the data and capturing frame at each iteration
    for t in Time:     
        for m in range(N_t): #### was N_c but both were same
            if ((m % skip == 0) and (t > m*T_step)):
                y = c*SIN_p[:] * ( t - T_step * m ) 
                z = c*COS_p[:] * ( t - T_step * m ) + ( R0 + Vp * (m * T_step) )
         
                plt.quiver(y, z, sc * c*SIN_p[:], sc * c*COS_p[:], angles="xy", 
                    zorder=1, pivot="mid", alpha=0.5,width=0.005, scale=5, 
                    scale_units='inches', animated=True, color=cm(doppler[:]))
        # particle:
        plt.scatter( 0 , R0 + Vp * t , color = 'black' , s = 30, animated=True)
        
        camera.snap()
        
###############################################################################    
animation = camera.animate(interval = 1000/framerate)# this is 50 frames a second #interval = 800, repeat = True, repeat_delay = 500)
animation.save('output/Animations/Emanating_Field.mp4',dpi=400)
print(" Run time: %s seconds" % (time.time() - start_time))