###
#
# use similar function to that of replace_refs() to load figures from ref's
#
#
# need to be able to handle sections and that with *'s i.e. \section*{}
#
#
#
#
import subprocess
import re
import os
import sys

### passed variables:
topic_folder_name = sys.argv[1]
pdf_name = sys.argv[2]
Topic_Name = sys.argv[3]

########################################################
# Paths ################################################
########################################################

### from make_page.py ###
py_to_page_structure = "../SCRIPTS/Structure_Page.html"
py_to_output_page    = "../../pages/" + topic_folder_name + ".html"
py_to_main_tex       = "Latex/Tex/Main_Matter.tex"
#py_to_defs          = "Latex/Tex/Terms/Definitions.tex"
py_to_terms          = "Latex/Tex/Terms"
py_to_tikz           = "Latex/output/tikz/"
py_to_svgs           = "Latex/images/svg/"
py_to_bib            = "Latex/refs.bib"
py_to_bugs           = "bugs/"


### from html page ###
html_to_svgs = "../topics/" + topic_folder_name + "/" + py_to_svgs
html_to_pdf  = "../topics/" + topic_folder_name + "/Latex/output/" + pdf_name
html_to_js_diagrams    = "./"


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
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() == '':
                file.write('<br>')
            else:
                file.write(line)

###
def remove_comments(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            # Remove everything after the '%' character
            line = re.sub('%.*', '', line)
            # Only write the line if it's not empty after removing the comment
            if line.strip():
                file.write(line)

###
def colorbox_replace(filename):
    # Read the LaTeX file
    with open(filename, 'r', encoding='utf-8') as file:
        latex_content = file.read()

    # Regular expression pattern
    pattern = r"\\begin{tcolorbox}\[breakable\]\n\\begin{enumerate}(.*?)\\end{enumerate}\n\\end{tcolorbox}"
    replacement = r'<div style="border: 3px solid black; background-color: #fff9cf; padding: 10px; border-radius: 10px;">\1</div>'

    # Replace \item with <li> and add closing </li>
    latex_content = re.sub(r"\\item\s+(.*?)\n", r"<li>\1</li>\n", latex_content)

    # Perform the replacement
    html_content = re.sub(pattern, replacement, latex_content, flags=re.DOTALL)

    # Overwrite the original file with the HTML content
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)

###
# *** when next/previous clicked, need to load the right TOC ***

def replace_headings(latex_content):
    # Replace chapters with h1 tags
    counter = [0]
    def replace_func(m):
        counter[0] += 1
        if counter[0] == 2:
            return f"\n<div class='arrow-nav'>\n <a></a>\n<a onclick=\"showContent('ch{counter[0]}_wrap'); document.getElementById('ch{counter[0]}_details').open = true;\" style=\"font-weight: bold; text-align: right; padding-right: 10px; \"> Next > </a> \n</div>\n </section> \n <section id=\"ch{counter[0]}_wrap\" class=\"chapter\" style=\"display: none !important;\"> \n <h1 id=\"ch{counter[0]}_header\">" + f"{counter[0]}. " + m.group(1) + '</h1>'
        elif counter[0] > 2:
            return f"\n<div class='arrow-nav'>\n <a onclick=\"showContent('ch{counter[0]-2}_wrap'); document.getElementById('ch{counter[0]-2}_details').open = true;\" style=\"font-weight: bold; padding-left: 10px;\"> < Previous </a>\n<a onclick=\"showContent('ch{counter[0]}_wrap'); document.getElementById('ch{counter[0]}_details').open = true;\" style=\"font-weight: bold; text-align: right; padding-right: 10px; \"> Next > </a> \n</div>\n </section> \n <section id=\"ch{counter[0]}_wrap\" class=\"chapter\" style=\"display: none !important;\"> \n <h1 id=\"ch{counter[0]}_header\">" + f"{counter[0]}. " + m.group(1) + '</h1>'
        else:
            return f'<section id="ch{counter[0]}_wrap" class="chapter"> \n <h1 id="ch{counter[0]}_header">' + f"{counter[0]}. " + m.group(1) + '</h1>'

    latex_content = re.sub(r'\\chapter\{(.+?)\}', replace_func, latex_content)

    # Replace sections with h2 tags
    latex_content = re.sub(r'\\section\{(.+?)\}', lambda m:'<h2 id="' + m.group(1).replace(' ', '').replace("'","") + '_header">' + m.group(1) + '</h2>', latex_content)
    # Replace subsections with h3 tags
    latex_content = re.sub(r'\\subsection\{(.+?)\}', lambda m:'<h3 id="' + m.group(1).replace(' ', '').replace("'","") + '_header">' + m.group(1) + '</h3>', latex_content)
    # Replace subsubsections with h4 tags
    latex_content = re.sub(r'\\subsubsection\{(.+?)\}', lambda m:'<h4 id="' + m.group(1).replace(' ', '').replace("'","") + '_header">' + m.group(1) + '</h4>', latex_content)

    latex_content += f"\n<div>\n<a onclick=\"showContent('ch{counter[0]-1}_wrap'); document.getElementById('ch{counter[0]-1}_details').open = true;\" style=\"font-weight: bold;\"> < Previous </a> \n</div>\n"
    latex_content += '</section>'

    return latex_content

