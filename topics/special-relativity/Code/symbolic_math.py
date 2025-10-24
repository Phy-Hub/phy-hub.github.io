import sympy

# Define the symbols
y, z, b = sympy.symbols('y z b', real=True)

# Define g in terms of b
g = 1 / sympy.sqrt(1 - b**2)

# Define the integrand
integrand = 1 / (sympy.sqrt(y**2 + g**2 * z**2) + b * g * z)**2

# Compute the definite integral
integral_result = sympy.integrate(integrand, (z, -sympy.oo, sympy.oo))

print("Integral result:", integral_result)