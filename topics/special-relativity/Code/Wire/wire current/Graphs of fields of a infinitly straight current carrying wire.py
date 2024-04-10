import matplotlib.pyplot as plt 
import numpy as np

r = 2
q_e = -1
q_p = -1
Lambda = 3
Eps0 = 8.854 * 10**(-12)

axis = 10
n = 100
c = 3*10**8

u = v = np.linspace(-axis, axis, n)
v_p,v_e = np.meshgrid(u, v)

gamma_vp = 1 / np.sqrt(1 - (v_p**2/c**2))

Lambda_minus = Lambda * gamma_vp * (1+ (v_e*v_p / c**2))
Lambda_plus = - Lambda * gamma_vp 

Lambda_tot = Lambda_minus + Lambda_plus

E = (Lambda * v_e * v_p) / (2 * np.pi* Eps0 * c**2 * r)

F= q_p * E

plt.figure(1)
plt.title('E-Field')
plt.contourf(v_p,v_e, E, 100, cmap= 'bwr')
plt.colorbar()
plt.xlabel("$v_p$")
plt.ylabel("$v_e$")

plt.figure(2)
plt.title('Force on particle in Lab Frame')
plt.contourf(v_p,v_e, F, 100, cmap= 'bwr')
plt.colorbar()
plt.xlabel("$v_p$")
plt.ylabel("$v_e$")

plt.figure(3)
plt.title('Charge density in Particles frame')
plt.contourf(v_p,v_e, Lambda_tot, 100, cmap= 'bwr')
plt.colorbar()
plt.xlabel("$v_p$")
plt.ylabel("$v_e$")

plt.show()