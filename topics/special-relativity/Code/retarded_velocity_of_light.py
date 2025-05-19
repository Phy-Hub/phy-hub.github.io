import Paths as path
import numpy as np
import matplotlib.pyplot as plt

# Define the velocity range as a fraction of the speed of light (c)
v = np.linspace(-0.7, 0.99, 400)  # v/c ratio

# Lorentz Transformation (Special Relativity)
u_ret = 1 / (1 + v)  # Lorentz factor

# Create the plot
plt.figure(figsize=(10, 6))
plt.figure(frameon=False)
plt.plot(v, u_ret)
plt.title('retarded_speed_of_light')
plt.xlabel('v/c')
plt.ylabel(r'$\|\mathbf{u}_{ret}\|$')
plt.grid(False)  # Set grid to False
# Set the x-axis limits
plt.xlim(-1, 1)

plt.xticks(np.arange(-1, 1.1, 0.5))

# Remove the white background
plt.gca().set_facecolor('none')

# Save the plot
plt.savefig(path.svg + 'retarded_velocity_of_light.svg', transparent=True)
plt.savefig(path.pdf + 'retarded_velocity_of_light.pdf', transparent=True)

# Show the plot
plt.show()
