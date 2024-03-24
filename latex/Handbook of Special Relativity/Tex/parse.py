import re

text = 'Main_matter.tex'

def replace_strings(text, strings):
    def repl(match):
        equation_text = match.group(0)
        for string in strings:
            equation_text = re.sub(rf'(?<!\\)\b{string}\b', f'{{{string}}}', equation_text)
        return equation_text

    return re.sub(r'\\begin{equation}.*?\\end{equation}', repl, text, flags=re.DOTALL)

# Usage:
with open(text, 'r') as file:
    content = file.read()

strings_to_replace = ['c', 'v', '<S>']  # Add your strings here
new_content = replace_strings(content, strings_to_replace)

with open(text, 'w') as file:
    file.write(new_content)



####
# confuses the c in \frac
# could maybe exclude instances of a blackslash \ followed by just letters until there is a space or a none a-z or A-Z character
# but not from when findind \tau or \gamma

# also need for $ $ environment

# at end of parcing replace instances of {{ and }} with { and }

# to be careful with u and u_p and primes, i.e. t and t'