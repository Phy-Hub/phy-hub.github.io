import Paths as path
import SR_Functions as SR
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
start_time = time.time()
### Set up ####################################################################
c = 1
V = np.array([ 0 , -0.9 ])
Gamma = 1 / np.sqrt( 1 - ( V[1] / c )**2 )

T_prop = 10
T_prop_PRM = Gamma * T_prop
t_PRM = 0#- Gamma *  ( V[1] / c ) * c*T_prop

t = 0
Rs = np.array([[ c*t , 0 , 0 ],[ c*t , 0 , 0 ]])#([[ c*t , 0 , c*T_prop ],[ c*t , 0 , - c*T_prop ]]) #sources

N_ang = 33 # even
ang = np.linspace( np.pi/N_ang , 2*np.pi - np.pi/N_ang , N_ang)

###############################################################################
R       =  np.zeros( ( len(Rs) , N_ang , 3 ) )
R_PRM   =  np.zeros( ( len(Rs) , N_ang , 3 ) )
R_PRM_  =  np.zeros( ( len(Rs) , N_ang , 2 ) )
C_PRM   =  np.zeros( ( len(Rs) , N_ang , 3 ) )
Rs_PRM  =  np.zeros( ( len(Rs)         , 2 ) )
Rs_PRM_ =  np.zeros( ( len(Rs)         , 2 ) )
### Main ######################################################################

C = np.swapaxes(  np.array([ np.tile( t , (N_ang,) ),  c * np.sin(ang) , c * np.cos(ang)  ])  ,0,1)

for i in range(len(Rs)):
    R[i] = C * T_prop + np.tile( Rs[i] , (N_ang,1) )

    R_PRM[i]  = SR.TRANS_Multi_R4(R[i], V)
    C_PRM[i]  = SR.TRANS_Multi_V4(C, R[i], V)

    for j in range(N_ang):
        R_PRM_[i,j] = SR.TRANS_3Position_simul(R[i,j,1:], V, C_PRM[i,j,1:], t)

    ts_PRM     = SR.TRANS_4Position( Rs[i] , V )[0]
    Rs_PRM[i]  = SR.TRANS_4Position( Rs[i] , V )[1:]
    Rs_PRM_[i] = SR.TRANS_3Position_simul(Rs[i,1:], V, -V, t)

### Plots #####################################################################
### Format ####################################################################
sc = 0.7 #0.7/3 #arrow scale
ylim = R_PRM[0,0,2] +4
xlim = -(Rs_PRM[1,1]+V[1]*T_prop_PRM) + 4
def PlotStyle(yy,zz,tt):
    plt.axis('equal')
    plt.axis('off')
    plt.axis('square')
    plt.xlim([-xlim, xlim])
    plt.ylim([-2*xlim,ylim])
    plt.arrow(-xlim, 0, 2*xlim-2, 0, lw = 1, head_width=1.3, head_length=1, overhang = sc,
              length_includes_head= True)
    plt.arrow(0, -ylim, 0, 2*ylim -2,lw = 1, head_width=1.3, head_length=1, overhang = sc,
              length_includes_head= True)
    plt.annotate(yy, xy=(0, 0), xytext=(xlim-6,2))
    plt.annotate(zz, xy=(0, 0), xytext=(-3,ylim-6))
    plt.annotate(tt, xy=(0, 0), xytext=(xlim/3,xlim/1.2))

### SubPlot 1 #################################################################
plt.figure(frameon=False)
PlotStyle("y","z","t = %s" %t)
for i in range(len(Rs)):
    plt.scatter( Rs[i,1] ,Rs[i,2], color = 'black' , s = 10, animated=True)
    plt.quiver(  R[i,:,1], R[i,:,2] , sc * C[:,1], sc * C[:,2],
                  angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
                  scale=5, scale_units='inches', headwidth=7, color="red")#,headwidth=1)

plt.savefig(path.svg +"Rest_Pulse.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf +"Rest_Pulse.pdf",bbox_inches='tight', format='pdf',transparent=True)

### SubPlot 2 #################################################################
plt.figure(frameon=False)
PlotStyle("y'","z'",  r"t' = $- \gamma \frac{vz}{c^2}$") # r"t'=$\gamma(t-\dfrac{vz}{c^2})$ ")
cm = mpl.cm.cool
for i in range(len(Rs)):
    coord = ( R_PRM[i,:,2] + R_PRM[0,0,2] ) / ( 2 * R_PRM[0,0,2] )
    plt.scatter( Rs_PRM[i,0] ,Rs_PRM[i,1]+V[1]*T_prop_PRM, color = 'grey' , s = 20, animated=True,alpha=0.4)
    plt.scatter( Rs_PRM[i,0] ,Rs_PRM[i,1], color = 'black' , s = 20, animated=True)

    plt.quiver(R_PRM[i,:,1], R_PRM[i,:,2], sc * C_PRM[i,:,1], sc * C_PRM[i,:,2],
                angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
                scale=5, scale_units='inches', headwidth=5, color=cm( coord ))

plt.savefig(path.svg +"Prime_Pulse.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf +"Prime_Pulse.pdf",bbox_inches='tight', format='pdf',transparent=True)

### SubPlot 3 #################################################################
plt.figure(frameon=False)
PlotStyle("y'","z'",r"t'= 0") #$\gamma$t")
doppler = SR.Doppler(V[1], C_PRM[0,:,2])
cm = mpl.cm.rainbow
for i in range(len(Rs)):
    plt.scatter( Rs_PRM[i,0] ,Rs_PRM[i,1]+V[1]*T_prop_PRM, color = 'grey' , s = 20, animated=True,alpha=0.7)
    plt.scatter( Rs_PRM_[i,0] ,Rs_PRM_[i,1], color = 'black' , s = 20, animated=True)

    plt.quiver(R_PRM_[i,:,0], R_PRM_[i,:,1], sc * C_PRM[i,:,1], sc * C_PRM[i,:,2],
                angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
                scale=5, scale_units='inches', headwidth=5, color=cm( doppler ))

plt.savefig(path.svg +"Prime_Pulse_Simultaneous.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf +"Prime_Pulse_Simultaneous.pdf",bbox_inches='tight', format='pdf',transparent=True)

###############################################################################
print(" Run time: %s seconds" % (time.time() - start_time))
plt.show()