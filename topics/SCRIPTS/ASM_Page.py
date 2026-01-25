###
import subprocess
import re
import os
import sys
import urllib.request, urllib.error
from datetime import datetime

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
py_to_main_tex       = "Latex/Main_Matter.tex"
py_to_defs          = "Latex/Tex/Terms/Definitions.tex"
py_to_terms          = "Latex/Tex/Terms"
py_to_term_comands   = "Latex/Tex/Terms/Term_commands.tex"
py_to_tikz           = "Latex/output/tikz/"
py_to_svgs           = "Latex/images/svg/"
#py_to_pdfs           = "Latex/images/pdf/"
py_to_bib            = "Latex/refs.bib"
py_to_bugs           = "bugs/"


### from html page ###
html_to_svgs = "../topics/" + topic_folder_name + "/" + py_to_svgs
html_to_pdfs  = "../topics/" + topic_folder_name + "/Latex/output/" + pdf_name
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
                file.write('<br>\n')
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
def wrap_content(latex_file):
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()

    # --- 1. PRE-SCAN: Map Chapters to Parts ---
    # We need this so the "Next" button in Part 1 knows that Chapter 2 is in Part 2.
    chapter_part_map = {}
    temp_part_count = 0
    temp_ch_count = 0

    for line in lines:
        if re.search(r'\\part(?:\[.*?\])?\{(.+?)\}', line):
            temp_part_count += 1
        elif re.search(r'\\chapter(?:\[.*?\])?\{(.+?)\}', line):
            temp_ch_count += 1
            # If a chapter appears before any part, it defaults to part 0
            chapter_part_map[temp_ch_count] = temp_part_count

    total_chapters = temp_ch_count

    # --- 2. SETUP ---
    LEVELS = {
        'chapter': (0, 3),
        'section': (1, 4),
        'subsection': (2, 5),
        'subsubsection': (3, 6)
    }

    nums = [0, 0, 0, 0]  # [ch, sec, subsec, subsubsec]
    output = []
    in_part = False
    part_count = 0

    # --- 3. HELPER FUNCTIONS ---

    def get_nav_footer(current_ch, current_part):
        """Generates HTML for Previous/Next with Part-aware IDs."""
        prev_ch = current_ch - 1
        next_ch = current_ch + 1

        # Calculate Previous Button
        if prev_ch >= 1:
            prev_part = chapter_part_map.get(prev_ch, 0)
            prev_id = f"part_{prev_part}_ch{prev_ch}"
            prev_btn = (f'<a onclick="showContent(\'{prev_id}_wrap\'); syncToc(\'{prev_id}_toc\');" '
                        f'style="font-weight: bold; padding-left: 10px; cursor: pointer;"> &lt; Previous </a>\n')
        else:
            prev_btn = "<a></a>\n"

        # Calculate Next Button
        if next_ch <= total_chapters:
            next_part = chapter_part_map.get(next_ch, 0)
            next_id = f"part_{next_part}_ch{next_ch}"
            next_btn = (f'<a onclick="showContent(\'{next_id}_wrap\'); syncToc(\'{next_id}_toc\');" '
                        f'style="font-weight: bold; text-align: right; padding-right: 10px; cursor: pointer;"> Next &gt; </a>\n')
        else:
            next_btn = ""

        return f'\n\n<div class="arrow-nav">\n{prev_btn}{next_btn}</div>\n\n</section>\n'

    def close_tags(target_depth, reset_counters=True):
        for i in range(3, target_depth - 1, -1):
            if nums[i] > 0:
                if not in_part:
                    output.append('</div>')
                if i > target_depth and reset_counters:
                    nums[i] = 0

    def close_block(reset_counters=True):
        close_tags(1, reset_counters=reset_counters)
        if in_part:
            output.append('</div>')
            output.append('</section>\n')
        elif nums[0] > 0:
            # Pass current part_count to footer
            output.append(f'</div>{get_nav_footer(nums[0], part_count)}')

    # --- 4. MAIN PARSING LOOP ---
    for line in lines:
        line = line.strip()

        # Handle Parts
        part_match = re.search(r'\\part(?:\[.*?\])?\{(.+?)\}', line)
        if part_match:
            close_block(reset_counters=False)
            in_part = True
            part_count += 1
            # ID Format: partX_wrap
            output.append(f'<section id="part_{part_count}_wrap" class="chapter part-wrapper">')
            output.append(f'<h2 class="part_header" id="part_{part_count}_header" style="display: flex; justify-content: center; text-align: center;">Part {to_roman(part_count)}.<br>{part_match.group(1)}</h2>')
            output.append(f'<div id="part_{part_count}_content">')
            continue

        # Handle Chapters and Sections
        cmd_match = re.search(r'\\(chapter|section|subsection|subsubsection)(?:\[.*?\])?\{(.+?)\}', line)
        if cmd_match:
            cmd, title = cmd_match.groups()
            depth, h_lvl = LEVELS[cmd]

            if depth == 0: # Chapter
                close_block()
                in_part = False
                nums[0] += 1
                nums[1:] = [0, 0, 0]

                # --- NEW ID GENERATION ---
                # We prefix with part_{part_count}_
                current_id_base = f"part_{part_count}_ch{nums[0]}"

                display = ' style="display: none !important;"' if nums[0] > 1 else ""

                output.append(f'<section id="{current_id_base}_wrap" class="chapter" {display}>\n'
                              f'<h3 id="{current_id_base}_header" class="chapter_header" style="display: flex; justify-content: center; text-align: center;">Chapter {nums[0]}. {title}</h3>')
                output.append(f'<div id="{current_id_base}_content">\n<span style="display: none">\\(\\nextSection\\)</span>')
            else:
                close_tags(depth)
                nums[depth] += 1

                # Update ID for sub-items to match parent pattern
                # e.g. part1_ch1_1
                suffix_str = "_".join(map(str, nums[:depth+1]))
                id_str = f"part_{part_count}_ch{suffix_str}"

                prefix = ".".join(map(str, nums[:depth+1])) if depth < 3 else ""
                output.append(f'<h{h_lvl} id="{id_str}_header">{prefix} {title}</h{h_lvl}>\n<div id="{id_str}_content">')
            continue

        output.append(line)

    close_block() # Final cleanup

    with open(latex_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))


