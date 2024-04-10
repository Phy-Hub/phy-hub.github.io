""" Paths from the Make_page.py file """

def paths(topic_folder_name):

    ### from make_page.py ###

    py_to_page_structure = "../SCRIPTS/Structure_Page.html"

    py_to_output_page = "../../pages/" + topic_folder_name + ".html"

    ###

    py_to_main_tex = "Latex/Tex/Main_Matter.tex"

#   py_to_defs     = "Latex/Tex/Terms/Definitions.tex"

    py_to_terms    = "Latex/Tex/Terms"

    py_to_tikz     = "Latex/output/tikz/"

    py_to_svgs     = "Latex/images/svg/"

    py_to_js_diagrams = "JS_Animation/"


    ### from html ###

    html_to_svgs = "../topics/" + topic_folder_name + "/" + py_to_svgs

    html_to_pdf  = "../latex/"  + topic_folder_name + "/Layout.pdf"



    # to get path use:
    # import Paths as path
    # plt.savefig(path.svg + "filename.type")