###
def wrap_content(latex_file):
    with open(latex_file, 'r', encoding='utf-8') as file:
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

    with open(latex_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(output))

########################################################
# Graphics #############################################
########################################################
###
def Figures_to_HTML(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    chapter_counter = 0  # Initialize chapter counter
    figure_counter = 0  # Initialize figure counter

    # Find chapter starts (you might need to adjust the regex)
    chapter_starts = re.findall(r'\\chapter\{.*?\}', content)

    # Process each chapter separately
    for chapter_index, chapter_start in enumerate(chapter_starts):
        chapter_num = chapter_index + 1 # Auto-increment chapter number

        # Find the end of the current chapter (this is a simplification)
        # You might need a more robust way to determine chapter boundaries
        next_chapter_index = chapter_index + 1
        if next_chapter_index < len(chapter_starts):
            chapter_end_index = content.find(chapter_starts[next_chapter_index])
        else:
            chapter_end_index = len(content) # End of the document

        chapter_content = content[content.find(chapter_start):chapter_end_index]

        figure_envs = re.findall(r'\\begin{figure}.*?\\end{figure}', chapter_content, re.DOTALL)

        for figure_env in figure_envs:
            figure_counter += 1
            subfigure_envs = re.findall(r'\\begin{subfigure}.*?\\end{subfigure}', figure_env, re.DOTALL)
            if subfigure_envs:
                replacement = f'<br>\n \t <figure>\n <div style="display: flex; justify-content: space-between;">\n'
                subfig_letter = 'a'
                for subfigure_env in subfigure_envs:
                    replacement += '   ' + process_figure(subfigure_env, chapter_num, figure_counter, subfig_letter) + '\n'
                    subfig_letter = chr(ord(subfig_letter) + 1)
                replacement += '</div>\n'
                caption_match = re.search(r'\\caption\{(?P<caption>.*\})', figure_env)
                if caption_match:
                    # Add chapter and figure number to caption
                    replacement += f'<figcaption>Figure {chapter_num}.{figure_counter}: {caption_match.group("caption")[:-1]}</figcaption>\n'
                replacement += '</figure>\n'
            else:
                replacement = process_figure(figure_env, chapter_num, figure_counter, '')

            # Replace in the original content
            content = content.replace(figure_env, replacement)

        # Reset figure counter for the next chapter
        figure_counter = 0

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)


