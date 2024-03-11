import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from celluloid import Camera
import time
start_time = time.time()
print("start time =", time.strftime("%H:%M:%S"))

# Creating figure and camera object ###########################################
fig = plt.figure(frameon=False)
plt.axis('off') #plt.axis('square') #fig.patch.set_alpha(0.)
plt.axis('equal')
Axis_max = 10
plt.xlim( -Axis_max , Axis_max )
plt.ylim( -Axis_max , Axis_max )
camera = Camera(fig)

###############################################################################
Vmax = 0.95
N_v = 30 # number of velocity steps
N_theta = 72
Theta = np.linspace( 0  , 2*np.pi , N_theta )
Vparticle = np.linspace( 0 , Vmax , N_v )

###############################################################################
### Velocity directions ###
c = 1
for Vp in Vparticle:
    gamma = 1 / np.sqrt(  1 - ( Vp/c )**2  )
    
    for i in range(len(Theta)-1):
        COS = ( np.cos(Theta[i]) + Vp )  /  ( 1 + Vp * np.cos(Theta[i]) )
        SIN = np.sign( np.pi - Theta[i] ) * np.sqrt( 1 - COS**2 )
        doppler2 = 1 / (  gamma * ( 1 + (Vp/c) * COS  )) - 0.25 / gamma**10 ### last term added to colour better ### 
        plt.arrow(0, 0, 9*SIN, 9*COS, color=mpl.cm.rainbow(doppler2), head_width=0.2)
    
    # particle, its velocity and text:
    X_p = plt.scatter( 0 ,0 , color = 'black' , s = 30, animated=True) 
    plt.quiver(0,0,0,9*Vp,color='black',scale=1, scale_units = 'xy', width= 0.01,
               headwidth=5, headlength = 4)
    plt.text(5, -10, 'Particle velocity = %s c' %Vp, color='black', weight='bold')
    
    camera.snap()

### Still #####################################################################
    if Vp == Vmax:
        fig = plt.figure(7)
        ax = fig.add_subplot(projection='polar')
        ax.scatter(0,1,c="black", s=10,alpha=0) # cmap='Oranges'
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title('Aberrated Angles')
        for i in range(len(Theta)-1):
            COS = ( np.cos(Theta[i]) + Vp )  /  ( 1 + Vp * np.cos(Theta[i]) )
            SIN = np.sign( np.pi - Theta[i] ) * np.sqrt( 1 - COS**2 )
            doppler2 = 1 / (  gamma * ( 1 + (Vp/c) * COS  )) - 0.25 / gamma**10            
            ax.quiver(0,0, SIN, COS , scale = 2,color=mpl.cm.rainbow(doppler2),alpha=1)
    
        plt.text(3.35*np.pi/4, 1.4,' $v_q$ = %s' %-Vmax, color='r')
        ax.text(np.radians(145),ax.get_rmax()/2.,'Velocity',
                rotation=-45,ha='center',va='center')
        plt.quiver(0,Vmax,color='black',scale=1, scale_units = 'xy', width= 0.01,
                   headwidth=5, headlength = 4)
        ax.set_rlabel_position(135)
        plt.scatter( 0 ,0 , color = 'black' , s = 50, animated=True) 
        plt.savefig("output/mmmmmmmmm.pdf")

    if Vp == Vmax:
        fig = plt.figure(frameon=False)
        plt.axis('off') #plt.axis('square') #fig.patch.set_alpha(0.)
        plt.axis('equal')
        Axis_max = 11
        plt.xlim( -Axis_max , Axis_max )
        plt.ylim( -Axis_max , Axis_max )
        
        ### Axis ######################################################################
        plt.annotate("y'", xy=(0, 0), xytext=(11,1))
        plt.annotate("z'", xy=(0, 0), xytext=(1,11))
        
        plt.arrow(-10, 0, 21, 0, lw = 1, head_width=1.5, head_length=1, overhang = 0.85, 
                  length_includes_head= True) 
        plt.arrow(0, -11, 0, 22, lw = 1, head_width=1.5, head_length=1, overhang = 0.85,
                  length_includes_head= True)
        
        for i in range(len(Theta)-1):
            COS = ( np.cos(Theta[i]) + Vp )  /  ( 1 + Vp * np.cos(Theta[i]) )
            SIN = np.sign( np.pi - Theta[i] ) * np.sqrt( 1 - COS**2 )
            doppler2 = 1 / (  gamma * ( 1 + (Vp/c) * COS  )) - 0.25 / gamma**10 ### last term added to colour better ### 
            plt.arrow(0, 0, 9*SIN, 9*COS, color=mpl.cm.rainbow(doppler2), head_width=0.2)
        
        # particle, its velocity and text:
        X_p = plt.scatter( 0 ,0 , color = 'black' , s = 30, animated=True) 
        plt.quiver(0,0,0,9*Vp,color='black',scale=1, scale_units = 'xy', width= 0.01,
                   headwidth=5, headlength = 4)
        plt.text(5, -10, 'Particle velocity = %s c' %Vp, color='black', weight='bold')
        plt.savefig("output/Stills/Aberrated_velocities.pdf",bbox_inches='tight', format='pdf',transparent=True)
        
###############################################################################
animation = camera.animate(interval = 1000/10)# this is 50 frames a second if 1000/20 #interval = 800, repeat = True, repeat_delay = 500)
animation.save('output/Animations/Animation_Aberrated_velocities.mp4',dpi=400)
print("Run time   = %s seconds" % (time.time() - start_time))