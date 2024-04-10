import re

###
# be careful this may break the latex
###

###
# maybe change manually and use this to check for missed bracketing
###

text = 'Main_matter.tex'

def replace_vars(text, strings):
    def repl(match):
        equation_text = match.group(0)
        for string in strings:
            equation_text = re.sub(rf'(?<!\\)\b{string}\b', f'{{{string}}}', equation_text)
        return equation_text

    # Modify the regular expression to also match text between dollar signs
    return re.sub(r'(\\begin{equation}.*?\\end{equation}|\$.*?\$)', repl, text, flags=re.DOTALL)

def replace_greek_vars(text, strings):
    def repl(match):
        equation_text = match.group(0)
        for string in strings:
            equation_text = re.sub(rf'{string}', f'{{{string}}}', equation_text)
        return equation_text

    # Modify the regular expression to also match text between dollar signs
    return re.sub(r'(\\begin{equation}.*?\\end{equation}|\$.*?\$)', repl, text, flags=re.DOTALL)

# Usage:
with open('Main_matter.tex', 'r') as file:
    content = file.read()

strings_to_replace = ["c", "v"]#, "<S>'"]  # Add your strings here
new_content = replace_vars(content, strings_to_replace)

with open('Main_matter.tex', 'w') as file:
    file.write(new_content)




####
# confuses the c in \frac
# could maybe exclude instances of a blackslash \ followed by just letters until there is a space or a none a-z or A-Z character
# but not from when findind \tau or \gamma

# also need for $ $ environment

# at end of parcing replace instances of {{ and }} with { and } but only if surround the variable though, as other times this is true

# to be careful with u and u_p and primes, i.e. t and t'