def process_figure(figure_env, chapter_num, figure_counter, subfig_letter):
    include_graphics_match = re.search(r'\\includegraphics(\[.*?\])?\{(?P<filename>.*?)\}', figure_env)
    tikzpicture_env_match = re.search(r'(\\begin{tikzpicture}.*?\\end{tikzpicture})', figure_env, re.DOTALL)
    tikzfilename_match = re.search(r'\\tikzsetnextfilename\{(?P<filename>.*?)\}', figure_env)
    caption_match = re.search(r'\\caption\{(?P<caption>.*\})', figure_env)
    label_match = re.search(r'\\label\{(?P<label>.*\})', figure_env)
    subfigures = re.findall(r'(\\begin\{subfigure\}.*?\\end\{subfigure\})', figure_env, re.DOTALL)

    if include_graphics_match or tikzpicture_env_match:
        filename = include_graphics_match.group('filename') if include_graphics_match else tikzfilename_match.group('filename') if tikzfilename_match else 'missing'
        filename = os.path.splitext(os.path.basename(filename))[0] + '.svg'
        if not os.path.isfile(py_to_svgs + f'{filename}'): print(" # \n # No file: " + py_to_svgs + f"{filename} \n #")
        if label_match:
            fig_id =  f' id="{label_match.group("label")[:-1].replace(" ", "_")}"'
        else:
            fig_id = ''

        if caption_match:
            caption_text = caption_match.group("caption")[:-1]
        else :
            caption_text = ""

        # Add chapter and figure number to caption if not a subfigure
        if "\\begin{subfigure}" in figure_env:
            caption = f"{subfig_letter}) {caption_text}"
        else:
            caption = f"Figure {chapter_num}.{figure_counter}: {caption_text}"


        return f'<figure' + fig_id +'>\n<img src="' + html_to_svgs + f'{filename}" style="width:100%; height:auto;" loading="lazy">\n<figcaption>{caption}</figcaption>\n</figure>'

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
def insert_JS(filename,js_location):
    # Read all lines into memory
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Perform the replacements and write all lines back to the same file
    with open(filename, 'w', encoding='utf-8') as file:
        N_s = 0
        script_lines = []
        for line in lines:
            match = re.search(r'javascript\{createTruckDiagram:(.*)\}', line)

            if match:
                N_s = N_s + 1
                script_line = 'createTruckDiagram("TruckFig_'+ str(N_s) + '",' + match.group(1) + ');\n'
                script_lines.append(script_line)
                file.write(f'<div id="TruckFig_' + str(N_s) + '"></div>\n')
            else:
                file.write(line)

    return script_lines

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
            with open(os.path.join(dirpath, file), 'r', encoding='utf-8') as f:
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
                    label = 'math_' + match.group(1).replace('<', '_lt').replace('>', '_gt').replace("'", "_prime").replace("\\",'').replace(" ", "_")
                    term = '\\(' + match.group(1) + '\\)'
                    state = 'description'
    return output_lines

