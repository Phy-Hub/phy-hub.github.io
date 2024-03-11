import matplotlib.pyplot as plt 
import numpy as np

x_p = np.loadtxt("x_p.txt")
y_p = np.loadtxt("y_p.txt")
E_x = np.loadtxt("E_x.txt")
E_y = np.loadtxt("E_y.txt")
E_R = np.loadtxt("E_R.txt")
E_theta = np.loadtxt("E_theta.txt")


plt.pcolor(x_p,y_p,E_x, cmap= 'bwr')
plt.colorbar()
#plt.ylim(-5, 5)
plt.show() 

