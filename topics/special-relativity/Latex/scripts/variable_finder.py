import re
import os

# --- Configuration ---
INPUT_FILE = '../Main_matter.tex'
OUTPUT_FILE = '../Main_Matter_processed.tex'
COMMANDS_FILE = '../Tex/Terms/Term_commands.tex'

# --- NEW: Number Mapping ---
DIGIT_MAP = {
    '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
    '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
}

# 1. WRAPPER COMMANDS
WRAPPER_COMMANDS = {
    'underline', 'hat', 'vec', 'bar', 'dot', 'ddot', 'tilde',
    'mathbf', 'mathcal', 'mathbb', 'mathrm', 'bm'
}

# 2. IGNORE COMMANDS
IGNORE_COMMANDS = {
    'begin', 'end', 'split', 'equation', 'align', 'pmatrix', 'bmatrix', 'vmatrix',
    'left', 'right', 'label', 'ref', 'cite', 'color', 'space', 'vspace', 'hspace',
    'frac', 'dfrac', 'tfrac', 'sum', 'prod', 'int', 'partial', 'sqrt',
    'cdot', 'times', 'div', 'pm', 'mp',
    'leq', 'geq', 'neq', 'approx', 'equiv', 'sim', 'll', 'gg', 'mhl',
    'rightarrow', 'leftarrow', 'Rightarrow', 'Leftarrow', 'to', 'in', 'subset',
    'cup', 'cap', 'setminus', 'infty', 'lim', 'quad', 'qquad',
    'sin', 'cos', 'tan', 'exp', 'ln', 'log', 'det', 'max', 'min', 'bigg', 'big', 'Big', 'sinb', 'cosb', 'boldsymbol'
}

# 3. TEXT/PROTECTED COMMANDS
TEXT_COMMANDS = {
    'text', 'mbox', 'label', 'ref', 'cite', 'url', 'href', 'color',
    'input', 'include', 'eqref', 'begin', 'end'
}

# ... [Keep mask_comments, get_balanced_text, get_math_regions, check_suffix, parse_variables, replace_math_content AS IS] ...
# (Paste the helper functions here if re-assembling the full file, otherwise just update process_tex below)

def mask_comments(text):
    lines = text.split('\n')
    masked_lines = []
    for line in lines:
        idx = -1
        is_escaped = False
        for i, char in enumerate(line):
            if char == '\\': is_escaped = not is_escaped
            elif char == '%':
                if not is_escaped:
                    idx = i
                    break
                is_escaped = False
            else: is_escaped = False
        if idx != -1:
            line = line[:idx] + ' ' * (len(line) - idx)
        masked_lines.append(line)
    return '\n'.join(masked_lines)

def get_balanced_text(text, start_index):
    if start_index >= len(text) or text[start_index] != '{':
        return "", start_index
    depth = 0
    for i in range(start_index, len(text)):
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0: return text[start_index:i+1], i + 1
    return "", start_index

def get_math_regions(text):
    regions = []
    eq_pattern = re.compile(r'(\\begin\{equation\}.*?\\end\{equation\})', re.DOTALL)
    for match in eq_pattern.finditer(text):
        regions.append({'start': match.start(), 'end': match.end()})

    temp_text = list(text)
    for r in regions:
        for i in range(r['start'], r['end']): temp_text[i] = ' '
    temp_text_str = "".join(temp_text)

    inline_pattern = re.compile(r'(?<!\\)\$(.*?)(?<!\\)\$', re.DOTALL)
    for match in inline_pattern.finditer(temp_text_str):
        regions.append({'start': match.start(), 'end': match.end()})

    return sorted(regions, key=lambda x: x['start'])