###
### *** need to make labels for variables in my latex code
###
def create_math_terms(folder_path, file_prefix="Terms_ch"):
    variables = {}

    try:
        filenames = [
            f for f in os.listdir(folder_path) if f.startswith(file_prefix) and os.path.isfile(os.path.join(folder_path, f))
        ]
    except FileNotFoundError:
        print(f"Error: Folder not found: {folder_path}")
        return {}

    if not filenames:
        print(f"No files found with prefix '{file_prefix}' in '{folder_path}'")
        return {}

    html_string = ''
    for filename in filenames:
        filepath = os.path.join(folder_path, filename)
        html_string += f'<dl id="{os.path.splitext(os.path.basename(filename))[0]}" style="display: none;">\n'

        with open(filepath, "r", encoding="utf-8") as file:
            file_content = file.read()

            # Find all instances of \variable
            start_indices = [m.start() for m in re.finditer(r"\\variable", file_content)]

            for start_index in start_indices:

                # Find the first opening brace after \variable
                first_brace_index = file_content.find("{", start_index + 9)
                if first_brace_index == -1:
                    continue  # Skip if no opening brace

                # Extract variable name
                open_braces = 0
                variable_start = first_brace_index + 1
                variable_end = -1
                for i in range(variable_start, len(file_content)):
                    if file_content[i] == '{':
                        open_braces += 1
                    elif file_content[i] == '}':
                        if open_braces == 0:
                            variable_end = i
                            break
                        else:
                            open_braces -= 1

                if variable_end == -1:
                    continue  # Skip if no matching closing brace

                variable = file_content[variable_start:variable_end].strip()

                # Find the second opening brace (start of definition)
                second_brace_index = file_content.find("{", variable_end + 1)
                if second_brace_index == -1:
                    continue  # Skip if no second opening brace

                # Extract definition
                open_braces = 0
                definition_start = second_brace_index + 1
                definition_end = -1
                for i in range(definition_start, len(file_content)):
                    if file_content[i] == '{':
                        open_braces += 1
                    elif file_content[i] == '}':
                        if open_braces == 0:
                            definition_end = i
                            break
                        else:
                            open_braces -= 1

                if definition_end == -1:
                    continue # Skip if no matching closing brace.

                definition = file_content[definition_start:definition_end].strip()
                variables[variable] = definition

                ##########
                ##########
                label = "none"

                #Crucial:  fixing math and links to definition for html
                variable = variable.replace('<', '\\lt ').replace('>', '\\gt ')
                variable = re.sub(r'\$(.*?)\$', r'\1', variable) # Properly escape for LaTeX
                definition = definition.replace('<', '\\lt ').replace('>', '\\gt ')
                definition = re.sub(r'\\hyperlink\{(.*?)\}\{(.*?)\}', lambda m: f'<span onmouseover="document.getElementById(\'{m.group(1)}\').style.display=\'block\'" onmouseout="document.getElementById(\'{m.group(1)}\').style.display=\'none\'">{m.group(2)}</span>', definition)
                definition = re.sub(r'\$(.*?)\$', r'\\(\1\\)', definition) # Properly escape for LaTeX

                new_line = f'<dt style="cursor: pointer;" onclick="document.getElementById(\'{label}\').style.display = document.getElementById(\'{label}\').style.display == \'none\' ? \'inline\' : \'none\';"> \\({variable}\\)<b>:</b> </dt>\n<dd id="{label}" style="display: none;">{definition}</dd>\n'
                html_string += new_line

                html_string += '<br>'  # after each variable


        html_string += '\n </dl>\n'

    return html_string

###
def math_to_HTML(content):
    math_envs = re.findall(r'(?<!<div class="math">\n)\\begin{equation}.*?\\end{equation}', content, re.DOTALL)

    for math_env in math_envs:
        label = re.search(r'\\label\{(?P<label>.*\})', math_env)
        if label: id = f' id="{label.group("label")[:-1].replace(" ", "_")}"'
        else:     id = ''

        math_env_no_label = re.sub(r'\\label\{.*?\}', '', math_env, flags=re.DOTALL)
        # Remove newlines within the equation, except those after \\
        math_env_no_label_no_newlines = re.sub(r'(?<!\\\\)\n', ' ', math_env_no_label)
        content = content.replace(math_env, f'<div class="math"{id}>\n{math_env_no_label_no_newlines}\n</div>')

    return content

###
def replace_refs(input_string, fig_dict):
    # This pattern matches \eqref{} and captures the content inside the brackets
    pattern_ref_eq = r'\\eqref\{(.*?)\}'
    pattern_ref_fig = r'\\ref\{(.*?)\}'

    # This function will be used to replace each match
    def replacer_ref_eq(match):
        id = match.group(1).replace(" ", "_")
        eq_number = find_key_from_label(eq_dict, id)
        # Replace with a span element that shows a div with the matched id on hover
        return f'<span class="ref_eq" onmouseover="copyContent(\'{id}\',\'equation_hover\'); " onmouseout="deleteContent(\'equation_hover\');">({eq_number})</span>'
    def replacer_ref_fig(match):
        id = match.group(1).replace(" ", "_")
        fig_num = find_key_from_label(fig_dict,id)
        # Replace with a span element that shows a div with the matched id on hover
        return f'<span class="ref_fig" onmouseover="copyContent(\'{id}\',\'fig_hover\');" onmouseout="deleteContent(\'fig_hover\');">{fig_num}</span>'
    def replacer_cite_bib(match):
        id = match.group(1)


    # Use re.sub to replace each match in the input string
    output_string = re.sub(pattern_ref_eq , replacer_ref_eq, input_string)
    output_string = re.sub(pattern_ref_fig, replacer_ref_fig, output_string)

    return output_string

