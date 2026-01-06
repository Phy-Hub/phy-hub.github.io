########################################################
# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST#
########################################################
import subprocess
import re
import os
import sys
import urllib.request
import urllib.error

########################################################
# Paths ################################################
########################################################
topic_folder_name = "special-relativity"
pdf_name = "Handbook_of_Special_Relativity.pdf"
Topic_Name = "Special Relativity"
### from make_page.py ###
py_to_page_structure = "../SCRIPTS/Structure_Page.html"
py_to_output_page    = "../../pages/" + topic_folder_name + ".html"
py_to_main_tex       = "Latex/Tex/Main_Matter.tex"
#py_to_defs          = "Latex/Tex/Terms/Definitions.tex"
py_to_terms          = "Latex/Tex/Terms"
py_to_tikz           = "Latex/output/tikz/"
py_to_svgs           = "Latex/images/svg/"
py_to_pdfs           = "Latex/images/pdf/"
py_to_bib            = "Latex/refs.bib"
py_to_bugs           = "bugs/"
### from html page ###
html_to_svgs = "../topics/" + topic_folder_name + "/" + py_to_svgs
html_to_pdfs  = "../topics/" + topic_folder_name + "/Latex/output/" + pdf_name
html_to_js_diagrams    = "./"

########################################################
# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST#
########################################################

def check_latex_web_links(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # regex to find \href{...} contents
        urls = re.findall(r'\\href\{([^}]+)\}', f.read())

    # Filter/deduplicate
    links = set(u for u in urls if u.startswith(('http', 'www')))
    print(f"Checking {len(links)} links in '{filename}'...\n")

    for url in links:
        try:
            # We must fake a User-Agent or many sites (like Wikipedia/Amazon) will block urllib
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"✅ [{response.getcode()}] {url}")
        except urllib.error.HTTPError as e:
            # urllib raises an exception for 404s, 403s, etc.
            print(f"❌ [{e.code}] {url}")
        except urllib.error.URLError:
            print(f"🚫 [Connection Error] {url}")

# Call the function directly
check_latex_web_links(py_to_main_tex)