def check_suffix(text, base, start_index):
    current_term = base
    i = start_index
    n = len(text)
    while i < n:
        if text[i].isspace():
            i += 1
            continue
        if text[i] == "'":
            current_term += "'"
            i += 1
            continue
        if text[i] == '_':
            i += 1
            suffix = "_"
            if i < n:
                if text[i] == '{':
                    block, end = get_balanced_text(text, i)
                    suffix += block
                    i = end
                elif text[i] == '\\':
                    j = i + 1
                    cmd = "\\"
                    while j < n and (text[j].isalpha() or text[j] == '@'):
                        cmd += text[j]; j += 1
                    if len(cmd) == 1 and j < n: cmd += text[j]; j += 1
                    suffix += cmd
                    i = j
                else:
                    suffix += text[i]; i += 1
            current_term += suffix
            continue
        if text[i] == '^':
             i += 1
             if i < n:
                if text[i] == '{': _, end = get_balanced_text(text, i); i = end
                elif text[i] == '\\':
                     j = i + 1
                     while j < n and (text[j].isalpha() or text[j] == '@'): j += 1
                     i = j
                else: i += 1
             continue
        break
    return current_term, i

def parse_variables(math_str):
    candidates = set()
    i = 0
    n = len(math_str)
    SKIP_CHARS = set("={}()[]+-*/!,.<>|;:?^& \t\n\r")

    while i < n:
        char = math_str[i]
        if char in SKIP_CHARS: i += 1; continue

        if char == '\\':
            j = i + 1
            cmd_name = ""
            while j < n and (math_str[j].isalpha() or math_str[j] == '@'):
                cmd_name += math_str[j]; j += 1
            full_cmd = math_str[i:j]

            if not cmd_name: i = j + 1 if j < n else j; continue

            if cmd_name.startswith('T'):
                i = j
                continue

            if cmd_name in WRAPPER_COMMANDS:
                k = j
                while k < n and math_str[k].isspace(): k += 1
                if k < n and math_str[k] == '{':
                    _, end_idx = get_balanced_text(math_str, k)
                    base = math_str[i:end_idx]
                    term, new_i = check_suffix(math_str, base, end_idx)
                    candidates.add(term); i = new_i; continue
                elif k < n:
                    base = math_str[i:k+1]
                    term, new_i = check_suffix(math_str, base, k+1)
                    candidates.add(term); i = new_i; continue

            if cmd_name in IGNORE_COMMANDS or cmd_name in TEXT_COMMANDS:
                if cmd_name in TEXT_COMMANDS:
                       k = j
                       while k < n and math_str[k].isspace(): k += 1
                       if k < n and math_str[k] == '{':
                         brace_content, end_idx = get_balanced_text(math_str, k)
                         inner_text = brace_content[1:-1]
                         inner_math_matches = re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$', inner_text, flags=re.DOTALL)
                         for m in inner_math_matches:
                             inner_vars = parse_variables(m)
                             for iv in inner_vars: candidates.add(iv)
                         i = end_idx; continue
                i = j; continue

            term, new_i = check_suffix(math_str, full_cmd, j)
            candidates.add(term); i = new_i; continue

        if char.isalpha():
            term, new_i = check_suffix(math_str, char, i+1)
            candidates.add(term); i = new_i; continue
        i += 1
    return list(candidates)

def replace_math_content(text, replacements):
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    result = []
    i = 0
    n = len(text)

    while i < n:
        matched_replacement = False
        for key in sorted_keys:
            if text.startswith(key, i):
                if key[-1].isalpha() and (i + len(key) < n) and text[i + len(key)].isalpha():
                      continue
                result.append(replacements[key] + " ")
                i += len(key)
                matched_replacement = True
                break

        if matched_replacement:
            continue

        if text[i] == '\\':
            j = i + 1
            cmd = ""
            while j < n and (text[j].isalpha() or text[j] == '@'):
                cmd += text[j]; j += 1
            full_cmd = text[i:j]

            if cmd in TEXT_COMMANDS:
                result.append(full_cmd)
                i = j
                while i < n and text[i].isspace():
                    result.append(text[i]); i += 1

                if i < n and text[i] == '{':
                    content, end_idx = get_balanced_text(text, i)
                    if '$' in content:
                        inner = content[1:-1]
                        parts = re.split(r'((?<!\\)\$(?:.*?)(?<!\\)\$)', inner, flags=re.DOTALL)
                        new_inner = ""
                        for part in parts:
                            if part.startswith('$') and part.endswith('$'):
                                math_inner = part[1:-1]
                                processed_math = replace_math_content(math_inner, replacements)
                                new_inner += f"${processed_math}$"
                            else:
                                new_inner += part
                        result.append(f"{{{new_inner}}}")
                    else:
                        result.append(content)
                    i = end_idx
                continue

            result.append(full_cmd)
            i = j; continue

        result.append(text[i]); i += 1

    return "".join(result)