###
def bib_to_html(bib_file):

    with open(bib_file, 'r', encoding='utf-8') as bibfile:
        bib_content = bibfile.read()

    bib_lines = []  # Initialize the list of formatted lines

    entries = bib_content.split('@')[1:]
    entry_counter = 1

    for entry in entries:
        lines = entry.strip().split('\n')
        entry_type, citekey_rest = lines[0].split('{', 1)
        citekey = citekey_rest.strip(',')

        fields = {}
        for line in lines[1:-1]:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                fields[key.strip().lower()] = value.strip(' {},')

        # Custom formatting logic
        try:
            author_list = fields.get('author', '').split(' and ')
            if len(author_list) > 1:
                authors = f"{author_list[0].split(',')[0]}, et al."
            elif len(author_list) == 1 and ',' in author_list[0]:
                authors = author_list[0].split(',')[0]
            else:
                authors = author_list[0] if author_list else "Unknown Author"

            title = fields.get('title', 'No Title')
            journal = fields.get('journal', '')
            volume = fields.get('volume', '')
            number = fields.get('number', '')
            year = fields.get('year', '')
            pages = fields.get('pages', '')

            if pages:
                pages_str = f", pp. {pages.replace('--', '\u2013')}"
            else:
                pages_str = ""

            # Construct the formatted reference string
            reference_html = (
                f'<p id="{citekey}" style="font-size: 0.7em;">'
                f'[{entry_counter}] &nbsp; {authors} "{title}." In: <i>{journal}</i> {volume}{"."+number if number else ""}{" ("+year+")" if year else ""}{pages_str}.'
                f'</p>\n'
            )

            bib_lines.append(reference_html)  # Add the formatted line to the list
            entry_counter += 1

        except Exception as e:
            print(f"Error processing entry {citekey}: {e}")
            bib_lines.append(f'<p id="{citekey}">Error processing entry</p>\n')

    return bib_lines

###
def create_dictionary_of_bib(filepath):
    bib_dict = {}
    bib_number = 0
    pattern_cite_bib = r'\\cite\{(.*?)\}'

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filepath, 'w', encoding='utf-8') as file:
        for line in lines:
            match = re.search(pattern_cite_bib, line)
            if match:
                bib_label = match.group(1)

                if any(entry.get("label") == bib_label for entry in bib_dict.values()):
                    bib_number = find_key_from_label(bib_dict,bib_label)
                    html = f"<a>[{bib_number}]</a>"
                else:
                    bib_number = bib_number + 1
                    html = f"<a>[{bib_number}]</a>"
                    bib_dict[bib_number] = {"title": None, "label": bib_label}

                line = line.replace(match.group(0), html)

            file.write(line)

###
def create_dictionary_of_toc(filepath):
    structure_dict = {}
    counters = {
        "chapter": 0,
        "section": 0,
        "subsection": 0,
        "subsubsection": 0
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r"\\(chapter|section|subsection|subsubsection)(?:\[([^\]]*)\])?\s*\{([^}]+)\}\s*(?:\\label\{([^}]+)\})?", line)
            if match:
                level = match.group(1)
                short_title = match.group(2).strip() if match.group(2) else None
                title = match.group(3).strip()
                label = match.group(4).strip() if match.group(4) else None

                # Replace title with short_title if short_title exists
                if short_title:
                    title = short_title

                if level == "chapter":
                    counters["chapter"] += 1
                    counters["section"] = 0
                    counters["subsection"] = 0
                    counters["subsubsection"] = 0
                    structure_dict[f"{counters['chapter']}"] = {"title": title, "label": label}
                elif level == "section":
                    counters["section"] += 1
                    counters["subsection"] = 0
                    counters["subsubsection"] = 0
                    structure_dict[f"{counters['chapter']}.{counters['section']}"] = {"title": title, "label": label}
                elif level == "subsection":
                    counters["subsection"] += 1
                    counters["subsubsection"] = 0
                    structure_dict[f"{counters['chapter']}.{counters['section']}.{counters['subsection']}"] = {"title": title, "label": label}
                elif level == "subsubsection":
                    counters["subsubsection"] += 1
                    structure_dict[f"{counters['chapter']}.{counters['section']}.{counters['subsection']}.{counters['subsubsection']}"] = {"title": title, "label": label}

    return structure_dict

