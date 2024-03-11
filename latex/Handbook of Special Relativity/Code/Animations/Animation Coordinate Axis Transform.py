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
Axis_max = 11
plt.xlim( -Axis_max , Axis_max )
plt.ylim( -Axis_max , Axis_max )
camera = Camera(fig)
##############################################################################
Vp = 0.75
c = 1
gamma = SR.Gamma(-Vp)

runtime = 6 # must be interger
framerate = 10#20

R0 = - Axis_max + 1 # intial position # double for single pulse
T0 = R0 / Vp    # intial time
N_t = framerate * runtime # number of time steps
T_step = - T0 / N_t #1 #.5 # interval between each arrow
N_ang = 10#100
N_waves = 1
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

#Looping the data and capturing frame at each iteration
for t in Time:     
    
    y = c*SIN_p[:] * t 
    z = c*COS_p[:] * t  + R0
     
    plt.quiver(y, z, sc * c*SIN_p[:], sc * c*COS_p[:], angles="xy", 
                zorder=1, pivot="mid", alpha=0.5,width=0.005, scale=5, 
                scale_units='inches', animated=True, color=cm(doppler[:]))
            
    # Propagation                
    plt.arrow(0, R0, y[1], z[1]-R0, lw = 1, head_width=0, head_length=0, overhang = sc, 
                          length_includes_head= True, color = "cyan")
    plt.arrow(0, R0, 0, Vp * t, lw = 1, head_width=0, head_length=0, overhang = sc, 
                          length_includes_head= True, color = "red")
                                        
    # particle:
    P = R0 + Vp * t
    plt.scatter( 0 , P  , color = 'red' , s = 30, animated=True)
    plt.scatter( 0 , R0  , color = 'gray' , s = 30, animated=True)
    
    # Axis
    plt.arrow(-2, P, 4, 0, lw = 1, head_width=0.5, head_length=0.5, overhang = sc, 
              length_includes_head= True, color = "grey") 
    plt.arrow(0, P-2, 0, 4 ,lw = 1, head_width=0.5, head_length=0.5, overhang = sc,
              length_includes_head= True, color = "grey",alpha=0.2)      
    plt.annotate("z", xy=(0, 0), xytext=(0.5,P+1.5), color = "grey")
    plt.annotate("y", xy=(0, 0), xytext=(1.5,P-1), color = "grey")
    
    plt.arrow(-3, 0, 6, 0, lw = 1, head_width=0.5, head_length=0.5, overhang = sc, 
              length_includes_head= True, color = "black") 
    plt.arrow(0, -3, 0, 6 ,lw = 1, head_width=0.5, head_length=0.5, overhang = sc,
              length_includes_head= True, color = "black")      
    plt.annotate("z'", xy=(0, 0), xytext=(0.5,3), color = "black")
    plt.annotate("y'", xy=(0, 0), xytext=(3,-1), color = "black")
    
    if t > 3:
        plt.annotate( r"$ \theta ' $", xy=(0, 0), xytext=(0.15,R0+2), color = "black")
           
    camera.snap()
    
for i in range(20):
    
    plt.quiver(y, z, sc * c*SIN_p[:], sc * c*COS_p[:], angles="xy", 
                zorder=1, pivot="mid", alpha=0.5,width=0.005, scale=5, 
                scale_units='inches', animated=True, color=cm(doppler[:]))
            
    # Propagation                
    plt.arrow(0, R0, y[1], z[1]-R0, lw = 1, head_width=0, head_length=0, overhang = sc, 
                          length_includes_head= True, color = "cyan")
    plt.arrow(0, R0, 0, -Vp * T0, lw = 1, head_width=0, head_length=0, overhang = sc, 
                          length_includes_head= True, color = "red")
                                      
    # particle:
    plt.scatter( 0 , R0 - Vp * T0  , color = 'red' , s = 30, animated=True)
    plt.scatter( 0 , R0  , color = 'gray' , s = 30, animated=True)
    
    # Axis
    plt.arrow(-2, P, 4, 0, lw = 1, head_width=0.5, head_length=0.5, overhang = sc, 
              length_includes_head= True, color = "grey") 
    plt.arrow(0, P-2, 0, 4 ,lw = 1, head_width=0.5, head_length=0.5, overhang = sc,
              length_includes_head= True, color = "grey",alpha=0.2)      
    plt.annotate("z", xy=(0, 0), xytext=(0.5,P+1.5), color = "grey")
    plt.annotate("y", xy=(0, 0), xytext=(1.5,P-1), color = "grey")
    
    plt.arrow(-3, 0, 6, 0, lw = 1, head_width=0.5, head_length=0.5, overhang = sc, 
              length_includes_head= True, color = "black") 
    plt.arrow(0, -3, 0, 6 ,lw = 1, head_width=0.5, head_length=0.5, overhang = sc,
              length_includes_head= True, color = "black")      
    plt.annotate("z'", xy=(0, 0), xytext=(0.5,3), color = "black")
    plt.annotate("y'", xy=(0, 0), xytext=(3,-1), color = "black")
    
    plt.annotate( r"$ \theta ' $", xy=(0, 0), xytext=(0.15,R0+2), color = "black")
    
    camera.snap()
        
        
###############################################################################    
animation = camera.animate(interval = 1000/framerate)# this is 50 frames a second #interval = 800, repeat = True, repeat_delay = 500)
animation.save('output/Animations/Emanating_Field_with_coordinate_axis.mp4',dpi=400)
print(" Run time: %s seconds" % (time.time() - start_time))