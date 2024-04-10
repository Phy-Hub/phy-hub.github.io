###
#
# use similar function to that of replace_eqref() to load figures from \ref's
#
#
# need to be able to handle sections and that with *'s i.e. \section*{}
#
#
#
#
import Paths as path
import subprocess
import re
import os

########################################################
# Formatting ###########################################
########################################################
###
def replace(filename, pattern, replacement):
    with open(filename, 'r', encoding='utf-8') as file:
        filedata = file.read()

    filedata = re.sub(pattern, replacement, filedata)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(filedata)

###
def replace_blank_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if line.strip() == '':
                file.write('<br>')
            else:
                file.write(line)

###
def remove_comments(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            # Remove everything after the '%' character
            line = re.sub('%.*', '', line)
            # Only write the line if it's not empty after removing the comment
            if line.strip():
                file.write(line)

###
def colorbox_replace(filename):
    # Read the LaTeX file
    with open(filename, 'r') as file:
        latex_content = file.read()

    # Regular expression pattern
    pattern = r"\\begin{tcolorbox}\[breakable\]\n\\begin{enumerate}(.*?)\\end{enumerate}\n\\end{tcolorbox}"
    replacement = r'<div style="border: 3px solid black; background-color: #fff9cf; padding: 10px; border-radius: 10px;">\1</div>'

    # Replace \item with <li> and add closing </li>
    latex_content = re.sub(r"\\item\s+(.*?)\n", r"<li>\1</li>\n", latex_content)

    # Perform the replacement
    html_content = re.sub(pattern, replacement, latex_content, flags=re.DOTALL)

    # Overwrite the original file with the HTML content
    with open(filename, 'w') as file:
        file.write(html_content)

###
#
# remove previous for first chapter ###
#
def replace_headings(latex_content):
    # Replace chapters with h1 tags
    counter = [0]
    def replace_func(m):
        counter[0] += 1
        if counter[0] > 1:
            return f"\n<div class='arrow-nav'>\n <a onclick=\"showContent('ch{counter[0]-2}_wrap')\" style=\"font-weight: bold; padding-left: 10px;\"> < Previous </a>\n<a onclick=\"showContent('ch{counter[0]}_wrap')\" style=\"font-weight: bold; text-align: right; padding-right: 10px; \"> Next > </a> \n</div>\n </section> \n <section id=\"ch{counter[0]}_wrap\" class=\"chapter\" style=\"display: none !important;\"> \n <h1 id=\"ch{counter[0]}_header\">" + f"{counter[0]}. " + m.group(1) + '</h1>'
        else:
            return f'<section id="ch{counter[0]}_wrap" class="chapter"> \n <h1 id="ch{counter[0]}_header">' + f"{counter[0]}. " + m.group(1) + '</h1>'

    latex_content = re.sub(r'\\chapter\{(.+?)\}', replace_func, latex_content)

    # Replace sections with h2 tags
    latex_content = re.sub(r'\\section\{(.+?)\}', lambda m:'<h2 id="' + m.group(1).replace(' ', '') + '_header">' + m.group(1) + '</h2>', latex_content)
    # Replace subsections with h3 tags
    latex_content = re.sub(r'\\subsection\{(.+?)\}', lambda m:'<h3 id="' + m.group(1).replace(' ', '') + '_header">' + m.group(1) + '</h3>', latex_content)
    # Replace subsubsections with h4 tags
    latex_content = re.sub(r'\\subsubsection\{(.+?)\}', lambda m:'<h4 id="' + m.group(1).replace(' ', '') + '_header">' + m.group(1) + '</h4>', latex_content)

    latex_content += f"\n<div>\n<a onclick=\"showContent('ch{counter[0]-1}_wrap')\" style=\"font-weight: bold;\"> < Previous </a> \n</div>\n"
    latex_content += '</section>'

    return latex_content

###
def wrap_content(latex_file):
    with open(latex_file, 'r') as file:
        lines = file.readlines()

    output = []
    chapter_num = 0
    section_num = 0
    subsection_num = 0

    for line in lines:
        if line.startswith('\\chapter'):
            chapter_num   += 1
            if subsection_num > 0:
                output.append('</div>  <!-- close subsection-->')
            if section_num > 1:
                output.append('</div> <!-- close section-->')
            if chapter_num > 1:
                output.append('</div> <!-- close chapter-->')
            output.append(line.strip())
            output.append(f'<div id="ch{chapter_num}'+'_content">')
            output.append('<span style="display: hidden">\\(\\nextSection\\)</span>')
            section_num    = 0
            subsection_num = 0
        elif line.startswith('\\section'):
            section_num   += 1
            if subsection_num > 0:
                output.append('</div>  <!-- close subsection-->')
            if section_num > 1:
                output.append('</div> <!-- close section-->')
            output.append(line.strip())
            output.append(f'<div id="ch{chapter_num}_{section_num}'+'_content">')
            subsection_num = 0
        elif line.startswith('\\subsection'):
            subsection_num += 1
            if subsection_num > 1:
                output.append('</div> <!-- close subsection-->')
            output.append(line.strip())
            output.append(f'<div id="ch{chapter_num}_{section_num}_{subsection_num}'+'_content">')
        else:
            output.append(line.strip())

    if chapter_num > 1:
        output.append('</div>') # to close last chapter

    with open(latex_file, 'w') as file:
        file.write('\n'.join(output))

########################################################
# Graphics #############################################
########################################################
###
def Figures_to_HTML(file):
    with open(file, 'r') as f:
        content = f.read()

    figure_envs = re.findall(r'\\begin{figure}.*?\\end{figure}', content, re.DOTALL)

    for figure_env in figure_envs:
        subfigure_envs = re.findall(r'\\begin{subfigure}.*?\\end{subfigure}', figure_env, re.DOTALL)
        if subfigure_envs:
            replacement = f'<br>\n \t <figure>\n <div style="display: flex; justify-content: space-between;">\n'
            for subfigure_env in subfigure_envs:
                replacement += '    ' + process_figure(subfigure_env) + '\n'
            replacement += '</div>\n'
            caption_match = re.search(r'\\caption\{(?P<caption>.*\})', figure_env)
            if caption_match:
                replacement += f'<figcaption>{caption_match.group("caption")[:-1]}</figcaption>\n'
            replacement += '</figure>\n'
        else:
            replacement = process_figure(figure_env)
        content = content.replace(figure_env, replacement)

    with open(file, 'w') as f:
        f.write(content)


def process_figure(figure_env):
    include_graphics_match = re.search(r'\\includegraphics(\[.*?\])?\{(?P<filename>.*?)\}', figure_env)
    tikzpicture_env_match = re.search(r'(\\begin{tikzpicture}.*?\\end{tikzpicture})', figure_env, re.DOTALL)
    tikzfilename_match = re.search(r'\\tikzsetnextfilename\{(?P<filename>.*?)\}', figure_env)
    caption_match = re.search(r'\\caption\{(?P<caption>.*\})', figure_env)

    if include_graphics_match or tikzpicture_env_match:
        filename = include_graphics_match.group('filename') if include_graphics_match else tikzfilename_match.group('filename') if tikzfilename_match else 'missing'
        filename = os.path.splitext(os.path.basename(filename))[0] + '.svg'
        if not os.path.isfile(path.py_to_svgs + f'{filename}'): print(" # \n # No file: " + path.py_to_svgs + f"{filename} \n #")
        return f'<figure>\n<img src="' + path.html_to_svgs + f'{filename}" style="width:100%; height:auto;" loading="lazy">\n<figcaption>&nbsp;{caption_match.group("caption")[:-1]}</figcaption>\n</figure>'
    else:
        return '*** svg figure missing ***'

###
def tikz2svg(input_directory, output_directory):
    # Get a list of all pdf files in the input directory
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Loop over the pdf files and convert each one to svg
    for pdf_file in pdf_files:
        svg_file = os.path.join(output_directory, os.path.splitext(pdf_file)[0] + '.svg')
        subprocess.run(['pdf2svg', os.path.join(input_directory, pdf_file), svg_file])

###
def insert_JS(filename, js_folder):
    # Read all lines into memory
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Perform the replacements and write all lines back to the same file
    with open(filename, 'w') as file:
        for line in lines:
            match = re.search(r'javascript\{(.*)\}', line)
            if match:
                # The name of the replacement file is dependent on the content within the brackets
                replace_file = js_folder + match.group(1) + '.html'
                try:
                    with open(replace_file, 'r') as rfile:
                        replace_lines = rfile.readlines()
                    # Replace the line with the lines from the replacement file
                    file.writelines(replace_lines)
                except FileNotFoundError:
                    print(f"File {replace_file} not found. Skipping replacement.")
            else:
                file.write(line)

########################################################
# Page elements ########################################
########################################################
###
def create_toc(html_file):

    headers = re.findall(r'<(h[1-2])\s*([^>]*)>(.*?)</\1>', html_file)

    toc = "<h4>Contents</h4>\n"
    i=0
    ch_num = 0
    for tag, attrs, text in headers:
        header_id = re.search(r'id="(.*?)"', attrs)
        text = text.strip()

        # Add indentation based on header tag
        if tag == 'h1':
            ch_num = ch_num + 1
            if i==0:
                toc += f"<details id='ch{ch_num}_details' open>\n"
            else:
                toc += "</details>\n"
                toc += f"<details id='ch{ch_num}_details' >\n"

            style = "style='font-weight: bold;'"
            toc += f"<summary onclick=\"showContent('ch{ch_num}_wrap')\"><a href='#{header_id.group(1)}' onclick=\"event.stopPropagation(); showContent('ch{ch_num}_wrap'); $(this).parent().parent().attr('open', '');\" {style}>{text}</a></summary>\n"
            i=1

        elif tag == 'h2':
            style = "style='display: block; margin-left: 20px;'"
            toc += f"<a href='#{header_id.group(1)}' {style}>{text}</a>\n"
        else:
            toc += "error\n"

    toc += "</details>\n"
    return toc

###
def create_terms(terms_folder):
    # Get the list of all files in directory tree at given path
    terms = []
    for (dirpath, dirnames, filenames) in os.walk(terms_folder):
        for file in filenames:
            # Open the file and read the lines
            with open(os.path.join(dirpath, file), 'r') as f:
                lines = f.readlines()
                # Append the lines to the list
                terms.extend(lines)

    output_lines = []
    state = None
    label, term, description = None, None, None
    for line in terms:
        if state == 'description':
            description = line.strip()
            description = re.sub(r'\$(.*?)\$', r'\(\g<1>\)', description).replace('<', '\\lt ').replace('>', '\\gt ')
            new_line = f'<dd id="{label}" style="display: none;"> <b>{term}:</b>  {description}  </dd>\n'
            output_lines.append(new_line)
            state = None
        else:
            match = re.search(r'\\noindent \\hypertarget{(.+?)}{\\textbf{(.+?):}}', line)
            if match:
                label, term = match.groups()
                state = 'description'
            else:
                match = re.search(r'\\noindent \$\{(.+?)\}\$', line)
                if match:
                    label = 'math_' + match.group(1).replace('<', 'lt-').replace('>', '-gt').replace("'", "-prime").replace("\\",'')
                    term = '\\(' + match.group(1) + '\\)'
                    state = 'description'
    return output_lines

###
def create_math_terms(directory):

    # Get the list of all files in directory tree at given path
    input_files = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for file in filenames:
            if file.startswith('Terms_ch'):
                input_files.append(os.path.join(dirpath, file))

    html_string = ''
    for input_file in input_files:
        html_string += f'<dl id="{os.path.splitext(os.path.basename(input_file))[0]}" style="display: none;">\n'
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
            for i in range(len(lines)):
                match = re.match(r'\\noindent \\hypertarget\{(.+)\}\{\$(.+)\$ \\textbf\{:\}\}', lines[i])
                if match:
                    name, variable = match.groups()
                    if i+1 < len(lines):
                        definition = lines[i+1].strip()
                        variable = variable.replace('<', '\\lt ').replace('>', '\\gt ')
                        definition = definition.replace('<', '\\lt ').replace('>', '\\gt ')
                        definition = re.sub(r'\\hyperlink\{(.*?)\}\{(.*?)\}', lambda m: f'<span onmouseover="document.getElementById(\'{m.group(1)}\').style.display=\'block\'" onmouseout="document.getElementById(\'{m.group(1)}\').style.display=\'none\'">{m.group(2)}</span>', definition)
                        definition = re.sub(r'\$(.*?)\$', r'\(\g<1>\)', definition)
                        new_line = f'<dt style="cursor: pointer;" onclick="document.getElementById(\'{name}\').style.display = document.getElementById(\'{name}\').style.display == \'none\' ? \'inline\' : \'none\';"> \\({variable}\\)<b>:</b> </dt>\n<dd id="{name}" style="display: none;">{definition}</dd>\n'
                        html_string += new_line
                    html_string += '<br>'
        html_string += '\n </dl>\n'

    return html_string

def math_to_HTML(content):
    math_envs = re.findall(r'\\begin{equation}.*?\\end{equation}', content, re.DOTALL)

    for math_env in math_envs:
        label = re.search(r'\\label\{(?P<label>.*\})', math_env)
        if label: id = f' id="{label.group("label")[:-1]}"'
        else:     id = ''
        content = content.replace(math_env, f'<div class="math"{id}>\n{math_env}\n</div>')

    return content


def replace_eqref(input_string):
    # This pattern matches \eqref{} and captures the content inside the brackets
    pattern = r'\\eqref\{(.*?)\}'

    # This function will be used to replace each match
    def replacer(match):
        id = match.group(1)
        # Replace with a span element that shows a div with the matched id on hover
        return f'<span class="eqref" onmouseover="copyContent(\'{id}\',\'equation_hover\');" onmouseout="deleteContent(\'equation_hover\');">\\eqref{{{id}}}</span>'

    # Use re.sub to replace each match in the input string
    output_string = re.sub(pattern, replacer, input_string)

    return output_string



###
def make_page(input_file, output_file, toc_file, content_file, Defs_file, Math_Terms_lines):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if '[Insert TOC]' in line:
                file.writelines(toc_file)
            elif '[Insert Content]' in line:
                file.writelines(content_file)
            elif '[Insert Definitions]' in line:
                file.writelines(Defs_file)
            elif '[Insert Math Terms]' in line:
                file.writelines(Math_Terms_lines)
            elif '[Insert PDF Link]' in line:
                file.write('<a href="\\latex\\' + path.html_to_pdf + 'Handbook of Special Relativity\\Layout.pdf" style="padding-top: 5px;"> <b> ↓ PDF </b> </a> <br>')
            else:
                file.write(line)

def checks(html):
    eq = 0
    print('### PROBLEM LaTeX LINES ###')
    with open(html, 'r') as file:
        for line in file:
            if line.startswith('\\begin{equation}'):
                eq = 1
                continue
            elif line.startswith('\\end{equation}'):
                eq = 0
                continue
            if eq == 0:
                if line.startswith('\\'):
                    print('# ' + line.strip())

                # Split the line into parts by LaTeX brackets
                parts = re.split(r'\\\(.+?\\\)', line)

                # Check each part for backslashes
                for part in parts:
                    if '\\' in part:
                        print(f"### '{line.strip()}'")
    print('######################')


###################################################################################
###################################################################################
###################################################################################
Latex_File = 'Latex_content.txt'

with open(path.py_to_main_tex, 'rb') as src, open(Latex_File, 'wb') as dst:
    dst.write(src.read())

# to do first to avoid conflicts:
remove_comments(Latex_File)
replace(Latex_File,'<', r'\\lt ')
replace(Latex_File,'>', r'\\gt ')

# Call the function with your input and output file paths
Figures_to_HTML(Latex_File)
tikz2svg(path.py_to_tikz, path.py_to_svgs)
replace_blank_lines(Latex_File)
replace(Latex_File, r'\$(.*?)\$', r'\(\1\)')
replace(Latex_File, 'mhl', 'bbox[#fff9cf, 10px, border-radius: 10px; border: 3px solid black]')
replace(Latex_File, r'\\Vec', r'\\mathbf')
replace(Latex_File, r'\\noindent', '')
replace(Latex_File, r'\\protect', '')
replace(Latex_File, r'\\textbf\{(.*?)\}', r'<b>\1</b>')
replace(Latex_File, r'\\hyperlink\{(.*?)\}\{(.*?)\}', "<span onmouseover=\"document.getElementById('\\g<1>').style.display='block'\" onmouseout=\"document.getElementById('\\g<1>').style.display='none'\">\\g<2></span>")
replace(Latex_File, r'\\scalebox{0.5}{R}', 'R')
replace(Latex_File, r'\\AA', "Å") #'Å')
replace(Latex_File, r'\\newline', '<br>')
replace(Latex_File, r'\\mainmatter', '')
#replace(Latex_File,r'\\label\{.*?\}', '')
replace(Latex_File,r'\\input\{.*?\}', '')
colorbox_replace(Latex_File)
insert_JS(Latex_File, path.py_to_js_diagrams)

wrap_content(Latex_File)

# Read the LaTeX file
with open(Latex_File, 'r') as file:
    latex_content = file.read()


# Convert to HTML headings
main_content = replace_headings(latex_content)
main_content = math_to_HTML(main_content)
main_content = replace_eqref(main_content)

# Call the function with your HTML file
toc = create_toc(main_content) # needs to take final html
vars = create_math_terms(path.py_to_terms)
defs = create_terms(path.py_to_terms)

make_page(path.py_to_page_structure, path.py_to_output_page, toc, main_content, defs, vars)

checks(path.py_to_output_page)

os.remove(Latex_File)

# pdflatex -synctex=1 -interaction=nonstopmode --shell-escape Layout.tex