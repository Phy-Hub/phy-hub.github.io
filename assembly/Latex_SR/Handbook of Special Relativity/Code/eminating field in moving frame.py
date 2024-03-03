# inward velocities are oppositly aberrated (fix)

""" calculates: the transformed speed of light velocity vectors, and the
    transformed flux element at an angle relative to proper flux element  """
import Paths as path
import SR_Functions as SR
import time
import matplotlib.pyplot as plt
import numpy as np
start_time = time.time()
### Constants ################################################################
N_ang = 71 # even number
dtheta = ( 2 * np.pi ) / ( N_ang - 1 )                                       ### theta <= pi, but 2pi used as needed for plot
c = 1
V_MAG = - 0.9

V = np.array([0,0,V_MAG])
Gamma = 1 / np.sqrt( 1 - ( V_MAG / c )**2 )

### output data
U_PRM = np.zeros((N_ang,3))
U     = np.zeros((N_ang,3))
R_PRM = np.zeros((N_ang,3))
ang = np.zeros((N_ang))
zeros = np.zeros((N_ang))

### angle rotated around z-axis from x-axis
phi = 0
CosP = np.cos(phi)
SinP = np.sin(phi)
ang = np.linspace( 0 , 2*np.pi - 2*np.pi/N_ang , N_ang)

###################### Primed Velocity Vectors ###############################
for k in range(N_ang):
    #ang[k] = k * dtheta# - dtheta # last term is to make sure
    U[k,:] = c * np.array([ np.sin(ang[k])*CosP, np.sin(ang[k])*SinP, np.cos(ang[k]) ])
    U_PRM[k,:] = SR.TRANS_Velocity_fast(U[k,:], V, V_MAG, Gamma, np.dot(U[k,:],V))

########## displacement in primed due to 1 second of proper time #############
    R_PRM[k,:] = SR.TRANS_3Position_fast(U[k,:], 1, V, V_MAG, Gamma, np.dot(U[k,:],V) )

### Relative Flux ############################################################
# primed flux relative to proper flux # maybe incorrect #
cosT = np.cos(ang)
ang_PRM = np.arccos( SR.TRANS_CT( cosT, V_MAG ) )

for i in range( int(N_ang/2), N_ang ):
    ang_PRM[i] = - ang_PRM[i]

surface_density = 1 / ( Gamma**2 * ( 1 + (V_MAG/c) * cosT )**2 )
R_ratio         = 1 / ( Gamma**2 * ( 1 + (V_MAG/c) * cosT )    )
Flux_tot = R_ratio * surface_density

