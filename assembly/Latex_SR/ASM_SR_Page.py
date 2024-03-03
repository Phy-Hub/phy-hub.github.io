###
#
#
# need to be able to handle sections and that with *'s i.e. \section*{}
#
#
#
#
from pathlib import Path
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
def replace_headings(latex_content):
    # Replace chapters with h1 tags
    counter = [0]
    def replace_func(m):
        counter[0] += 1
        if counter[0] > 1:
            return '</section> \n <section id="' + m.group(1).replace(' ', '').replace(':', '') + '_div" class="chapter" style="display: none !important;"> \n <h1 id="' + m.group(1).replace(' ', '').replace(':', '') + '">' + m.group(1) + '</h1>'
        else:
            return '</section> \n <section id="' + m.group(1).replace(' ', '').replace(':', '') + '_div" class="chapter"> \n <h1 id="' + m.group(1).replace(' ', '').replace(':', '') + '">' + m.group(1) + '</h1>'

    latex_content = re.sub(r'\\chapter\{(.+?)\}', replace_func, latex_content)
    latex_content = re.sub('</section> \n', '', latex_content, count=1) #removes first /div

    # Replace sections with h2 tags
    latex_content = re.sub(r'\\section\{(.+?)\}', lambda m:'<h2 id="' + m.group(1).replace(' ', '') + '_header">' + m.group(1) + '</h2>', latex_content)
    # Replace subsections with h3 tags
    latex_content = re.sub(r'\\subsection\{(.+?)\}', lambda m:'<h3 id="' + m.group(1).replace(' ', '') + '_header">' + m.group(1) + '</h3>', latex_content)
    # Replace subsubsections with h4 tags
    latex_content = re.sub(r'\\subsubsection\{(.+?)\}', lambda m:'<h4 id="' + m.group(1).replace(' ', '') + '_header">' + m.group(1) + '</h4>', latex_content)

    latex_content += '</section>'

    return latex_content

###
def wrap_sections(latex_file):
    with open(latex_file, 'r') as file:
        lines = file.readlines()

    output = []
    current_div = None
    chapter_num = 0

    for line in lines:
        if line.startswith('\\chapter'):
            chapter_num += 1
            if current_div is not None:
                output.append('</div>')
            current_div = line.strip().split('{')[1].split('}')[0]
            output.append(line.strip())
            output.append(f'<div id="ch{chapter_num}_{current_div.replace(" ", "")}'+'_content">')
        elif line.startswith('\\section') or line.startswith('\\subsection'):
            if current_div is not None:
                output.append('</div>')
            current_div = line.strip().split('{')[1].split('}')[0]
            output.append(line.strip())
            output.append(f'<div id="ch{chapter_num}_{current_div.replace(" ", "")}'+'_content">')
        else:
            output.append(line.strip())

    if current_div is not None:
        output.append('</div>')

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
        return f'<figure style="margin-right: 10px;">\n<img src="/visuals/svg/{filename}" style="width:100%; height:auto;" loading="lazy">\n<figcaption>{caption_match.group("caption")[:-1]}</figcaption>\n</figure>'
    else:
        return '*** figure missing ***'


###
def pdfs2svgs(input_directory, output_directory):
    # Get a list of all pdf files in the input directory
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Loop over the pdf files and convert each one to svg
    for pdf_file in pdf_files:
        svg_file = os.path.join(output_directory, os.path.splitext(pdf_file)[0] + '.svg')
        subprocess.run(['pdf2svg', os.path.join(input_directory, pdf_file), svg_file])

###
def insert_JS(filename):
    # Read all lines into memory
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Perform the replacements and write all lines back to the same file
    with open(filename, 'w') as file:
        for line in lines:
            match = re.search(r'javascript\{(.*)\}', line)
            if match:
                # The name of the replacement file is dependent on the content within the brackets
                replace_file = '../../visuals/Diagrams/' + match.group(1) + '.html'
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
                toc += f"<details id='ch{ch_num}_{header_id.group(1)}_details' open>\n"
            else:
                toc += "</details>\n"
                toc += f"<details id='ch{ch_num}_{header_id.group(1)}_details' >\n"

            style = "style='font-weight: bold;'"
            toc += f"<summary onclick=\"showContent('{header_id.group(1)}_div')\"><a href='#ch{ch_num}_{header_id.group(1)}' onclick=\"event.stopPropagation(); showContent('{header_id.group(1)}_div'); $(this).parent().parent().attr('open', '');\" {style}>{text}</a></summary>\n"
            i=1

        elif tag == 'h2':
            style = "style='display: block; margin-left: 20px;'"
            toc += f"<a href='#{header_id.group(1)}' {style}>{text}</a>\n"
        else:
            toc += "error\n"

    toc += "</details>\n"
    return toc