# --- MODIFIED PROCESS FUNCTION ---
def process_tex():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found."); return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        original_text = f.read()

    masked_text = mask_comments(original_text)
    regions = get_math_regions(masked_text)

    print("--- Extracting Variables ---")
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
        for v in vars_found: all_candidates.add(v)

    sorted_candidates = sorted(list(all_candidates), key=len, reverse=True)
    replacements = {}
    definitions = []
    used_commands = set()

    print(f"Found {len(sorted_candidates)} potential variables.")

    for term in sorted_candidates:
        first_collision = False

        while True:
            print(f"Variable:  {term}")
            prompt_text = f"Replace with (Enter to auto-generate"
            if first_collision:
                prompt_text += ", or Enter again to SKIP"
            prompt_text += "): "

            user_input = input(prompt_text).strip()
            command_to_use = ""

            # Case 1: Auto-generate
            if not user_input:
                if first_collision:
                    print(f"  [Skipped] Variable '{term}' will not be replaced.")
                    break

                # --- UPDATED: Process letters, numbers, AND primes ---
                stripped_term = ""
                for char in term:
                    if char.isalpha():
                        stripped_term += char
                    elif char.isdigit():
                        stripped_term += DIGIT_MAP.get(char, "")
                    elif char == "'":
                        stripped_term += "Prime"
                # -----------------------------------------------------

                if not stripped_term:
                    print("  [Skipped] Term contains no valid characters for auto-generation.")
                    break

                command_to_use = f"\\TT{stripped_term}"
                print(f"  -> Generated: {command_to_use}")

            # Case 2: Manual Input
            else:
                command_to_use = user_input

            # Check for Collisions
            if command_to_use in used_commands:
                print(f"  [Error] Command '{command_to_use}' is ALREADY used.")
                if not user_input:
                    first_collision = True
                continue

            # Valid
            replacements[term] = command_to_use
            definitions.append(f"\\newcommand{{{command_to_use}}}{{{term}}}")
            used_commands.add(command_to_use)
            break

    print("Applying replacements...")
    final_text = ""
    last_idx = 0

    for reg in regions:
        final_text += original_text[last_idx:reg['start']]
        math_block_orig = original_text[reg['start']:reg['end']]

        block_lines = math_block_orig.split('\n')
        processed_lines = []
        for line in block_lines:
            idx = -1; is_escaped = False
            for i, c in enumerate(line):
                if c == '\\': is_escaped = not is_escaped
                elif c == '%':
                    if not is_escaped: idx = i; break
                    is_escaped = False
                else: is_escaped = False

            if idx != -1: code_part = line[:idx]; comment_part = line[idx:]
            else: code_part = line; comment_part = ""

            if code_part.strip():
                code_part = replace_math_content(code_part, replacements)

            processed_lines.append(code_part + comment_part)
        final_text += '\n'.join(processed_lines)
        last_idx = reg['end']

    final_text += original_text[last_idx:]

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f: f.write(final_text)
    with open(COMMANDS_FILE, 'w', encoding='utf-8') as f:
        f.write("% Auto-generated variable definitions\n")
        for line in definitions: f.write(line + "\n")

    print(f"Success! Processed file saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_tex()