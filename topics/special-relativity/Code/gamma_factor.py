import Paths as path
import numpy as np
import matplotlib.pyplot as plt

# Define the velocity range as a fraction of the speed of light (c)
v_c = np.linspace(0, 0.99, 400)  # v/c ratio

# Lorentz Transformation (Special Relativity)
gamma = 1 / np.sqrt(1 - v_c**2)  # Lorentz factor

# Create the plot
plt.figure(figsize=(10, 6))
plt.figure(frameon=False)
plt.plot(v_c, gamma)
plt.title('Gamma Factor')
plt.xlabel('v/c')
plt.ylabel(r'$\gamma$')
plt.grid(False)  # Set grid to False
# Set the x-axis limits
plt.xlim(0, 1)

# Remove the white background
plt.gca().set_facecolor('none')

# Save the plot
plt.savefig(path.svg + 'Gamma_Factor.svg', transparent=True)
plt.savefig(path.pdf + 'Gamma_Factor.pdf', transparent=True)

# Show the plot
plt.show()