###
def create_dictionary_of_figures(latex_file):
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    figure_data = {}
    chapter_number = 0
    figure_number = 0
    label_count = 0

    chapters = re.split(r'\\chapter{', content)[1:]

    for chapter_content in chapters:
        chapter_number += 1
        figure_number = 0

        figure_matches = re.findall(r'\\begin{figure}(.*?)\\end{figure}', chapter_content, re.DOTALL)

        for figure_match in figure_matches:
            figure_number += 1

            label_count += len(re.findall(r'\\label{', figure_match))

            # Find main figure title and label
            figure_title = ""
            figure_label = ""
            caption_match = re.search(r'\\caption\s*(\{.*?\})\s*(?:\\label\s*\{([^}]+)\})?', figure_match, re.DOTALL)
            if caption_match:
                title_match = re.search(r'\\textbf{([^}]*?)}', caption_match.group(1))
                if title_match:
                    figure_title = title_match.group(1).strip()

            # Find label OUTSIDE of any subfigure environment
            temp_figure_match = figure_match
            for subfigure_match in re.findall(r'\\begin{subfigure}(.*?)\\end{subfigure}', figure_match, re.DOTALL):
                temp_figure_match = temp_figure_match.replace(subfigure_match, "")

            label_match = re.search(r'\\label{([^}]*?)}', temp_figure_match)
            if label_match:
                figure_label = label_match.group(1).replace(" ", "_")

            figure_id = f"{chapter_number}.{figure_number}"
            figure_data[figure_id] = {"title": figure_title, "label": figure_label}  # Store as dictionary

            subfigure_matches = re.findall(r'\\begin{subfigure}(.*?)\\end{subfigure}', figure_match, re.DOTALL)

            for i, subfigure_match in enumerate(subfigure_matches):
                subfigure_letter = chr(ord('a') + i)

                # Find subfigure title
                subfigure_title = ""
                subfigure_label = ""

                subfigure_caption_match = re.search(r'\\caption{(.*?)}', subfigure_match, re.DOTALL)
                if subfigure_caption_match:
                    subfigure_title_match = re.search(r'\\textbf{([^}]*?)}', subfigure_caption_match.group(1))
                    if subfigure_title_match:
                        subfigure_title = subfigure_title_match.group(1).strip()

                    # Find label within the caption or outside of it
                    label_match = re.search(r'\\label{([^}]*?)}', subfigure_caption_match.group(1))
                    if label_match:
                        subfigure_label = label_match.group(1).strip()
                    else:
                        label_match = re.search(r'\\label{([^}]*?)}', subfigure_match)
                        if label_match:
                            subfigure_label = label_match.group(1).strip()

                subfigure_id = f"{chapter_number}.{figure_number}.{subfigure_letter}"
                figure_data[subfigure_id] = {"title": subfigure_title, "label": subfigure_label}  # Store as dictionary

    return figure_data

