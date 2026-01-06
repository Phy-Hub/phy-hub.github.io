import re
import os

# --- Configuration ---
INPUT_FILE = 'Main_Matter.tex'
OUTPUT_FILE = 'Main_Matter_processed.tex'
COMMANDS_FILE = 'Terms/termcommands.tex'

# 1. WRAPPER COMMANDS
# Commands that are PART of the variable name and MUST capture their argument.
WRAPPER_COMMANDS = {
    'underline', 'hat', 'vec', 'bar', 'dot', 'ddot', 'tilde',
    'mathbf', 'boldsymbol', 'mathcal', 'mathbb', 'mathrm', 'bm'
}

# 2. IGNORE COMMANDS
# Commands to strictly ignore (Structure/Operators).
IGNORE_COMMANDS = {
    'begin', 'end', 'split', 'equation', 'align', 'pmatrix', 'bmatrix', 'vmatrix',
    'left', 'right', 'label', 'ref', 'cite', 'color', 'space', 'vspace', 'hspace',
    'frac', 'dfrac', 'tfrac', 'sum', 'prod', 'int', 'partial', 'sqrt',
    'cdot', 'times', 'div', 'pm', 'mp',
    'leq', 'geq', 'neq', 'approx', 'equiv', 'sim', 'll', 'gg', 'mhl',
    'rightarrow', 'leftarrow', 'Rightarrow', 'Leftarrow', 'to', 'in', 'subset',
    'cup', 'cap', 'setminus', 'infty', 'lim', 'quad', 'qquad',
    'sin', 'cos', 'tan', 'exp', 'ln', 'log', 'det', 'max', 'min', 'bigg', 'big','Big','sinb','cosb'
}

# 3. TEXT COMMANDS
# Commands whose content is usually text, BUT we must check if they contain embedded math ($...$)
TEXT_COMMANDS = {'text', 'mbox', 'label', 'ref', 'cite', 'url', 'href', 'color'}

def mask_comments(text):
    """
    Replaces comments with spaces, preserving indices.
    """
    lines = text.split('\n')
    masked_lines = []
    for line in lines:
        idx = -1
        is_escaped = False
        for i, char in enumerate(line):
            if char == '\\':
                is_escaped = not is_escaped
            elif char == '%':
                if not is_escaped:
                    idx = i
                    break
                is_escaped = False
            else:
                is_escaped = False

        if idx != -1:
            line = line[:idx] + ' ' * (len(line) - idx)
        masked_lines.append(line)
    return '\n'.join(masked_lines)

def get_balanced_text(text, start_index):
    """
    Finds balanced { ... }. Returns (content_with_braces, end_index).
    """
    if start_index >= len(text) or text[start_index] != '{':
        return "", start_index

    depth = 0
    for i in range(start_index, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start_index:i+1], i + 1
    return "", start_index

def get_math_regions(text):
    """
    Finds regions strictly inside $...$ or \begin{equation}...\end{equation}.
    """
    regions = []

    # 1. Display Math
    eq_pattern = re.compile(r'(\\begin\{equation\}.*?\\end\{equation\})', re.DOTALL)
    for match in eq_pattern.finditer(text):
        regions.append({'start': match.start(), 'end': match.end()})

    # 2. Inline Math (masking display math first)
    temp_text = list(text)
    for r in regions:
        for i in range(r['start'], r['end']):
            temp_text[i] = ' '
    temp_text_str = "".join(temp_text)

    inline_pattern = re.compile(r'(?<!\\)\$(.*?)(?<!\\)\$', re.DOTALL)
    for match in inline_pattern.finditer(temp_text_str):
        regions.append({'start': match.start(), 'end': match.end()})

    return sorted(regions, key=lambda x: x['start'])

def check_suffix(text, base, start_index):
    """
    Checks for suffixes: Subscripts (_), Primes ('), but ignores Superscripts (^).
    Handles complex chains like x'_i or x''_i.
    """
    current_term = base
    i = start_index
    n = len(text)

    while i < n:
        if text[i].isspace():
            i += 1
            continue

        # 1. Handle Prime (')
        if text[i] == "'":
            current_term += "'"
            i += 1
            continue

        # 2. Handle Subscript (_)
        if text[i] == '_':
            i += 1
            suffix = "_"
            if i < n:
                if text[i] == '{':
                    block, end = get_balanced_text(text, i)
                    suffix += block
                    i = end
                elif text[i] == '\\':
                    # Command subscript: _\sigma
                    j = i + 1
                    cmd = "\\"
                    while j < n and (text[j].isalpha() or text[j] == '@'):
                        cmd += text[j]
                        j += 1
                    # Handle single symbol command (like _\Phi vs _\,)
                    if len(cmd) == 1 and j < n:
                         cmd += text[j]
                         j += 1
                    suffix += cmd
                    i = j
                else:
                    suffix += text[i]
                    i += 1
            current_term += suffix
            continue

        # 3. Handle Superscript (^) -> SKIP
        if text[i] == '^':
            i += 1
            if i < n:
                if text[i] == '{':
                    _, end = get_balanced_text(text, i)
                    i = end
                elif text[i] == '\\':
                     j = i + 1
                     while j < n and (text[j].isalpha() or text[j] == '@'): j += 1
                     i = j
                else:
                    i += 1
            continue

        # If none of the above, suffix chain ends
        break

    return current_term, i

