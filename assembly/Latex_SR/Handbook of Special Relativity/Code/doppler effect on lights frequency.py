import numpy as np
import matplotlib.pyplot as plt

vp= 0.8
c = 1
beta_p = vp/c
v=-vp

gamma = 1 / np.sqrt( 1 - beta_p**2 )

N_ang = 2003
theta = np.linspace( 0 , 2*np.pi , N_ang)
line = np.linspace( 0 , 0 , N_ang)

doppler = 1 / ( gamma * ( 1 - beta_p * np.cos(theta) ))

gbc = gamma* beta_p * np.cos(theta)

doppler2 = 1 / ( -gbc + np.sqrt( gbc**2 + 1 ) )


plt.figure()
plt.scatter( theta, doppler, color = 'black' , s = 1)
plt.scatter( theta, doppler2, color = 'red' , s = 1)

plt.show()