### PLOTS ####################################################################
# Velocities in proper frame ##################################################
plt.figure(1)
plt.axis('equal')
plt.title('Field Propagation Velocities in particle\'s Proper Frame')
plt.plot(U[:,0], U[:,2], '.', alpha=0)
plt.quiver(zeros,zeros,U[:,0],U[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=8, headlength = 6)
plt.quiver(0,0,0,0,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.text(-1.5, 0.9, '<Proper>', color='r', weight='bold')
plt.yticks(ticks=[-1,-0.5,0,0.5,1], labels=None)
plt.xticks(ticks=[-1.5,-1,-0.5,0,0.5,1,1.5], labels=None)
plt.xlabel("$U_{Y}$")
plt.ylabel("$U_{Z}$")
plt.savefig( "Velocities_Proper.svg")
plt.savefig( "Velocities_Proper.pdf")

fig1 = plt.figure(2,frameon=False)
plt.axis('equal')
plt.axis('off')
Axis_max = 1
plt.xlim( -Axis_max , Axis_max )
plt.ylim( -Axis_max , Axis_max )
plt.plot(U[:,0], U[:,2], '.', alpha=0)
plt.quiver(zeros,zeros,U[:,0],U[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=6, headlength = 6, headaxislength = 6)
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
            hspace = 0, wspace = 0)
plt.margins(0,0)
#plt.text(0.5, -1, 'Particle at rest', color='black', weight='bold')
plt.scatter( 0 ,0, color = 'red' , s = 30, animated=True)
plt.savefig( "Still_Proper_field.svg",bbox_inches=0,transparent=True)
plt.savefig( "Still_Proper_field.pdf",bbox_inches=0,transparent=True)

# Velocities in primed frame ##################################################
plt.figure(3)
plt.axis('equal')
plt.title('Transformed Field Propagation Velocities')
plt.plot(U_PRM[:,0], U_PRM[:,2], '.', alpha=0)
plt.quiver(zeros,zeros,U_PRM[:,0],U_PRM[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=8, headlength = 6)
plt.quiver(0,0,0,-V_MAG,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.text(-1.5, 0.9, '<Primed>', color='r', weight='bold')
#plt.text(-2.5, -1.4, ' Velocity of particle <primed> = %s' %-V_MAG, color='r')
plt.yticks(ticks=[-1,-0.5,0,0.5,1], labels=None)
plt.xticks(ticks=[-1.5,-1,-0.5,0,0.5,1,1.5], labels=None)
plt.xlabel("$U_{Y}'$")
plt.ylabel("$U_{Z}'$")
plt.savefig( "Velocities_Aberrated.svg")
plt.savefig( "Velocities_Aberrated.pdf")

plt.figure(4,frameon=False)
plt.axis('equal')
plt.axis('off')
plt.xlim( -Axis_max , Axis_max )
plt.ylim( -Axis_max , Axis_max )
plt.plot(U_PRM[:,0], U_PRM[:,2], '.', alpha=0)
plt.quiver(zeros,zeros,U_PRM[:,0],U_PRM[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=6, headlength = 6, headaxislength = 6)
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.quiver(0,0,0,-V_MAG,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4, headaxislength = 3)
#plt.text(0.5, -1, 'Particle velocity = %s c' %V_MAG, color='black', weight='bold')
plt.savefig( "Still_primed_field.svg", bbox_inches='tight',transparent=True)
plt.savefig( "Still_primed_field.pdf", bbox_inches='tight',transparent=True)

plt.figure(5)
plt.axis('equal')
plt.title('Transformed Field Velocity (-c) with Evenly Distributes Proper Theta')
plt.plot(U_PRM[:,0], U_PRM[:,2], '.')#, alpha=0)
plt.quiver(U_PRM[:,0],U_PRM[:,2],-0.6*U_PRM[:,0],-0.6*U_PRM[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=8, headlength = 6)
plt.quiver(0,0,0,-V_MAG,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.text(-1.5, 0.9, '<Primed>', color='r', weight='bold')
plt.text(-2.5, -1.4, ' Velocity of particle <primed> = %s' %-V_MAG, color='r')
plt.yticks(ticks=[-1,-0.5,0,0.5,1], labels=None)
plt.xticks(ticks=[-1.5,-1,-0.5,0,0.5,1,1.5], labels=None)
plt.xlabel("$U_{X}'$")
plt.ylabel("$U_{Z}'$")

plt.figure(9,frameon=False)
plt.axis('equal')
plt.axis('off')
plt.plot(U_PRM[:,0], U_PRM[:,2], '.', alpha=0)
plt.quiver(U_PRM[:,0],U_PRM[:,2],-0.6*U_PRM[:,0],-0.6*U_PRM[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=8, headlength = 6)
plt.quiver(0,0,0,V_MAG,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.savefig( "Still_primed_field_2.svg", bbox_inches='tight', transparent=True)
plt.savefig( "Still_primed_field_2.pdf", bbox_inches='tight', transparent=True)


plt.figure(10,frameon=False)
plt.axis('equal')
plt.axis('off')
plt.plot(U[:,0], U[:,2], '.', alpha=0)
plt.quiver(U[:,0],U[:,2],-0.6*U[:,0],-0.6*U[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=8, headlength = 6)
plt.quiver(0,0,0,0,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.savefig( "Still_proper_field_2.svg", bbox_inches='tight', transparent=True)
plt.savefig( "Still_proper_field_2.pdf", bbox_inches='tight', transparent=True)


###############################################################################
plt.figure(6)
plt.axis('equal')
plt.title('displacement in primed due to 1 second of proper time')
plt.plot(R_PRM[:,0], R_PRM[:,2], '.', alpha=0)
plt.quiver(zeros,zeros,R_PRM[:,0],R_PRM[:,2],units='xy',scale=1,
           scale_units = 'xy', width= 0.01, headwidth=8, headlength = 6)
plt.quiver(0,0,0,-V_MAG,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
plt.text(-3.5, 4, '<Primed>', color='r', weight='bold')
plt.text(-4.5, -1.4, ' Velocity of particle <primed> = %s' %-V_MAG, color='r')
plt.xlabel("$R_{X}'$")
plt.ylabel("$R_{Z}'$")

# relative field strength #####################################################
fig = plt.figure(7)
ax = fig.add_subplot(projection='polar')
ax.scatter(ang_PRM,Flux_tot,c=Flux_tot, cmap='turbo', s=10) # cmap='Oranges'
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title('Relative Field Strength in Primed Frame')
plt.text(3.35*np.pi/4, np.max(Flux_tot)*1.35,
         ' $v_q$ = %s' %-V_MAG, color='r')
ax.text(np.radians(145),ax.get_rmax()/2.,'Strength Ratio',
        rotation=-45,ha='center',va='center')
plt.quiver(0,ax.get_rmax()/2,color='r',scale=1, scale_units = 'xy', width= 0.01,
           headwidth=5, headlength = 4)
ax.set_rlabel_position(135)
plt.savefig( "Field_Strength_Ratio.svg")
plt.savefig( "Field_Strength_Ratio.pdf")

###############################################################################
plt.figure(8)
V = np.linspace(-0.8, 0.999, 1000)
doppler =  ( ( 1 - V ) / ( 1 - V**2 ) )
plt.title('doppler factor (theta = 0)')
plt.plot(V, doppler, '.', label="$\gamma A$")
plt.plot(V, 1/doppler, '.', label="$ \dfrac{1}{\gamma A}$")
plt.xlabel("velcoity of frame")
plt.ylabel("Magnitude")
plt.legend(loc='best')

####################################################################
plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))