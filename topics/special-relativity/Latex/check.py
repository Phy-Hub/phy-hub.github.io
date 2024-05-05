import os
import re

def parse_tex_files(pattern, error_message, directories=['Tex', 'Tex/Terms']):
    regex = re.compile(pattern, re.DOTALL)
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.tex'):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        matches = list(regex.finditer(content))
                        for match in matches:
                            start = match.start()
                            line_num = content.count('\n', 0, start) + 1
                            print("\033[42m\033[30m {}\033[00m" .format(f"{file}, line: {line_num} : {error_message}"))

# Call the function with your pattern and error message
parse_tex_files('\n\n\n', 'Two newlines in a row')
