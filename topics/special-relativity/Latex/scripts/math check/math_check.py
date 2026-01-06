from sympy import *
from sympy.printing import latex

x, y, z, beta, gamma = symbols('x y z beta gamma')
L = sqrt(x**2 + y**2 + gamma**2 * z**2)
F1 = x / (L * gamma * (1 - beta * gamma * z / L))
F2 = y / (L * gamma * (1 - beta * gamma * z / L))
F3 = gamma * (gamma * z / L - beta) / (gamma * (1 - beta * gamma * z / L))

J = Matrix([[diff(F1, x), diff(F1, y), diff(F1, z)],
            [diff(F2, x), diff(F2, y), diff(F2, z)],
            [diff(F3, x), diff(F3, y), diff(F3, z)]])

# Calculate the norm of the Jacobian matrix (Frobenius norm)
norm_J = sqrt(sum(sum(J[i, j]**2 for j in range(3)) for i in range(3))).simplify()

subs_dict = {sqrt(x**2 + y**2 + gamma**2 * z**2): Symbol("L")}
subs_dict2 = {(x**2 + y**2 + gamma**2 * z**2): Symbol("L^2")}
norm_J = norm_J.subs(subs_dict)
norm_J = norm_J.subs(subs_dict2)


#print("Norm of Jacobian:")
#pprint(norm_J)
#pprint(latex(norm_J), use_unicode=True)

# Write the LaTeX output to a file
with open("math_check.tex", "w") as f:
    f.write("\\documentclass[preview]{standalone}\n")
    f.write("\\usepackage{adjustbox}\n")
    f.write("\\begin{document}\n")
    f.write("\\begin{equation*}\n")
    f.write("\\adjustbox{max width=\\textwidth}{\n")
    f.write(latex(norm_J))
    f.write("\n } \n")
    f.write("\\end{equation*}\n")
    f.write("\\end{document}")