###
def create_dictionary_of_equations(latex_file):
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    equation_data = {}
    chapter_number = 0
    equation_number = 0
    tot_equations = 0

    chapters = re.split(r'\\chapter{', content)[1:]

    for chapter_content in chapters:
        chapter_number += 1
        equation_number = 0

        equation_matches = re.findall(r'\\begin{equation}(.*?)\\end{equation}', chapter_content, re.DOTALL)

        tot_equations = tot_equations + len(equation_matches)


        for equation_match in equation_matches:
            equation_number += 1

            # Find equation label
            equation_label = ""
            label_match = re.search(r'\\label{([^}]*?)}', equation_match)
            if label_match:
                equation_label = label_match.group(1).replace(" ", "_")

            equation_id = f"{chapter_number}.{equation_number}"
            equation_data[equation_id] = {"label": equation_label}  # Store as dictionary

    return equation_data

###
def find_key_from_label(data_dict, target_label):
    for key, value in data_dict.items():
        if value['label'] == target_label:
            return key
    return None

###
def find_label_from_key(data_dict, target_key):
    if target_key in data_dict:
        return data_dict[target_key]['label']
    else:
        return None

###
def check_duplicate_labels(data_dict):
    label_to_keys = {}  # Dictionary to store labels and their associated keys

    for key, value in data_dict.items():
        label = value.get("label")
        if label:  # Check if the label exists
            if label in label_to_keys:
                label_to_keys[label].append(key)
            else:
                label_to_keys[label] = [key]

    # Check for duplicates and print messages
    for label, keys in label_to_keys.items():
        if len(keys) > 1:
            print(f"Duplicate label found: '{label}' in {keys}")

########################################################
# Make page ############################################
########################################################
###

###
def make_page(input_file, output_file, toc_file, content_file, Defs_file, Math_Terms_lines,script_lines, bib_lines):
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
                file.write('<a href="' + html_to_pdf + '" style="padding-top: 5px; color: black;"><b>&#11015; PDF</b></a><br>')
            elif '[Insert Topic Name]' in line:
                file.write(Topic_Name)
            elif '[Insert Script]' in line:
                for line in script_lines:
                    file.write(line)
            elif '[Insert Bib]' in line:
                for line in bib_lines:
                    file.write(line)
            else:
                file.write(line)

###
def checks(html_file):
    eq = 0
    line_number = 0  # Initialize line number counter
    with open(py_to_bugs + "latex_still_in_html.txt", 'w', encoding='utf-8') as outfile:
        outfile.write('### PROBLEM LaTeX LINES ###\n')
        with open(html_file, 'r', encoding='utf-8') as infile:
            i = 0
            Latex_commands = []
            for line in infile:
                line_number += 1  # Increment line number for each line
                if line.startswith('\\begin{equation}'):
                    eq = 1
                    continue
                elif line.startswith('\\end{equation}'):
                    eq = 0
                    continue
                if eq == 0:
                    part = re.sub(r'\\\(.+?\\\)', '*equation*', line)
                    latex_matches = re.findall(r"\\(\w+)\{", part)  # Find all matches in the line
                    for match in latex_matches:
                        if match not in Latex_commands:  # Check for duplicates before adding
                            Latex_commands.append(match)

                    if part.startswith('\\'):
                        i=i+1
                        outfile.write(f"# Line {line_number}: {part.strip()}\n")  # Include line number

                    if '\\' in part:
                        i=i+1
                        outfile.write(f"### Line {line_number}: '{part.strip()}'\n") # Include line number

        outfile.write('######################\n')
        outfile.write(f'number of lines with bugs: {i} \n')
        outfile.write('######################\n')
        outfile.write('commands: \n')
        for Latex_command in Latex_commands:
            outfile.write(f'\\{Latex_command} \n')

import re