def parse_variables(math_str):
    candidates = set()
    i = 0
    n = len(math_str)

    # Skip chars: structure, operators, formatting.
    # NOTE: We skip '{' and '}' here to allow finding x inside {x}.
    SKIP_CHARS = set("={}()[]+-*/!,.<>|;:?^& \t\n\r")

    while i < n:
        char = math_str[i]

        if char in SKIP_CHARS:
            i += 1
            continue

        # --- COMMANDS ---
        if char == '\\':
            j = i + 1
            cmd_name = ""
            while j < n and (math_str[j].isalpha() or math_str[j] == '@'):
                cmd_name += math_str[j]
                j += 1

            full_cmd = math_str[i:j]

            if not cmd_name:
                i = j + 1 if j < n else j
                continue

            # A. Wrapper Commands (capture argument as part of var)
            if cmd_name in WRAPPER_COMMANDS:
                k = j
                while k < n and math_str[k].isspace(): k += 1

                if k < n and math_str[k] == '{':
                    brace_content, end_idx = get_balanced_text(math_str, k)
                    base = math_str[i:end_idx]
                    term, new_i = check_suffix(math_str, base, end_idx)
                    candidates.add(term)
                    i = new_i
                    continue
                elif k < n and math_str[k] == '\\':
                     m = k + 1
                     while m < n and math_str[m].isalpha(): m += 1
                     base = math_str[i:m]
                     term, new_i = check_suffix(math_str, base, m)
                     candidates.add(term)
                     i = new_i
                     continue
                elif k < n:
                    base = math_str[i:k+1]
                    term, new_i = check_suffix(math_str, base, k+1)
                    candidates.add(term)
                    i = new_i
                    continue

            # B. Ignore Commands (skip command name)
            if cmd_name in IGNORE_COMMANDS:
                i = j
                continue

            # C. Text Commands (CHECK FOR INNER MATH)
            if cmd_name in TEXT_COMMANDS:
                k = j
                while k < n and math_str[k].isspace(): k += 1
                if k < n and math_str[k] == '{':
                    brace_content, end_idx = get_balanced_text(math_str, k)

                    # RECURSION CHECK: Does this text block contain math delimiters?
                    # Remove the outer braces for the check
                    inner_text = brace_content[1:-1]

                    # Look for $...$ inside
                    inner_math_matches = re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$', inner_text)
                    if inner_math_matches:
                        for m in inner_math_matches:
                            # Recursively parse the math found inside the text
                            inner_vars = parse_variables(m)
                            for iv in inner_vars:
                                candidates.add(iv)

                    i = end_idx
                else:
                    i = j
                continue

            # D. Standard Variable Commands (\gamma)
            term, new_i = check_suffix(math_str, full_cmd, j)
            candidates.add(term)
            i = new_i
            continue

        # --- LETTERS ---
        if char.isalpha():
            term, new_i = check_suffix(math_str, char, i+1)
            candidates.add(term)
            i = new_i
            continue

        i += 1

    return list(candidates)

def process_tex():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        original_text = f.read()

    print("--- 1. Masking Comments ---")
    masked_text = mask_comments(original_text)

    print("--- 2. Scanning for Math Regions ---")
    regions = get_math_regions(masked_text)

    print("--- 3. Extracting Variables ---")
    all_candidates = set()

    for reg in regions:
        content_masked = masked_text[reg['start']:reg['end']]

        if content_masked.startswith('$') and content_masked.endswith('$'):
            search_content = content_masked[1:-1]
        elif content_masked.startswith(r'\begin'):
            search_content = content_masked
        else:
            search_content = content_masked

        vars_found = parse_variables(search_content)
        for v in vars_found:
            all_candidates.add(v)

    # Sort by Length Descending
    sorted_candidates = sorted(list(all_candidates), key=len, reverse=True)

    replacements = {}
    definitions = []

    print(f"Found {len(sorted_candidates)} potential variables.")
    print("-" * 50)

    for term in sorted_candidates:
        print(f"Variable:  {term}")
        new_text = input(f"Replace with (Enter to skip): ").strip()

        if new_text:
            replacements[term] = new_text
            definitions.append(f"\\newcommand{{{new_text}}}{{{term}}}")

    print("-" * 50)
    print("Applying replacements...")

    final_text = ""
    last_idx = 0

    for reg in regions:
        final_text += original_text[last_idx:reg['start']]
        math_block_orig = original_text[reg['start']:reg['end']]

        block_lines = math_block_orig.split('\n')
        processed_lines = []

        for line in block_lines:
            # Mask comment on line
            idx = -1
            is_escaped = False
            for i, c in enumerate(line):
                if c == '\\': is_escaped = not is_escaped
                elif c == '%':
                    if not is_escaped:
                        idx = i
                        break
                    is_escaped = False
                else: is_escaped = False

            if idx != -1:
                code_part = line[:idx]
                comment_part = line[idx:]
            else:
                code_part = line
                comment_part = ""

            for term, new_cmd in replacements.items():
                if term in code_part:
                    code_part = code_part.replace(term, new_cmd)

            processed_lines.append(code_part + comment_part)

        final_text += '\n'.join(processed_lines)
        last_idx = reg['end']

    final_text += original_text[last_idx:]

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_text)

    with open(COMMANDS_FILE, 'w', encoding='utf-8') as f:
        f.write("% Auto-generated variable definitions\n")
        for line in definitions:
            f.write(line + "\n")

    print(f"Success! Processed file saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_tex()