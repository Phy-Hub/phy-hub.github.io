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
Axis_max = 40
plt.xlim( - Axis_max , Axis_max )
plt.ylim( -3 , Axis_max )
camera = Camera(fig)
##############################################################################
c = 1
Vp = 0.9
V = np.array([ 0 , - Vp ])
beta = - Vp
gamma = 1 / np.sqrt(  1 - ( Vp/c )**2  )

runtime = 10 # must be interger # 12
framerate = 2#10
N_t = framerate * runtime # number of time steps
T_step = 0.5#- T0 / N_t #1 #.5 # interval between each arrow
N_waves = 7
skip = round( N_t / N_waves )

Rc1      =  np.empty( ( N_t , 3 ) )
Rc2      =  np.empty( ( N_t , 3 ) )
Rc1_PRM  =  np.empty( ( N_t , 2 ) ) 
Rc2_PRM  =  np.empty( ( N_t , 2 ) )
Rc1.fill(np.nan)
Rc2.fill(np.nan)
Rc1_PRM.fill(np.nan)
Rc2_PRM.fill(np.nan)

y = 3
z2 = 3
COS = z2 / np.sqrt( ( 2*y )**2 + z2**2 )
SIN = (2*y) / np.sqrt( ( 2*y )**2 + z2**2 )
C1  = c * np.array([  SIN ,  COS ])
C2  = c * np.array([ -SIN , -COS ])
C1_PRM = SR.TRANS_3Velocity( C1, V )
C2_PRM = SR.TRANS_3Velocity( C2, V )

doppler  = SR.Doppler(V[1], C1_PRM[1])
doppler2 = SR.Doppler(V[1], C2_PRM[1])

cm = mpl.cm.rainbow
sc = 0.7 # arrow scale        
###############################################################################
### retarded ###
#Looping the data and capturing frame at each iteration
dt = (1 / framerate)
T_PRM_diff = gamma * beta * z2 
for i in range(N_t):
    
    t = i
    Rs1 = np.array([ t , -y , 0  ])  
    Rs2 = np.array([ t ,  y , z2 ])
    Rs1_PRM = SR.TRANS_4Position( Rs1 , V )[1:]       
    Rs2_PRM = SR.TRANS_4Position( Rs2 , V )[1:] + np.array([ 0 ,  Vp * T_PRM_diff  ]) 
    
    for m in range(N_t): 
        if (m <= i):

            Rc1[m,:]   = Rs1   
            Rc1[m,1:]  = Rc1[m,1:] + (i-m) * C1 * dt 
            Rc1_PRM[m] = SR.TRANS_4Position( Rc1[m] , V )[1:] + C1_PRM * ( gamma * beta * Rc1[m,2])                

            Rc2[m,:]   = Rs2 
            Rc2[m,1:]  = Rc2[m,1:] + (i-m) * C2 * dt 
            Rc2_PRM[m] = SR.TRANS_4Position( Rc2[m] , V )[1:] + C2_PRM * ( gamma * beta * Rc2[m,2])
     
            if ( Rc2_PRM[m,0] > y ):
                Rc2_PRM[m,:] = np.nan
            
        if ((m % skip == 0) and (gamma * i > m*T_step)):
            plt.quiver(Rc1_PRM[m,0], Rc1_PRM[m,1], sc * C1_PRM[0], sc * C1_PRM[1], 
                angles="xy" , zorder=1, pivot="mid",
                alpha=0.5,width=0.005, scale=5, scale_units='inches', animated=True,
                color=cm(doppler))
                
            plt.quiver(Rc2_PRM[m,0], Rc2_PRM[m,1], sc * C2_PRM[0], sc * C2_PRM[1], 
                angles="xy" , zorder=1, pivot="mid",
                alpha=0.5,width=0.005, scale=5, scale_units='inches', animated=True,
                color=cm(doppler2))      
    # source:
    plt.scatter( Rs1_PRM[0] , Rs1_PRM[1] , color = 'black' , s = 30, animated=True)
    plt.scatter( Rs2_PRM[0] , Rs2_PRM[1] , color = 'black' , s = 30, animated=True) 
        
    camera.snap()
        
###############################################################################    
plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))