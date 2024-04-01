""" Output paths """

### from root

root_to_svg = "latex/Handbook of Special Relativity/images/svg/"

root_to_js_diagrams = "visuals/JS/"

root_to_pdf = "latex/Handbook of Special Relativity/Layout.pdf" ### not linked to python its in stucture file instead


### from python ###

py_to_root = "../"

py_to_latex_folder = "Handbook of Special Relativity/"

py_to_main_tex = py_to_latex_folder + "Tex/Main_Matter.tex"

py_to_defs = py_to_latex_folder + "Tex/Terms/Terms_ch1.tex"

py_to_terms = py_to_latex_folder + "Tex/Terms"

py_to_tikz = py_to_latex_folder + "output/tikz/"

py_to_svgs = py_to_latex_folder + "images/svg/"

py_to_page_structure = "Structure_Latex_Page.html"

py_to_output_page = py_to_root + "pages/special-relativity.html"

py_to_js_diagrams = py_to_root + root_to_js_diagrams


### from html ###

html_to_root = "../"

html_to_svgs = html_to_root + root_to_svg

html_to_pdf = html_to_root + root_to_pdf




# to get path use:
# import Paths as path
# plt.savefig(path.svg + "filename.type")