def check_ids_for_spaces(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:  # Handle potential encoding issues
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{html_file_path}'")
        return []

    # Regular expression to find id attributes.  This is more robust than simply splitting.
    id_pattern = re.compile(r'id\s*=\s*["\']([^"\']*)["\']')
    matches = id_pattern.findall(html_content)
    invalid_ids = []

    if not matches:
        print(f"No matching IDs found in '{html_file_path}'")
        return []

    for id_value in matches:
        if " " in id_value:
            print(f"ID with spaces found: '{id_value}'")
            invalid_ids.append(id_value)
    return invalid_ids

###################################################################################
###################################################################################
###################################################################################
Latex_File = 'Latex_content.txt'

with open(py_to_main_tex, 'rb') as src, open(Latex_File, 'wb') as dst:
    dst.write(src.read())

# to do first to avoid conflicts:
remove_comments(Latex_File)
replace(Latex_File,'<', r'\\lt ')
replace(Latex_File,'>', r'\\gt ')

# Create dictionaries
toc_dict = create_dictionary_of_toc(Latex_File)
fig_dict = create_dictionary_of_figures(Latex_File)
bib_dict = create_dictionary_of_bib(Latex_File)
eq_dict  = create_dictionary_of_equations(Latex_File)
# check for duplicate lables
check_duplicate_labels(toc_dict)
check_duplicate_labels(fig_dict)
check_duplicate_labels(eq_dict)

# Call the function with your input and output file paths
Figures_to_HTML(Latex_File)
tikz2svg(py_to_tikz, py_to_svgs)
replace_blank_lines(Latex_File)
replace(Latex_File, r'\$(.*?)\$', r'\(\1\)')
replace(Latex_File, 'mhl', 'bbox[#fff9cf, 10px, border-radius: 10px; border: 3px solid black]')
replace(Latex_File, r'\\begin\{mainpoints\}', '<div style="border: 3px solid black; padding-right: 20px; padding-left: 10px; background-color: #f0f0f0; border-radius: 10px;" aria-label="Enumerated List">\n\t<ol>')
replace(Latex_File, r'\\end\{mainpoints\}', '\t</ol>\n</div>')
replace(Latex_File, r'\\begin\{itemize\}', '<ul>')
replace(Latex_File, r'\\end\{itemize\}', '</ul>')
replace(Latex_File, r'\\Vec', r'\\mathbf')
replace(Latex_File, r'\\noindent', '')
replace(Latex_File, r'\\protect', '')
replace(Latex_File, r'\\textbf\{(.*?)\}', r'<b>\1</b>')
replace(Latex_File, r'\\hyperlink\{(.*?)\}\{(.*?)\}', "<span onmouseover=\"document.getElementById('\\g<1>').style.display='block'\" onmouseout=\"document.getElementById('\\g<1>').style.display='none'\">\\g<2></span>")
replace(Latex_File, r'\\href\{(.*?)\}\{(.*?)\}', "<a style='color: black' href='\\g<1>' target='_blank' rel='noopener noreferrer'>\\g<2></a>")
replace(Latex_File, r'\\scalebox{0.5}{R}', 'R')
replace(Latex_File, r'\\AA', "Å") #'Å')
replace(Latex_File, r'\\newline', '<br>')
replace(Latex_File, r'\\mainmatter', '')
replace(Latex_File,r'\\fi', '')
replace(Latex_File,r'\\input\{.*?\}', '')
replace(Latex_File,r'\\printbibliography\[.*?\]', '')
colorbox_replace(Latex_File)
script_lines = insert_JS(Latex_File, html_to_js_diagrams) #needs to be before reading latex content
bib_lines = bib_to_html(py_to_bib)

wrap_content(Latex_File)

# Read the LaTeX file
with open(Latex_File, 'r', encoding='utf-8') as file:
    latex_content = file.read()

# Convert to HTML headings
main_content = replace_headings(latex_content)
main_content = math_to_HTML(main_content)
main_content = replace_refs(main_content, fig_dict)
main_content += '\n'
main_content =  re.sub(r'\\label\{.*?\}', '', main_content)

# Call the function with your HTML file
toc = create_toc(main_content) # needs to take final html
vars = create_math_terms(py_to_terms)
defs = create_terms(py_to_terms)


make_page(py_to_page_structure, py_to_output_page, toc, main_content, defs, vars, script_lines, bib_lines)

checks(py_to_output_page)
check_ids_for_spaces(py_to_output_page)

os.remove(Latex_File)

# pdflatex -synctex=1 -interaction=nonstopmode --shell-escape Layout.tex