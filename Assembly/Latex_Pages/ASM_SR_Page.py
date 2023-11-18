import re
from pathlib import Path
import zipfile
import os
import shutil


def Diagrams_to_replace(filename):
    with open(filename, 'r') as file:
        data = file.read()

    # Regular expression pattern for tikzpicture or asy environment
    pattern = r'\\begin\{(tikzpicture|asy)\}.*?\\end\{(tikzpicture|asy)\}'

    # Replace the matched patterns with the error message
    new_data = re.sub(pattern, '*** MISSING DIAGRAM ***', data, flags=re.DOTALL)

    with open(filename, 'w') as file:
        file.write(new_data)


def colorbox_for_html(file_path):
    # Read the LaTeX file
    with open(file_path, 'r') as file:
        latex_content = file.read()

    # Regular expression pattern
    pattern = r"\\begin{tcolorbox}\[breakable\]\n\\begin{enumerate}(.*?)\\end{enumerate}\n\\end{tcolorbox}"
    replacement = r'<div style="border: 3px solid black; background-color: #fff9cf; padding: 10px; border-radius: 10px;">\1</div>'

    # Replace \item with <li> and add closing </li>
    latex_content = re.sub(r"\\item\s+(.*?)\n", r"<li>\1</li>\n", latex_content)

    # Perform the replacement
    html_content = re.sub(pattern, replacement, latex_content, flags=re.DOTALL)

    # Overwrite the original file with the HTML content
    with open(file_path, 'w') as file:
        file.write(html_content)


def create_toc(html_file):
    with open(html_file, 'r') as file:
        data = file.read()

    headers = re.findall(r'<(h[1-3])\s*([^>]*)>(.*?)</\1>', data)

    toc = "<h4>Contents</h4>\n"
    i=0
    for tag, attrs, text in headers:
        header_id = re.search(r'id="(.*?)"', attrs)
        text = text.strip()
        
        # Add indentation based on header tag
        if tag == 'h1':
            
            if i==0: 
                toc += f"<details id='{header_id.group(1)}_details' open>\n"       
            else:
                toc += "</details>\n"
                toc += f"<details id='{header_id.group(1)}_details' >\n"
            
            style = "style='font-weight: bold;'"
            toc += f"<summary onclick=\"showContent('{header_id.group(1)}_div')\"><a href='#{header_id.group(1)}' onclick=\"event.stopPropagation(); showContent('{header_id.group(1)}_div'); $(this).parent().parent().attr('open', '');\" {style}>{text}</a></summary>\n"
            i=1
            
            
        elif tag == 'h2':
            style = "style='display: block; margin-left: 20px;'"
            toc += f"<a href='#{header_id.group(1)}' {style}>{text}</a>\n"
        elif tag == 'h3':
            style = "style='display: block; margin-left: 40px;'"
            toc += f"<a href='#{header_id.group(1)}' {style}>{text}</a>\n"
        else:
            toc += "error\n"
            
  #      toc += f"<a href='#{header_id.group(1)}' {style}>{text}</a>\n"
        
    toc += "</details>\n"

    return toc