########################################################
# Graphics #############################################
########################################################
###
def Figures_to_HTML(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    chapter_counter = 0
    figure_counter = 0

    chapter_starts = re.findall(r'\\chapter\{.*?\}', content)

    for chapter_index, chapter_start in enumerate(chapter_starts):
        chapter_num = chapter_index + 1

        next_chapter_index = chapter_index + 1
        if next_chapter_index < len(chapter_starts):
            chapter_end_index = content.find(chapter_starts[next_chapter_index])
        else:
            chapter_end_index = len(content)

        chapter_content = content[content.find(chapter_start):chapter_end_index]

        figure_envs = re.findall(r'\\begin{figure}.*?\\end{figure}', chapter_content, re.DOTALL)

        for figure_env in figure_envs:
            figure_counter += 1
            subfigure_envs = re.findall(r'\\begin{subfigure}.*?\\end{subfigure}', figure_env, re.DOTALL)

            if subfigure_envs:
                # Extract main figure caption and label FIRST
                caption_match = re.search(r'\\caption\{(?P<caption>.*\})', figure_env)
                label_match = re.search(r'\\label\{(?P<label>.*\})', figure_env)

                replacement = f'<br>\n \t <figure class="subfigures" '
                if label_match:
                    main_fig_label = find_label_from_key(fig_dict, f"{chapter_num}_{figure_counter}")
                    replacement += f' id="{main_fig_label}"'  # Add ID to <figure>
                replacement += '>\n <div style="display: flex; justify-content: space-between;">\n'

                subfig_letter = 'a'
                for subfigure_env in subfigure_envs:
                    replacement += '   ' + process_figure(subfigure_env, chapter_num, figure_counter, subfig_letter) + '\n'
                    subfig_letter = chr(ord(subfig_letter) + 1)

                replacement += '</div>\n'

                main_caption = find_caption_from_key(fig_dict, f"{chapter_num}_{figure_counter}")

                if caption_match:
                    replacement += f'<figcaption>Figure {chapter_num}.{figure_counter}: {main_caption}</figcaption>\n'
                replacement += '</figure>'

            else:
                replacement = process_figure(figure_env, chapter_num, figure_counter, '')

            content = content.replace(figure_env, replacement)

        figure_counter = 0  # Reset for next chapter

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)


def process_figure(figure_env, chapter_num, figure_counter, subfig_letter):
    include_graphics_match = re.search(r'\\includegraphics(\[.*?\])?\{(?P<filename>.*?)\}', figure_env)
    tikzpicture_env_match = re.search(r'(\\begin{tikzpicture}.*?\\end{tikzpicture})', figure_env, re.DOTALL)
    tikzfilename_match = re.search(r'\\tikzsetnextfilename\{(?P<filename>.*?)\}', figure_env)
    caption_match = re.search(r'\\caption\{(?P<caption>.*\})', figure_env)
    label_match = re.search(r'\\label\{(?P<label>.*\})', figure_env)
    subfigures = re.findall(r'(\\begin\{subfigure\}.*?\\end\{subfigure\})', figure_env, re.DOTALL)

    # dont need to convert pdfs to svg apart from tikz which is already done
    # if include_graphics_match:
    #     pdfname = include_graphics_match.group('filename')
    #     svgname = os.path.splitext(os.path.basename(pdfname))[0] + '.svg'

    #     if not os.path.isfile(py_to_svgs + f'{svgname}'): print(" # \n # No file: " + py_to_svgs + f"{svgname} \n #")
    #     #svg_file = os.path.join(py_to_svgs, os.path.splitext(pdfname)[0] + '.svg')
    #     #subprocess.run(['pdf2svg', os.path.join(py_to_pdfs, pdfname), svg_file])


    if include_graphics_match or tikzpicture_env_match:
        filename = include_graphics_match.group('filename') if include_graphics_match else tikzfilename_match.group('filename') if tikzfilename_match else 'missing'
        filename = os.path.splitext(os.path.basename(filename))[0] + '.svg'
        if not os.path.isfile(py_to_svgs + f'{filename}'): print(" # \n # No file: " + py_to_svgs + f"{filename} \n #")
        if label_match:
            if subfig_letter:
                fig_id = ' id="' + find_label_from_key(fig_dict, f"{chapter_num}_{figure_counter}_{subfig_letter}") + '"'
            else:
               fig_id = ' id="' + find_label_from_key(fig_dict, f"{chapter_num}_{figure_counter}") + '"'


        else:
            fig_id = ''

        if caption_match:
            caption_text = caption_match.group("caption")[:-1]
        else :
            caption_text = ""

        if "\\begin{subfigure}" in figure_env:
            figclass = 'class="subfigure"'
            caption = f"{subfig_letter}) {caption_text}"
        else:
            caption_text = find_caption_from_key(fig_dict, f"{chapter_num}_{figure_counter}")
            if find_label_from_key(fig_dict, f"{chapter_num}_{figure_counter}"):
                fig_id = ' id="' + find_label_from_key(fig_dict, f"{chapter_num}_{figure_counter}") + '"'
            else:
                fig_id = ''
            figclass = 'class="singlefigure"'
            caption = f"Figure {chapter_num}.{figure_counter}: {caption_text}"
        return f'<figure ' + figclass + fig_id +'>\n<img src="' + html_to_svgs + f'{filename}" loading="lazy">\n<figcaption>{caption}</figcaption>\n</figure>'

    else:
        return '*** svg figure missing ***'

