import Paths as path
import numpy as np
import matplotlib.pyplot as plt
import subprocess

# Define the parameters
u = 0.9  # 0 or 0.9
c = 1  # You can set this to any value
gamma = 1 / np.sqrt(1 - (u / c)**2)  # Lorentz factor

N_coords = 1000 # 100, but increase to 300 for bigger file but better diagrams
# Create a grid of x and z values
coord_max = 10
y_values = np.linspace(-coord_max, coord_max, N_coords) # 1000
z_values = np.linspace(-coord_max, coord_max, N_coords) # 1000
Y, Z = np.meshgrid(y_values, z_values)
X = 0
nan_space = 1.5
Y = np.where( np.sqrt(Y**2 + Z**2) > nan_space-0.17, Y, np.nan)
Z = np.where( np.sqrt(Y**2 + Z**2) > nan_space-0.17, Z, np.nan)

M = np.sqrt(X**2 + Y**2 + gamma**2 * Z**2)
front_factor = 1 / ( gamma * M * ( 1 + (u/c) * (gamma * Z / M ) )**2 )
common_factor = - gamma * ( (u/c) + (gamma * Z / M ) ) / M

partial_dcdx = front_factor / gamma * np.array([
                                         Y**2 / M**2 + ( (gamma * Z) / M + (u/c) ) * (gamma * Z) / M,
                                        - X*Y / M**2,
                                        - X*Z / M**2
                                        ])

partial_dcdy = front_factor / gamma * np.array([
                                        - X*Y / M**2,
                                         X**2 / M**2 + ( (gamma * Z) / M + (u/c) ) * (gamma * Z) / M,
                                        - Y*Z / M**2
                                        ])

partial_dcdz = front_factor * np.array([
                                        common_factor * X,
                                        common_factor * Y,
                                        ( X**2 + Y**2) / M**2
                                        ])

partial_dcdt = -u*front_factor * np.array([
                                        common_factor * X,
                                        common_factor * Y,
                                        ( X**2 + Y**2) / M**2
                                        ])

mag_tot = np.sqrt( partial_dcdx**2 + partial_dcdy**2 + partial_dcdz**2  )

### Plots #####################################################################
### Format ####################################################################
def mag(partial_dc,x,y,z):
    return np.sqrt(partial_dc[0]**2 + partial_dc[1]**2 + partial_dc[2]**2)

def PlotStyle(fig_n, partial, coord):
    # plt.figure(fig_n)
    # contour = plt.contourf(Y, Z, mag(partial,X,Y,Z), levels=300, cmap='nipy_spectral') # levels=300

    fig = plt.figure(fig_n)
    ax = fig.add_subplot(111)
    contour = ax.imshow(mag(partial,X,Y,Z), extent=[-coord_max, coord_max, -coord_max, coord_max], origin='lower', cmap='nipy_spectral')

    cbar = plt.colorbar(contour, format='%.2f')
    plt.axis('square')
    circle = plt.Circle((0, 0), nan_space, color='black')
    plt.gca().add_patch(circle)
    plt.xlabel("$y$")
    plt.ylabel("$z$")
    plt.xticks(np.arange(-coord_max, 11, 5))
    plt.yticks(np.arange(-coord_max, 11, 5))

    filename = "Rate_of_change_of_lights_velocity_field_with_respect_to_" + coord
    if u == 0:
        filename = filename + "_u_is_0"
        plt.savefig(path.svg + filename + ".svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
        plt.savefig(path.pdf + filename + ".pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg
    else:
        plt.savefig(path.svg + filename + ".svg", bbox_inches='tight', format='svg',transparent=True) # changed from svg
        plt.savefig(path.pdf + filename + ".pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

    with open(path.svg + filename + ".svg", "r") as file:
        svg_content = file.read()

    # this stops line artifacts being rendered in html web page
    svg_content = svg_content.replace("<svg", '<svg shape-rendering="crispEdges"')

    with open(path.svg + filename + ".svg", "w") as file:
        file.write(svg_content)

    subprocess.run(['svgo', path.svg + filename + ".svg", '-o', path.svg + filename + ".svg"], shell=True)



# Plot the 2D contour plot
PlotStyle(1,partial_dcdx, 'x')
PlotStyle(2,partial_dcdy, 'y')
PlotStyle(3,partial_dcdz, 'z')
PlotStyle(4,partial_dcdt, 't')
PlotStyle(5,mag_tot, 'tot')

plt.show()