def copy_folder_from_zip(zip_file, folder, dest_folder):

    # Open the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # Extract each file in the specified folder to the destination folder
        for member in zip_ref.namelist():
            if member.startswith(folder):
                filename = os.path.basename(member)
                # Skip directories
                if not filename:
                    continue

                # Copy file (taken from zipfile's extract)
                source = zip_ref.open(member)
                target = open(os.path.join(dest_folder, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)



def Figures_to_HTML(file):
    with open(file, 'r') as f:
        content = f.read()

    figure_env_pattern = r'\\begin{figure}.*?\\end{figure}'
    include_graphics_pattern = r'\\includegraphics(\[.*?\])?\{(?P<filename>.*?)\}'
    tikzpicture_env_pattern = r'(\\begin{tikzpicture}.*?\\end{tikzpicture})'
    caption_pattern = r'\\caption\{(?P<caption>.*?)\}'

    figure_envs = re.findall(figure_env_pattern, content, re.DOTALL)

    for figure_env in figure_envs:
        replacement = ''
        include_graphics_match = re.search(include_graphics_pattern, figure_env)
        tikzpicture_env_match = re.search(tikzpicture_env_pattern, figure_env, re.DOTALL)
        caption_match = re.search(caption_pattern, figure_env)

        if include_graphics_match:
            filename = include_graphics_match.group('filename')
            filename = Path(filename).with_suffix('.svg')

            replacement = f'<br><figure><img src="Visuals/svg/{filename}" style="width:100%; height:auto;" loading="lazy"><figcaption>{caption_match.group("caption")}</figcaption> </figure>'
        elif tikzpicture_env_match:
            replacement =  '<br>*** MISSING TIKZ IMAGE ***<br>'          #tikzpicture_env_match.group(1)

            if caption_match:
                replacement += '\n' + caption_match.group('caption')

        content = content.replace(figure_env, replacement)

    with open(file, 'w') as f:
        f.write(content)


def replace_blank_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if line.strip() == '':
                file.write('<br>')
            else:
                file.write(line)
                
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
                
def remove_labels(filename):
    with open(filename, 'r') as file:
        data = file.read()

    # Remove all \label{...} occurrences
    data = re.sub(r'\\label\{.*?\}', '', data)

    with open(filename, 'w') as file:
        file.write(data)
                
def remove_mainmatter_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if '\\mainmatter' not in line:
                file.write(line)


def convert_latex_to_mathjax(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression pattern for inline math in LaTeX
    pattern = r'\$(.*?)\$'
    
    # Replace with MathJax friendly format
    new_content = re.sub(pattern, r'\(\1\)', content)

    with open(file_path, 'w') as file:
        file.write(new_content)


###
def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path, 'r', encoding='utf-8') as file:
        filedata = file.read()

    filedata = filedata.replace(old_string, new_string)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(filedata)


###
def replace_symbols(filename):
    with open(filename, 'r') as file:
        data = file.read()

    data = data.replace('$<', '$\\lt ')
    data = data.replace('>$', '\\gt $')

    with open(filename, 'w') as file:
        file.write(data)

###
def replace_figure_with_text(filename, text):
    with open(filename, 'r') as file:
        data = file.read()

    # Regex pattern to find the figure environment that contains a tikzpicture
    pattern = r'\\begin\{figure\}.*?\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}.*?\\end\{figure\}'

    # Replace the figure environment with the provided text
    data = re.sub(pattern, text, data, flags=re.DOTALL)

    with open(filename, 'w') as file:
        file.write(data)


###
def latex_to_html_headings(latex_content):
    # Replace chapters with h1 tags

    counter = [0]  # Use a list so that the variable is mutable inside the function
    def replace_func(m):
        counter[0] += 1
        if counter[0] > 1:
            return '</div> \n <div id="' + m.group(1).replace(' ', '').replace(':', '') + '_div" class="chapter" style="display: none !important;"> \n <h1 id="' + m.group(1).replace(' ', '').replace(':', '') + '">' + m.group(1) + '</h1>'
        else:
            return '</div> \n <div id="' + m.group(1).replace(' ', '').replace(':', '') + '_div" class="chapter"> \n <h1 id="' + m.group(1).replace(' ', '').replace(':', '') + '">' + m.group(1) + '</h1>'

    latex_content = re.sub(r'\\chapter\{(.+?)\}', replace_func, latex_content)

    latex_content = re.sub('</div> \n', '', latex_content, count=1)#removes first /div
    
    # Replace sections with h2 tags
    latex_content = re.sub(r'\\section\{(.+?)\}', lambda m:'<h2 id="' + m.group(1).replace(' ', '') + '">' + m.group(1) + '</h2>', latex_content)

    # Replace subsections with h3 tags
    latex_content = re.sub(r'\\subsection\{(.+?)\}', lambda m:'<h3 id="' + m.group(1).replace(' ', '') + '">' + m.group(1) + '</h3>', latex_content)

    # Replace subsubsections with h4 tags
    latex_content = re.sub(r'\\subsubsection\{(.+?)\}', lambda m:'<h4 id="' + m.group(1).replace(' ', '') + '">' + m.group(1) + '</h4>', latex_content)
    
    
    latex_content += '</div>'
    

    return latex_content


def create_html_with_mathjax(text_file_path, output_html_path):
    # Read the content of the text file
    with open(text_file_path, 'r') as file:
        text_content = file.read()

    # HTML template with MathJax
    html_template = f"""
        {text_content}
    """

    # Write the HTML content to the output file
    with open(output_html_path, 'w') as file:
        file.write(html_template)
        


def JS_input(file_path):
    # Read all lines into memory
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Perform the replacements and write all lines back to the same file
    with open(file_path, 'w') as file:
        for line in lines:
            match = re.search(r'javascript\{(.*)\}', line)
            if match:
                # The name of the replacement file is dependent on the content within the brackets
                replace_file = '../../Visuals/Diagrams/' + match.group(1) + '.html'
                try:
                    with open(replace_file, 'r') as rfile:
                        replace_lines = rfile.readlines()
                    # Replace the line with the lines from the replacement file
                    file.writelines(replace_lines)
                except FileNotFoundError:
                    print(f"File {replace_file} not found. Skipping replacement.")
            else:
                file.write(line)


Zip_folder = 'Handbook of Special Relativity.zip'

Latex_File = 'Special_Relativity.html'
with zipfile.ZipFile(Zip_folder, 'r') as myzip:
    with open(Latex_File, 'wb') as myfile:
        myfile.write(myzip.read('Tex/Main_Matter.tex'))
        
        
copy_folder_from_zip(Zip_folder,'images/svg', '../../Visuals/svg')

# to do first to avoid conflicts:
remove_comments(Latex_File)
replace_symbols(Latex_File)

# Call the function with your input and output file paths
Figures_to_HTML(Latex_File)
replace_blank_lines(Latex_File)
convert_latex_to_mathjax(Latex_File)
replace_string_in_file(Latex_File, 'mhl', 'bbox[#fff9cf, 10px, border-radius: 10px; border: 3px solid black]')
replace_string_in_file(Latex_File, '\\Vec', '\\mathbf')
replace_string_in_file(Latex_File, '\\scalebox{0.5}{R}', 'R')
replace_string_in_file(Latex_File, '\\AA', "Å") #'Å')
replace_string_in_file(Latex_File, '\\newline', '<br>')
replace_figure_with_text(Latex_File, '<br> *** There is a missing figure here *** <br>')
remove_mainmatter_lines(Latex_File)
remove_labels(Latex_File)
colorbox_for_html(Latex_File)
Diagrams_to_replace(Latex_File)
JS_input(Latex_File)


# Read the LaTeX file
with open(Latex_File, 'r') as file:
    latex_content = file.read()

# Convert to HTML headings
html_content = latex_to_html_headings(latex_content)

# Write the output to a new HTML file
with open(Latex_File, 'w') as file:
    file.write(html_content)


create_html_with_mathjax(Latex_File, Latex_File)

# Call the function with your HTML file
toc = create_toc(Latex_File)

def replace_inserts(input_file, output_file, toc_file, content_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    toc_lines = toc

    with open(content_file, 'r') as file:
        content_lines = file.readlines()

    with open("../Navbar.html", 'r') as file:
        navbar = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if '[Insert TOC]' in line:
                file.write('<div id="SR_toc" class="grid-item collapsible toc"> \n')  # Line before the match
                file.writelines(toc_lines)
                file.write('</div>\n')  # Line after the match
            elif '[Insert Content]' in line:
                file.write('<div id="content" class="grid-item" style="padding: 10px;" >\n')  # Line before the match
                file.writelines(content_lines)
                file.write('</div>\n')  # Line after the match
            elif '[Insert navbar]' in line:
                file.writelines(navbar)
                file.write('</div>\n')  # Line after the match
            else:
                file.write(line)

replace_inserts("Structure_LatexPage.html", "../../SR_Page.html", toc, Latex_File)
os.remove(Latex_File)