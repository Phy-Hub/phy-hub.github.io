import os
import re

### checks to add
# check variables from variable file are in brackets {}
# check all greek letters are in their own brackets i.e. {\gammma} and i {} is part of function maybe add second {} i.e. \frac{1}{{\gamma}}
# formatting of all things in snippets, change snippet names of snippets to the regex used to find matches to check

def parse_tex_files(pattern_replacement_error_pairs, directories=['Tex', 'Tex/Terms']):
    for pattern, replacement, error_message in pattern_replacement_error_pairs:
        regex = re.compile(pattern, re.DOTALL)
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.tex'):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r') as f:
                            content = f.read()
                        matches = list(regex.finditer(content))
                        for match in matches:
                            start = match.start()
                            line_num = content.count('\n', 0, start) + 1
                            print("\033[42m\033[30m {}\033[00m" .format(f"{file}, line: {line_num} : {error_message}"))
                        if replacement is not None:
                            new_content = regex.sub(replacement, content)
                            with open(filepath, 'w') as f:
                                f.write(new_content)

# Call the function with your patterns, replacements, and error messages
patterns = [
    ('\n\n\n', '\n\n', 'Two empty lines replaced with one'),
    (r'\\begin\{figure\}.*?\\end\{figure\}',None,'figure found')
]

#parse_tex_files(patterns)

### when checking for a new line after all . check for e.g. or i.e.



def print_long_lines(filename):
    with open(filename, 'r') as file:
        for i, line in enumerate(file, start=1):
            if len(line) > 240: # average word length (6) * 40 words
                print(f"Line {i}: {len(line)}")

print_long_lines("Tex/Main_matter.tex")
