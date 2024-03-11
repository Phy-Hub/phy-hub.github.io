
### needs to be done for v = (0,0,+v ) currently for (0,0,-v)


import numpy as np

V=-0.9
c=1

angle = np.pi/4
angle2 = (3/4)*np.pi

f1= np.array([np.cos(angle), np.sin(angle)])
f2= np.array([np.cos(angle2), np.sin(angle2)])

print(f1,f2)

dflux1 = (1-V**2/c**2) / (1+(V/c)*np.cos(angle))**2
dflux2 = (1-V**2/c**2) / (1+(V/c)*np.cos(angle2))**2

f1=f1*dflux1
f2=f2*dflux2
print(f1,f2)

print(dflux1,dflux2)