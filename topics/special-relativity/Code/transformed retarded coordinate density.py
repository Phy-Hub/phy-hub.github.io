import numpy as np
import matplotlib.pyplot as plt
import Paths as path
filename_prefix = "coord_transform_"

# Define the density function
def density(x, y, z, b, g):
    denominator = g * ( 1 + b * g * z / np.sqrt(x**2 + y**2 + (g * z)**2) )
    return 1 / denominator

# Parameters
b = 0.9
g = 1 / np.sqrt(1 - b**2)

# Set x to a constant (for the y-z plane)
x = 0

# Grid creation
y = np.linspace(-5, 5, 1000)
z = np.linspace(-5, 5, 1000)
Y, Z = np.meshgrid(y, z)

# Calculate density values
density_values = density(x, Y, Z, b, g)
density_values = np.nan_to_num(density_values, nan=0)

# 2D Plotting (Figure 2)
fig = plt.figure()
ax = fig.add_subplot(111)

# Plot the 2D density image
im = ax.imshow(density_values, extent=[y.min(), y.max(), z.min(), z.max()], origin='lower', cmap='turbo')

# Add colorbar and labels
fig.colorbar(im)
ax.set_xlabel("y'")
ax.set_ylabel("z'", rotation=0)
#ax.set_title("Retarded Coordinate Density Transform")

plt.savefig(path.svg + filename_prefix + "Retarded_Coordinate_Density_Transform.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "Retarded_Coordinate_Density_Transform.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

# Show both figures
plt.show()