###
def create_defs(Defs_latex):
    output_lines = []
    state = None
    label, term, description = None, None, None
    for line in Defs_latex:
        if state == 'description':
            description = line.strip()
            new_line = f'<dd id="{label}" style="display: none;"> <b>{term}:</b>   {description}  </dd>\n'
            output_lines.append(new_line)
            state = None
        else:
            match = re.search(r'\\noindent \\hypertarget{(.+?)}{\\textbf{(.+?):}}', line)
            if match:
                label, term = match.groups()
                state = 'description'
    return output_lines

###
def create_math_terms():

    directory = 'Handbook of Special Relativity'

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
                        new_line = f'<dt style="cursor: pointer;" onclick="document.getElementById(\'{name}\').style.display = document.getElementById(\'{name}\').style.display == \'none\' ? \'inline\' : \'none\';"> \({variable}\)<b>:</b> </dt>\n<dd id="{name}" style="display: none;">{definition}</dd>\n'
                        html_string += new_line
                    html_string += '<br>'
        html_string += '\n </dl>\n'

    return html_string

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
            else:
                file.write(line)

###################################################################################
###################################################################################
###################################################################################
folder = 'Handbook of Special Relativity'
Latex_File = 'Special_Relativity.html'

with open(os.path.join(folder, 'Tex/Main_Matter.tex'), 'rb') as src, open(Latex_File, 'wb') as dst:
    dst.write(src.read())

Defs_File = open('Handbook of Special Relativity\Tex\Terms\Definitions.tex').read().splitlines()


# to do first to avoid conflicts:
remove_comments(Latex_File)
replace(Latex_File,'<', r'\\lt ')
replace(Latex_File,'>', r'\\gt ')

# Call the function with your input and output file paths
Figures_to_HTML(Latex_File)
pdfs2svgs('Handbook of Special Relativity/tikz', '../../visuals/svg')
replace_blank_lines(Latex_File)
replace(Latex_File, r'\$(.*?)\$', r'\(\1\)')
replace(Latex_File, 'mhl', 'bbox[#fff9cf, 10px, border-radius: 10px; border: 3px solid black]')
replace(Latex_File, r'\\Vec', r'\\mathbf')
replace(Latex_File, r'\\noindent', '')
replace(Latex_File, r'\\protect', '')
replace(Latex_File, r'\\textbf\{(.*?)\}', r'<b>\1</b>')
replace(Latex_File, r'\\hyperlink\{(.*?)\}\{(.*?)\}', "<span onmouseover=\"document.getElementById('\g<1>').style.display='block'\" onmouseout=\"document.getElementById('\g<1>').style.display='none'\">\g<2></span>")
replace(Latex_File, r'\\scalebox{0.5}{R}', 'R')
replace(Latex_File, r'\\AA', "Å") #'Å')
replace(Latex_File, r'\\newline', '<br>')
replace(Latex_File, r'\\mainmatter', '')
replace(Latex_File,r'\\label\{.*?\}', '')
colorbox_replace(Latex_File)
insert_JS(Latex_File)

wrap_sections(Latex_File)

# Read the LaTeX file
with open(Latex_File, 'r') as file:
    latex_content = file.read()

# Convert to HTML headings
main_content = replace_headings(latex_content)

# Call the function with your HTML file
toc = create_toc(main_content) # needs to take final html
vars = create_math_terms()
defs = create_defs(Defs_File)

make_page("Structure_LatexPage.html", "../../pages/special-relativity.html", toc, main_content, defs, vars)

os.remove(Latex_File)


# pdflatex -synctex=1 -interaction=nonstopmode --shell-escape Layout.tex