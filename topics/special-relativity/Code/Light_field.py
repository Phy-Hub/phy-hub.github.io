import Paths as path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the parameters
u = 0  # 0 or 0.9
c = 1  # You can set this to any value
gamma = 1 / np.sqrt(1 - (u / c)**2)  # Lorentz factor

# Create a grid of x and z values
x_values = np.linspace(-10, 10, 100) # 1000
z_values = np.linspace(-10, 10, 100) # 1000
X, Z = np.meshgrid(x_values, z_values)
Y = 0
nan_space = 1.5
X = np.where( np.sqrt(X**2 + Z**2) > nan_space, X, np.nan)
Z = np.where( np.sqrt(X**2 + Z**2) > nan_space, Z, np.nan)

M = np.sqrt(X**2 + Y**2 + gamma**2 * Z**2)
front_factor = 1 / ( M * ( (u/c) * (gamma * Z / M ) + 1 )**2 )
common_factor = - ( (u/c) + (gamma * Z / M ) ) / M

partial_dcdx = front_factor / gamma * np.array([
                                        1 - X**2 / M**2 + (u/c) * (gamma * Z) / M,
                                        - X*Y / M**2,
                                        - X*Z / M**2
                                        ])

partial_dcdy = front_factor / gamma * np.array([
                                        - X*Y / M**2,
                                        1 - Y**2 / M**2 + (u/c) * (gamma * Z) / M,
                                        - Y*Z / M**2
                                        ])

partial_dcdz = front_factor * np.array([
                                        common_factor * X,
                                        common_factor * Y,
                                        (1 / gamma) * ( X**2 + Y**2) / M**2
                                        ])

partial_dcdt = -u*front_factor * np.array([
                                        common_factor * X,
                                        common_factor * Y,
                                        (1 / gamma) * ( X**2 + Y**2) / M**2
                                        ])

mag_tot = np.sqrt( partial_dcdx**2 + partial_dcdz**2  )

### Plots #####################################################################
### Format ####################################################################
def mag(partial_dc,x,y,z):
    return np.sqrt(partial_dc[0]**2 + partial_dc[1]**2 + partial_dc[2]**2)

def PlotStyle(fig_n, partial, coord):
    plt.figure(fig_n)
    contour = plt.contourf(X, Z, mag(partial,X,0,Z) , levels=300, cmap='nipy_spectral')
    cbar = plt.colorbar(contour, format='%.2f')
    plt.axis('square')
    circle = plt.Circle((0, 0), nan_space, color='black')
    plt.gca().add_patch(circle)
    plt.xlabel('x')
    plt.ylabel('z')
    plt.xticks(np.arange(-10, 11, 5))
    plt.yticks(np.arange(-10, 11, 5))

# Plot the 2D contour plot
PlotStyle(1,partial_dcdx, 'x')
PlotStyle(2,partial_dcdy, 'y')
PlotStyle(3,partial_dcdz, 'z')
#PlotStyle(4,'t')
PlotStyle(4,mag_tot, 'tot')

plt.show()