###
def tikz2svg(input_directory, output_directory):
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    os.makedirs(output_directory, exist_ok=True)

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_directory, pdf_file)
        svg_path = os.path.join(output_directory, os.path.splitext(pdf_file)[0] + '.svg')

        if not os.path.exists(svg_path) or os.path.getmtime(pdf_path) > os.path.getmtime(svg_path):
            print(f"Converting: {pdf_file}")
            subprocess.run(['pdf2svg', pdf_path, svg_path], check=True)
            subprocess.run(['svgo.cmd', svg_path, '--precision=2'], check=True)


########################################################
# Page elements ########################################
########################################################
###

def to_roman(n):
        return {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI'}.get(int(n), str(n))

def create_toc(toc_dic):
    # --- 1. Helpers & Sorting ---
    keys = sorted(toc_dic.keys(), key=lambda x: [int(k) for k in x.split('_')])

    # --- 2. Build Data Tree ---
    tree = []
    # (We don't need p_ids or c_ids lists anymore)

    for k in keys:
        content_levels = k.split('_')
        item = toc_dic[k]

        if len(content_levels) == 1: # Part
            tree.append({'id': content_levels[0], 'title': item['title'], 'chaps': []})
        elif len(content_levels) == 2: # Chapter
            if tree: # Safety check
                tree[-1]['chaps'].append({'id': content_levels[1], 'title': item['title'], 'sects': []})
        elif len(content_levels) == 3: # Section
            if tree and tree[-1]['chaps']:
                tree[-1]['chaps'][-1]['sects'].append({'id': content_levels[2], 'title': item['title']})

    # --- 3. Generate HTML (No JS here) ---
    html = ['<div id="toc_container"><ul style="list-style:none; padding:0;">']
    arrow = '<span class="toc-arrow">&#9654;</span>'

    for p in tree:
        # Added class: 'toc-part-link'
        html.append(f'''<li>
            <a href="#part_{p['id']}_header"
               id="link_part_{p['id']}"
               class="toc-link toc-part-link"
               onclick="toggleView('part_{p['id']}')">
                {arrow} <b>Part {to_roman(p['id'])}. {p['title']}</b>
            </a>
            <ul id="part_{p['id']}_toc" class="toc-sublist toc-part-sublist">''') # Added class

        for c in p['chaps']:
            # Added class: 'toc-chapter-link'
            html.append(f'''<li>
                <a href="#part_{p['id']}_ch{c['id']}_header"
                   id="link_ch_{c['id']}"
                   class="toc-link toc-chapter-link"
                   onclick="toggleView('part_{p['id']}_ch{c['id']}')">
                    {arrow} <b>{c['id']}. {c['title']}</b>
                </a>
                <ul id="part_{p['id']}_ch_{c['id']}_toc" class="toc-sublist toc-chapter-sublist">''') # Added class

            for s in c['sects']:
                html.append(f'''<li>
                    <a href="#part_{p['id']}_ch{c['id']}_{s['id']}_header" class="toc-link">
                        {c['id']}.{s['id']} {s['title']}
                    </a>
                </li>''')
            html.append('</ul></li>')
        html.append('</ul></li>')

    html.append('</ul></div>')

    return "".join(html)

###
def create_terms(file_path):
    # 1. Read the whole file as a single string
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    output_lines = []

    # 2. Find all occurrences of \term{label}{term}{definition}
    # re.DOTALL allows the '.' to match newlines, handling multi-line definitions
    pattern = r'\\term\{(.+?)\}\{(.+?)\}\{(.+?)\}'

    for match in re.finditer(pattern, content, re.DOTALL):
        label, term, desc = match.groups()

        # 3. Clean and Format the description
        desc = desc.strip()
        desc = re.sub(r'\$(.*?)\$', r'\(\g<1>\)', desc).replace('<', '\\lt ').replace('>', '\\gt ')

        new_line = f'<div id="{label}" style="display: none;">\n<dt><b>{term}:</b>  </dt>\n<dd> {desc} </dd>\n</div>\n'
        output_lines.append(new_line)

    return output_lines


###
def find_matching_brace(text, start_index):
    brace_count = 0
    for i in range(start_index, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return i
    return -1

def create_dictionary_of_math_terms(file_path):
    """
    Parses the .tex file and returns a list of dictionaries containing
    raw_command, term_content, and definition_content.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    entries = []
    command_iterator = re.finditer(r"\\variableterm", file_content)

    for match in command_iterator:
        current_index = match.start()

        # 1. Extract Command (ID)
        start_brace = file_content.find("{", current_index)
        if start_brace == -1: continue
        end_brace = find_matching_brace(file_content, start_brace)
        if end_brace == -1: continue

        raw_command = file_content[start_brace + 1 : end_brace].strip()
        current_index = end_brace + 1

        # 2. Extract Term
        start_brace = file_content.find("{", current_index)
        if start_brace == -1: continue
        end_brace = find_matching_brace(file_content, start_brace)
        if end_brace == -1: continue

        term_content = file_content[start_brace + 1 : end_brace].strip()
        current_index = end_brace + 1

        # 3. Extract Definition
        start_brace = file_content.find("{", current_index)
        if start_brace == -1: continue
        end_brace = find_matching_brace(file_content, start_brace)
        if end_brace == -1: continue

        definition_content = file_content[start_brace + 1 : end_brace].strip()

        # Append to list
        entries.append({
            "raw_command": raw_command,
            "term_content": term_content,
            "definition_content": definition_content
        })

    return entries

def create_html_terms_element(entries):
    """
    Takes a list of dictionaries and returns the formatted HTML string.
    """
    if not entries:
        return ""

    html_string = '<dl id="math-glossary" style="display: none;">\n'

    for entry in entries:
        raw_command = entry['raw_command']
        term_content = entry['term_content']
        definition_content = entry['definition_content']

        # Process ID
        label_id = "var" + raw_command.replace("\\", "")

        # Process Term Display
        display_term = f"\\( ({term_content}) \\)"

        # Process Definition content (Latex replacements)
        definition_content = definition_content.replace('<', '\\lt ').replace('>', '\\gt ')
        definition_content = re.sub(r'\$(.*?)\$', r'\\(\1\\)', definition_content)

        # JS toggles between 'inline' (text-flow) and 'none'
        js_toggle = f"document.getElementById('{label_id}').style.display = document.getElementById('{label_id}').style.display == 'none' ? 'inline' : 'none';"

        html_line = (
            f'<div>\n'
            f'  <dt data-term="{label_id}" style="display: inline; cursor: pointer; font-weight: bold;" onclick="{js_toggle}">'
            f'{display_term} <b>:</b> '
            f'</dt>\n'
            f'  <dd id="{label_id}" style="display: none; margin: 0; padding-left: 5px;">'
            f'{definition_content}'
            f'</dd>\n'
            f'</div>\n'
        )

        html_string += html_line

    html_string += '</dl>'
    return html_string

def find_matching_brace(text, start_index):
    open_braces = 0
    for i in range(start_index, len(text)):
        if text[i] == '{':
            open_braces += 1
        elif text[i] == '}':
            open_braces -= 1
            if open_braces == 0:
                return i
    return -1

# Example Usage:
# output = parse_term_commands("Term_commands.tex")
# print(output)

###
def Eq_env_to_HTML(content, terms_data):

    # 1. Sort terms by length of raw_command (descending).
    sorted_terms = sorted(terms_data, key=lambda x: len(x['raw_command']), reverse=True)

    def process_equation_match(match):
        math_env = match.group(0)

        # --- A. Extract Label ---
        label_match = re.search(r'\\label\{(?P<label>.*\})', math_env)
        if label_match:
            raw_label = label_match.group("label")[:-1]
            clean_id = raw_label.replace(" ", "_").replace(":", "").replace("'", "_")
            id_attr = f' id="{clean_id}"'
        else:
            id_attr = ''

        # --- B. Clean Environment ---
        math_body = re.sub(r'\\label\{.*?\}', '', math_env, flags=re.DOTALL)

        math_body = re.sub(
            r'(\\begin\{equation\})\s*(.*?)\s*(\\end\{equation\})',
            lambda m: f"{m.group(1)}\n{re.sub(r'(?<!\\\\)\n', ' ', m.group(2))}\n{m.group(3)}",
            math_body,
            flags=re.DOTALL
        )

        # --- C. Process Terms ---
        found_data_ids = []

        for term in sorted_terms:
            raw_cmd = term['raw_command']
            replacement = term['term_content']

            cmd_pattern = re.compile(re.escape(raw_cmd) + r'(?![a-zA-Z])')

            if cmd_pattern.search(math_body):
                data_id = "var" + raw_cmd.replace("\\", "")
                found_data_ids.append(data_id)
                math_body = cmd_pattern.sub(lambda m: replacement, math_body)

        # --- D. Construct HTML ---
        data_terms_attr = ""
        if found_data_ids:
            data_terms_attr = f' data-terms="{" ".join(found_data_ids)}"'

        return f'<div class="interactive-equation" class="math"{id_attr}{data_terms_attr}>\n{math_body}\n</div>'

    pattern = r'(?<!<div class="math">\n)\\begin{equation}.*?\\end{equation}'

    return re.sub(pattern, process_equation_match, content, flags=re.DOTALL)


###
def inline_math_replacement(content, terms_data):

    # 1. Sort terms by length of raw_command (descending)
    sorted_terms = sorted(terms_data, key=lambda x: len(x['raw_command']), reverse=True)

    def process_inline_match(match):
        # Extract the full match (e.g., "\( \force \)")
        full_match = match.group(0)

        # Extract the inner content (e.g., " \force ")
        # We use group(1) from the regex below
        math_body = match.group(1)

        # 2. Iterate through terms and replace in this specific block
        for term in sorted_terms:
            raw_cmd = term['raw_command']
            replacement = term['term_content']

            # Regex: Match command + lookahead to ensure it ends the word
            cmd_pattern = re.compile(re.escape(raw_cmd) + r'(?![a-zA-Z])')

            if cmd_pattern.search(math_body):
                # Use lambda for replacement to avoid 'bad escape' errors
                math_body = cmd_pattern.sub(lambda m: replacement, math_body)

        # Reconstruct the inline math string
        return f"\\({math_body}\\)"

    # Regex to find \( ... \)
    # \\\( matches literal \(
    # (.*?) matches content lazily (capturing group 1)
    # \\\) matches literal \)
    pattern = r'\\\((.*?)\\\)'

    # re.DOTALL allows the dot (.) to match newlines, in case inline math spans lines
    return re.sub(pattern, process_inline_match, content, flags=re.DOTALL)

###
def replace_refs(input_string):
    # This pattern matches \eqref{} and captures the content inside the brackets
    pattern_ref_eq = r'\\eqref\{(.*?)\}'
    pattern_ref_fig = r'\\ref\{(.*?fig.*?)\}'
    pattern_ref_toc = r'\\ref\{(.*?)\}'

    # This function will be used to replace each match
    def replacer_ref_eq(match):
        id = match.group(1).replace(" ", "_").replace(":","").replace("'","_")
        eq_number =  (find_key_from_label(eq_dict, id) or "").replace("_", ".")
        # Replace with a span element that shows a div with the matched id on hover
        return f'<span class="ref_eq" onmouseover="copyContent(\'{id}\',\'equation_hover\'); " onmouseout="deleteContent(\'equation_hover\');">({eq_number})</span>'
    def replacer_ref_fig(match):
        id = match.group(1).replace(" ", "_").replace(":","").replace("'","_")
        fig_num =  (find_key_from_label(fig_dict, id) or "").replace("_", ".")
        # Replace with a span element that shows a div with the matched id on hover
        return f'<span class="ref_fig" onmouseover="copyContent(\'{id}\',\'fig_hover\');" onmouseout="deleteContent(\'fig_hover\');">{fig_num}</span>'
    def replacer_ref_toc(match):
        id = match.group(1).replace(" ", "_").replace(":","").replace("'","_")
        toc_num = (find_key_from_label(toc_dict, id) or "").replace("_", ".")

        if '.' not in toc_num: # part
            return f'<a href="#part_{toc_num}_header" class="ref_toc" >{toc_num}</a>'
        else:
            # for "Chapter" (e.g., "1.2.3" -> "2.3")
            toc_num_sep = toc_num.split(".")
            display_num = ".".join(toc_num_sep[1:])
            href = display_num.replace(".", "_")
            part_num = ".".join(toc_num_sep[:1])
            return f'<a href="#part_{part_num}_ch{href}_header" class="ref_toc" >{display_num}</a>' #todo need way for click to load chapter if ref is to a hidden chapter
               #todo <a href="#part_{part_num}_ch{c['id']}_wrap" id="link_ch_{c['id']}" class="toc-link" onclick="toggleView('ch', '{c['id']}')">

    # Use re.sub to replace each match in the input string
    output_string = re.sub(pattern_ref_eq , replacer_ref_eq, input_string)
    output_string = re.sub(pattern_ref_fig, replacer_ref_fig, output_string)
    output_string = re.sub(pattern_ref_toc, replacer_ref_toc, output_string) # must be after fig replacer


    return output_string

###
def process_bib_and_cites(bib_path, tex_path):
    # 1. Load Files
    with open(bib_path) as f: bib_raw = f.read()
    with open(tex_path) as f: tex_raw = f.read()

    # 2. Parse BibTeX (Unchanged)
    db = {}
    for chunk in bib_raw.split('@')[1:]:
        m_head = re.match(r'(\w+)\s*\{\s*([^,]+),', chunk)
        if not m_head: continue
        fields = {k.lower(): (v1 or v2 or v3).strip()
                  for k, v1, v2, v3 in re.findall(r'(\w+)\s*=\s*(?:\{(.+?)\}|"(.+?)"|(\d+))', chunk, re.DOTALL)}
        db[m_head.group(2).strip()] = {'type': m_head.group(1).lower(), 'lbl': m_head.group(2).strip(), **fields}

    # 3. Process LaTeX (Updated for Bi-directional Linking)
    c_map, counter = {}, 1

    def sub_cite(m):
        nonlocal counter
        links = []
        for k in [x.strip() for x in m.group(1).split(',')]:
            if k in db:
                if k not in c_map:
                    c_map[k] = counter
                    db[k]['cid'] = counter
                    counter += 1

                # UPDATE: Added id='cite-...' for the back-link
                # We point href to '#ref-...' which will be the ID in the bibliography
                links.append(f'<a href="#ref-{k}" id="cite-{k}" class="citation-link">{c_map[k]}</a>')
            else:
                links.append(f"{k}?")
        return f"[{', '.join(links)}]"

    with open(tex_path, 'w') as f: f.write(re.sub(r'\\cite\{(.+?)\}', sub_cite, tex_raw))

    # 4. Generate HTML
    html = ['<section id="references" aria-labelledby="refs-title">\n<h4 id="refs-title">References</h4>\n<ol class="bibliography-list">\n']

    sorted_entries = sorted([x for x in db.values() if 'cid' in x], key=lambda x: x['cid'])

    for e in sorted_entries:
        # Clean Authors (Remove {} braces)
        clean_author = e.get('author', 'Unknown').replace('{', '').replace('}', '')
        aus = [n.split(',')[1].strip() + " " + n.split(',')[0].strip() if ',' in n else n
               for n in clean_author.split(' and ')]
        auth = ", ".join(aus).replace('others', 'et al.')

        # Format Date
        d_str = e.get('year', '')
        if 'date' in e:
            dt = datetime.strptime(e['date'], '%Y-%m-%d')
            d_str = f"{dt.strftime('%b.')} {dt.day}, {dt.year}"

        s = f'<li id="ref-{e["lbl"]}">'

        title = e.get('title', '')

        if e['type'] == 'article':
            # Articles: Quotes, No Italics
            # We remove <cite> here to prevent italics
            s += f'{auth}. “{title}”.'
        else:
            # Books, Misc, Online: Italics, No Quotes
            # We use <em> (or <cite>) to apply italics
            s += f'{auth}. <em>{title}</em>.'
        # -----------------------------------------

        if e['type'] == 'article':
            vol = f"{e.get('volume','')}" + (f".{e['number']}" if 'number' in e else "")
            s += f" In: <em>{e.get('journal','')}</em> {vol} ({d_str})"
        else:
            pub = [x for x in [e.get('publisher'), e.get('organization'), d_str] if x]
            s += f" {', '.join(pub)}."

            if 'url' in e:
                s += f' <span  style="font-family: monospace; font-size: 0.7rem;">URL:</span> <a href="{e["url"]}" class="bib-url" target="_blank" rel="noopener">{e["url"]}</a>'
                if 'urldate' in e: s += f" (visited on {e['urldate']})."

        if 'pages' in e: s += f", pp. {e['pages'].replace('--', '–')}."

        s += f' <a href="#cite-{e["lbl"]}" aria-label="Back to citation" style="text-decoration:none">↩</a>'
        s += "</li>\n"
        html.append(s)

    html.append("</ol>\n</section>\n")
    return "".join(html)



###
def create_dictionary_of_content(filepath):
    structure_dict = {}
    counters = {
        "part": 0,
        "chapter": 0,
        "section": 0,
        "subsection": 0,
        "subsubsection": 0
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r"\\(part|chapter|section|subsection|subsubsection)(?:\[([^\]]*)\])?\s*\{([^}]+)\}\s*(?:\\label\{([^}]+)\})?", line)

            if match:
                level = match.group(1)
                short_title = match.group(2).strip() if match.group(2) else None
                title = match.group(3).strip()
                label = match.group(4).replace(" ", "_").replace(":","").replace("'","_") if match.group(4) else None

                # Replace title with short_title if short_title exists
                if short_title:
                    title = short_title

                if level == "part":
                    counters["part"] += 1
                    structure_dict[f"{counters['part']}"] = {"title": title, "label": label}

                elif level == "chapter":
                    counters["chapter"] += 1
                    counters["section"] = 0
                    counters["subsection"] = 0
                    counters["subsubsection"] = 0
                    structure_dict[f"{counters['part']}_{counters['chapter']}"] = {"title": title, "label": label}

                elif level == "section":
                    counters["section"] += 1
                    counters["subsection"] = 0
                    counters["subsubsection"] = 0
                    structure_dict[f"{counters['part']}_{counters['chapter']}_{counters['section']}"] = {"title": title, "label": label}

                elif level == "subsection":
                    counters["subsection"] += 1
                    counters["subsubsection"] = 0
                    structure_dict[f"{counters['part']}_{counters['chapter']}_{counters['section']}_{counters['subsection']}"] = {"title": title, "label": label}

                elif level == "subsubsection":
                    counters["subsubsection"] += 1
                    structure_dict[f"{counters['part']}_{counters['chapter']}_{counters['section']}_{counters['subsection']}_{counters['subsubsection']}"] = {"title": title, "label": label}

    return structure_dict

def create_dictionary_of_figures(latex_file):
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    figure_data = {}
    chapter_number = 0
    figure_number = 0

    chapters = re.split(r'\\chapter\{', content)[1:]

    for chapter_content in chapters:
        chapter_number += 1
        figure_number = 0

        figure_matches = re.findall(r'\\begin\{figure\}(.*?)\\end\{figure\}', chapter_content, re.DOTALL)

        for figure_match in figure_matches:
            figure_number += 1

            # Remove subfigure environments from figure_match
            temp_figure_match = re.sub(r'\\begin\{subfigure\}.*?\\end\{subfigure\}', '', figure_match, flags=re.DOTALL)

            # Now search for caption and label in temp_figure_match
            figure_caption = ""
            figure_title = ""
            figure_label = ""

            # Function to find matching bracket
            def find_matching_bracket(text, open_bracket_pos):
                stack = []
                for i in range(open_bracket_pos, len(text)):
                    if text[i] == '{':
                        stack.append('{')
                    elif text[i] == '}':
                        if stack:
                            stack.pop()
                        if not stack:
                            return i
                return -1

            # Search for the main figure caption
            caption_match = re.search(r'\\caption\s*\{', temp_figure_match)
            if caption_match:
                open_bracket_pos = caption_match.end() - 1
                close_bracket_pos = find_matching_bracket(temp_figure_match, open_bracket_pos)
                if close_bracket_pos != -1:
                    figure_caption = temp_figure_match[open_bracket_pos + 1:close_bracket_pos].strip()

                    # Extract the figure title from the caption
                    title_match = re.search(r'\\textbf\{([^}]*?)\}', figure_caption)
                    if title_match:
                        figure_title = title_match.group(1).strip()

            # Find label in temp_figure_match
            label_match = re.search(r'\\label\{([^}]*?)\}', temp_figure_match)
            if label_match:
                figure_label = label_match.group(1).replace(" ", "_").replace(":","").replace("'","_")

            figure_id = f"{chapter_number}_{figure_number}"
            figure_data[figure_id] = {
                "title": figure_title,
                "label": figure_label,
                "caption": figure_caption
            }

            # Now process subfigures
            subfigure_matches = re.findall(r'\\begin\{subfigure\}(.*?)\\end\{subfigure\}', figure_match, re.DOTALL)

            for i, subfigure_match in enumerate(subfigure_matches):
                subfigure_letter = chr(ord('a') + i)

                # Find subfigure caption and label
                subfigure_title = ""
                subfigure_label = ""
                subfigure_caption = ""

                subfigure_caption_match = re.search(r'\\caption\s*\{', subfigure_match)
                if subfigure_caption_match:
                    open_bracket_pos = subfigure_caption_match.end() - 1
                    close_bracket_pos = find_matching_bracket(subfigure_match, open_bracket_pos)
                    if close_bracket_pos != -1:
                        subfigure_caption = subfigure_match[open_bracket_pos + 1:close_bracket_pos].strip()

                        # Extract the subfigure title from the caption
                        subfigure_title_match = re.search(r'\\textbf\{([^}]*?)\}', subfigure_caption)
                        if subfigure_title_match:
                            subfigure_title = subfigure_title_match.group(1).strip()

                # Find label in subfigure_match
                label_match = re.search(r'\\label\{([^}]*?)\}', subfigure_match)
                if label_match:
                    subfigure_label = label_match.group(1).replace(" ", "_").replace(":","").replace("'","_")

                subfigure_id = f"{chapter_number}_{figure_number}_{subfigure_letter}"
                figure_data[subfigure_id] = {
                    "title": subfigure_title,
                    "label": subfigure_label,
                    "caption": subfigure_caption
                }

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
                equation_label = label_match.group(1).replace(" ", "_").replace(":","").replace("'","_")

            equation_id = f"{chapter_number}_{equation_number}"
            equation_data[equation_id] = {"label": equation_label}  # Store as dictionary

    return equation_data

###
def find_key_from_label(data_dict, target_label):
    for key, value in data_dict.items():
        if value['label'] == target_label:
            return key
    print("label: ", target_label, " does not have a key" )
    return None

###
def find_label_from_key(data_dict, target_key):
    if target_key in data_dict:
        return data_dict[target_key]['label']
    else:
        print("Key: ", target_key, " does not have a label" )
        return None

###
def find_caption_from_key(data_dict, target_key):
    if target_key in data_dict:
        return data_dict[target_key]['caption']
    else:
        print("Key: ", target_key, " does not have a caption" )
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
def make_page(input_file, output_file, toc_file, content_file, Defs_file, Math_Terms_lines, bib_lines):
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
                file.write('<a href="' + html_to_pdfs + '" style="padding-top: 5px; color: black;"><b>&#11015; PDF</b></a><br>\n')
            elif '[Insert Topic Name]' in line:
                file.write(Topic_Name)
            elif '[Insert Bib]' in line:
                for line in bib_lines:
                    file.write(line)
            else:
                file.write(line)

########################################################
# Checks ###############################################
########################################################
###

def find_leftover_latex(html_file):
    print(f"Scanning {html_file}...")
    found, bugs = set(), 0
    stop_marker = None

    with open(html_file, 'r', encoding='utf-8') as f, open("latex_still_in_html.txt", 'w', encoding='utf-8') as out:
        for i, line in enumerate(f, 1):
            # check for start of block if not in one
            if not stop_marker:
                if '<script' in line: stop_marker = '</script>'
                elif '<style' in line: stop_marker = '</style>'
                elif r'\begin{equation}' in line: stop_marker = r'\end{equation}'

            # If we are inside a block, check if it ends here
            if stop_marker:
                if stop_marker in line: stop_marker = None
                continue

            # 2. Clean inline math to avoid false positives
            clean = re.sub(r'\\\(.*?\\\)', '', line)

            # 3. Find LaTeX commands, Matches \cmd and optional {arg}.
            matches = re.findall(r"\\([a-zA-Z]+)(\{[^}]*\})?", clean)
            curr_bugs = [f"\\{c}{a}" if (c in ['begin','end'] and a) else f"\\{c}" for c, a in matches]

            # 4. Find Stray Braces (by removing the valid commands we just found)
            clean_no_cmds = re.sub(r"\\([a-zA-Z]+)(\{[^}]*\})?", '', clean)
            if any(b in clean_no_cmds for b in '{}'):
                curr_bugs.append("STRAY_BRACES")

            # 5. Log if bugs found
            if curr_bugs:
                bugs += 1
                found.update(c for c in curr_bugs if c != "STRAY_BRACES")
                out.write(f"Line {i}: {line.strip()}\n   >>> Found: {curr_bugs}\n")
    if bugs == 0:
        print("- no leftover latex")
    else:
        print(f"Lines with bugs: {bugs}\nUnique commands: {sorted(found)}\nSee latex_still_in_html.txt")

###
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

### checks
def check_latex_href_links(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        urls = re.findall(r'\\href\{([^}]+)\}', f.read())

    # Filter/deduplicate
    links = set(u for u in urls if u.startswith(('http', 'www')))
    print(f"Checking {len(links)} web links...")

    def is_link_working(url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5):
                return True
        except urllib.error.URLError as e:
            print(f"❌ [{getattr(e, 'code', 'Connection Error')}] {url}")
            return False

    if all(is_link_working(url) for url in links):
        print("- all external links work")

###
from html.parser import HTMLParser
class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), set()

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.add(d['id'])
        if tag == 'a' and d.get('href', '').startswith('#'):
            target = d['href'][1:]
            if target: self.links.add(target)

###################################################################################
###################################################################################
###################################################################################
Latex_File = 'Latex_content.txt'

with open(py_to_main_tex, 'rb') as src, open(Latex_File, 'wb') as dst:
    dst.write(src.read())

# to do first to avoid conflicts:
remove_comments(Latex_File)
replace(Latex_File,'<<', r'\\ll ')
replace(Latex_File,'>>', r'\\gg ')
replace(Latex_File,'<', r'\\lt ')
replace(Latex_File,'>', r'\\gt ')

# Create dictionaries
toc_dict = create_dictionary_of_content(Latex_File)
fig_dict = create_dictionary_of_figures(Latex_File)
eq_dict  = create_dictionary_of_equations(Latex_File)
var_dict = create_dictionary_of_math_terms(py_to_term_comands)
# check for duplicate lables
check_duplicate_labels(toc_dict)
check_duplicate_labels(fig_dict)
check_duplicate_labels(eq_dict)

bib_lines = process_bib_and_cites(py_to_bib, Latex_File)


# Call the function with your input and output file paths
Figures_to_HTML(Latex_File)
tikz2svg(py_to_tikz, py_to_svgs)
replace_blank_lines(Latex_File)
replace(Latex_File, r'\$(.*?)\$', r'\(\1\)')
replace(Latex_File, 'mhl', 'bbox[#fff9cf, 10px, border-radius: 10px; border: 3px solid black]')
replace(Latex_File, r'\\begin\{mainpoints\}', '<div style="border: 3px solid black; padding-right: 20px; padding-left: 10px; background-color: #f0f0f0; border-radius: 10px;">\n\t<ol>')
replace(Latex_File, r'\\end\{mainpoints\}', '\t</ol>\n</div>')
replace(Latex_File, r'\\begin\{itemize\}', '<ul>')
replace(Latex_File, r'\\end\{itemize\}', '</ul>')
replace(Latex_File, r'\\begin\{note\}', '<blockquote class="note">')
replace(Latex_File, r'\\end\{note\}', '</blockquote>')
replace(Latex_File, r'\\begin\{derivation\}', '<div class="derivation">')
replace(Latex_File, r'\\end\{derivation\}', '</div>')
replace(Latex_File, r'\\Vec', r'\\mathbf')
replace(Latex_File, r'\\noindent', '')
replace(Latex_File, r'\\protect', '')
replace(Latex_File, r'\\textbf\{(.*?)\}', r'<b>\1</b>')
replace(Latex_File, r'\\hyperlink\{(.*?)\}\{(.*?)\}', "<span onmouseover=\"document.getElementById('\\g<1>').style.display='block'\" onmouseout=\"document.getElementById('\\g<1>').style.display='none'\">\\g<2></span>")
replace(Latex_File, r'\\href\{(.*?)\}\{(.*?)\}', '<a style="color: black" href="\\g<1>" target="_blank" rel="noopener noreferrer">\\g<2></a>')
replace(Latex_File, r'\\scalebox{0.5}{R}', 'R')
replace(Latex_File, r'\\AA', "Å") #'Å')
replace(Latex_File, r'\\newline', '<br>\n')
replace(Latex_File, r'\\mainmatter', '')
replace(Latex_File,r'\\input\{.*?\}', '')
replace(Latex_File,r'\\printbibliography\[.*?\]', '')
colorbox_replace(Latex_File)
replace(Latex_File, r"\\iffalse\s*animated_fig\{(.*?)\}\s*\\fi", '<button class="fig-button" data-src="animated_figs/\\1"><b>View Animated Figure</b></button>')
replace(Latex_File,r'\\fi', '')
########################################################## bib_lines = bib_to_html(py_to_bib)

wrap_content(Latex_File)

# Read the LaTeX file
with open(Latex_File, 'r', encoding='utf-8') as file:
    latex_content = file.read()

# Convert to HTML headings
main_content = latex_content
main_content = Eq_env_to_HTML(main_content,var_dict)
main_content = inline_math_replacement(main_content,var_dict)
main_content = replace_refs(main_content)
main_content += '\n'
main_content =  re.sub(r'\\label\{.*?\}', '', main_content)

# Call the function with your HTML file
toc = create_toc(toc_dict)
vars = create_html_terms_element(var_dict)
defs = create_terms(py_to_defs)

make_page(py_to_page_structure, py_to_output_page, toc, main_content, defs, vars, bib_lines)

find_leftover_latex(py_to_output_page)
check_ids_for_spaces(py_to_output_page)
check_latex_href_links(py_to_main_tex)
# check internal href links
parser = Checker()
with open(py_to_output_page, 'r', encoding='utf-8') as f:
    parser.feed(f.read())

broken = parser.links - parser.ids  # Set subtraction finds what's in links but NOT in ids
print(f"Broken links: {broken}" if broken else "All internal links valid!")

os.remove(Latex_File)