import Paths as path
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
start_time = time.time()
print("start time =", time.strftime("%H:%M:%S"))

###############################################################################
Vp = 0.95
N_v = 30 # number of velocity steps
N_theta = 72
Theta = np.linspace( 0  , 2*np.pi , N_theta )
c = 1
gamma = 1 / np.sqrt(  1 - ( Vp/c )**2  )

### Axis ######################################################################
def PlotStyle():
    plt.figure(frameon=False)
    plt.axis('off') #plt.axis('square') #fig.patch.set_alpha(0.)
    plt.axis('equal')
    Axis_max = 11
    plt.xlim( -Axis_max , Axis_max )
    plt.ylim( -Axis_max , Axis_max )

   # plt.annotate("y'", xy=(0, 0), xytext=(11,0.8))
    #plt.annotate("z'", xy=(0, 0), xytext=(0.6,11))

    ##plt.arrow(-10, 0, 21, 0, lw = 1, head_width=0.5, head_length=0.5, overhang = 0.85,
     #         length_includes_head= True)
    #plt.arrow(0, -11, 0, 22, lw = 1, head_width=0.5, head_length=0.5, overhang = 0.85,
    #          length_includes_head= True)

###############################################################################
### Velocity outwards directions rest frame ###
PlotStyle()
for i in range(len(Theta)-1):
    plt.arrow(0, 0, 9*np.sin(Theta[i]), 9*np.cos(Theta[i]), color = 'black', head_width=0.7, linewidth=1.5)

# particle, its velocity and text:
X_p = plt.scatter( 0 ,0 , color = 'black' , s = 30, animated=True)
plt.text(5, -10, 'Source velocity = 0', color='black', weight='bold')
plt.savefig(path.svg + "Aberrated_velocities_restframe.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf + "Aberrated_velocities_restframe.pdf",bbox_inches='tight', format='pdf',transparent=True)

###############################################################################
### Velocity outwards directions ###
PlotStyle()
for i in range(len(Theta)-1):
    COS_PRM = ( np.cos(Theta[i]) + Vp )  /  ( 1 + Vp * np.cos(Theta[i]) )
    SIN_PRM = np.sign( np.pi - Theta[i] ) * np.sqrt( 1 - COS_PRM**2 )
    doppler = 1 / (  gamma * ( 1 + (Vp/c) * COS_PRM  )) - 0.25 / gamma**10 ### last term added to colour better ###
    plt.arrow(0, 0, 9*SIN_PRM, 9*COS_PRM, color=mpl.cm.rainbow(doppler), head_width=0.7, linewidth=1.5)

# particle, its velocity and text:
X_p = plt.scatter( 0 ,0 , color = 'black' , s = 70, animated=True)
plt.quiver(0,0,0,9*Vp,color='black',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.text(5, -10, 'Source velocity = %s c' %Vp, color='black', weight='bold')
plt.savefig(path.svg + "Aberrated_velocities.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf + "Aberrated_velocities.pdf",bbox_inches='tight', format='pdf',transparent=True)

###############################################################################
### Velocity inwards directions ###
PlotStyle()
for i in range(len(Theta)-1):
    Theta[i] = Theta[i] + np.pi
    COS_PRM = ( np.cos(Theta[i]) - Vp )  /  ( 1 - Vp * np.cos(Theta[i]) )
    SIN_PRM = np.sign( 2 * np.pi - Theta[i] ) * np.sqrt( 1 - COS_PRM**2 )
    doppler = 1 / (  gamma * ( 1 - (Vp/c) * COS_PRM  )) - 0.25 / gamma**10 ### last term added to colour better ###
    plt.arrow(9*SIN_PRM, 9*COS_PRM,-3*SIN_PRM, -3*COS_PRM, color=mpl.cm.rainbow(doppler), head_width=0.7, linewidth=1.5)
    plt.arrow(9*SIN_PRM, 9*COS_PRM,-9*SIN_PRM, -9*COS_PRM, color=mpl.cm.rainbow(doppler), head_width=0, linewidth=1.5)

# particle, its velocity and text:
X_p = plt.scatter( 0 ,0 , color = 'black' , s = 100, animated=True)
plt.quiver(0,0,0,9*Vp,color='black',scale=1, scale_units = 'xy', width= 0.012, linewidth = 5,
           headwidth=4, headlength = 4.5)
plt.text(5, -10, 'Source velocity = %s c' %Vp, color='black', weight='bold')

plt.savefig(path.svg + "Aberrated_velocities_inwards.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf + "Aberrated_velocities_inwards.pdf",bbox_inches='tight', format='pdf',transparent=True)

###############################################################################
### Velocity inwards directions rest frame ###
PlotStyle()
for i in range(len(Theta)-1):
    plt.arrow(9*np.sin(Theta[i]), 9*np.cos(Theta[i]),-2*np.sin(Theta[i]), -2*np.cos(Theta[i]), color = 'black', head_width=0.4, linewidth=1.5)
    plt.arrow(9*np.sin(Theta[i]), 9*np.cos(Theta[i]),-9*np.sin(Theta[i]), -9*np.cos(Theta[i]), color = 'black', head_width=0, linewidth=1.5)

# particle, its velocity and text:
X_p = plt.scatter( 0 ,0 , color = 'black' , s = 100, animated=True)
plt.text(5, -10, 'Source velocity = 0', color='black', weight='bold')
plt.savefig(path.svg + "Aberrated_velocities_inwards_restframe.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf + "Aberrated_velocities_inwards_restframe.pdf",bbox_inches='tight', format='pdf',transparent=True)

plt.show()
###############################################################################
print("Run time   = %s seconds" % (time.time() - start_time))