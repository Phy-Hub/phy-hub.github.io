import SR_Functions as SR
import numpy as np
import matplotlib.pyplot as plt
import time
start_time = time.time()
### Set up ####################################################################
c = 1
V = np.array([ 0 , -0.7])
Gamma = 1 / np.sqrt( 1 - ( V[1] / c )**2 )

dt = 0.1
t_0 = 0
N_t = 100
t_max = N_t * dt

t = np.linspace( t_0 , t_max , N_t)
t_prime = Gamma * t


a_z = -2
R_0 = np.array([ 0 , 0 ])
R_0_prime = R_0
U_0 = np.array([ 0 , 0.9 ])

R       =  np.zeros( ( len(t) , 2 ) )
R_prime =  np.zeros( ( len(t) , 2 ) )
U       =  np.zeros( ( len(t) , 2 ) )
U_prime =  np.zeros( ( len(t) , 2 ) )

U_0_prime = SR.TRANS_3Velocity(U_0, V)



for i in range(len(t)):
    R[i] =   R_mag * np.array([ np.sin(t[i]) ,   np.cos(t[i]) ])
    U[i] =   U_mag * np.array([ np.cos(t[i]) , - np.sin(t[i]) ])
    a[i] = - a_mag * np.array([ np.sin(t[i]) ,   np.cos(t[i]) ])
    
    
    U_prime[i] = SR.TRANS_3Velocity(U[i], V)
    a_prime[i] = SR.TRANS_2Acceleration(a[i], U[i], V)

R[0]       = R_0
R_prime[0] = R_0_prime
for i in range(len(t)-1):   
    
    R_prime[i+1] = R_prime[i]  + U_prime[i] * (Gamma * dt) + 0.5 * a[i] * (Gamma *dt)**2
    ### need to remove position propagated during

    
###############################################################################
plt.figure(1)
plt.axis('equal')
for i in range(len(t)):
    plt.scatter( R[i,0] ,R[i,1], color = 'black' , s = 5, animated=True,alpha=0.7)
 #   plt.scatter( R_prime[i,0] ,R_prime[i,1], color = 'red' , s = 5, animated=True,alpha=0.7)
    
plt.figure(2)
plt.axis('square')
for i in range(len(t)):
    plt.scatter( U_prime[i,0] ,U_prime[i,1], color = 'black' , s = 30, animated=True,alpha=0.7)
    
print(" Run time: %s seconds" % (time.time() - start_time))