import re
import os

# --- Configuration ---
INPUT_FILE = '../Main_matter.tex'
OUTPUT_FILE = '../Main_Matter_processed.tex'
COMMANDS_FILE = '../Tex/Terms/Term_commands.tex'
DICT_FILE = '../Tex/Terms/Term_dict.tex'

# --- Number Mapping ---
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

# --- HELPER FUNCTIONS ---
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
    candidates = []
    i = 0
    n = len(math_str)
    SKIP_CHARS = set("={}()[]+-*/!,.<>|;:?^& \t\n\r")

    def add_candidate(val):
        if val not in candidates:
            candidates.append(val)

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
                    add_candidate(term); i = new_i; continue
                elif k < n:
                    base = math_str[i:k+1]
                    term, new_i = check_suffix(math_str, base, k+1)
                    add_candidate(term); i = new_i; continue

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
                              for iv in inner_vars: add_candidate(iv)
                          i = end_idx; continue
                i = j; continue

            term, new_i = check_suffix(math_str, full_cmd, j)
            add_candidate(term); i = new_i; continue

        if char.isalpha():
            term, new_i = check_suffix(math_str, char, i+1)
            add_candidate(term); i = new_i; continue
        i += 1
    return candidates

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

# --- PROCESS FUNCTION ---
def process_tex():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found."); return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        original_text = f.read()

    masked_text = mask_comments(original_text)
    regions = get_math_regions(masked_text)

    print("--- Extracting Variables ---")

    candidates_ordered = []
    seen_candidates = set()

    for reg in regions:
        content_masked = masked_text[reg['start']:reg['end']]
        if content_masked.strip().startswith('$'):
            search_content = content_masked.strip()[1:-1]
        else:
            search_content = content_masked

        vars_found = parse_variables(search_content)

        for v in vars_found:
            if v not in seen_candidates:
                seen_candidates.add(v)
                candidates_ordered.append(v)

    sorted_candidates = candidates_ordered

    replacements = {}
    definitions = []
    dict_entries = []

    # --- UPDATED LOAD LOGIC ---
    existing_definitions = {}

    if os.path.exists(COMMANDS_FILE):
        print(f"Reading existing commands from {COMMANDS_FILE}...")
        try:
            with open(COMMANDS_FILE, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                existing_matches = re.findall(r'\\variableterm\{(.*?)\}\{(.*?)\}', existing_content)
                for cmd, val in existing_matches:
                    existing_definitions[cmd] = val

                print(f" -> Found {len(existing_definitions)} defined commands.")
        except Exception as e:
            print(f"Warning: Could not read existing commands: {e}")

    print(f"Found {len(sorted_candidates)} potential variables.")

    # Flag to break out of the main loop completely
    stop_prompting = False

    for term in sorted_candidates:
        if stop_prompting:
            break

        first_collision = False
        is_reusing_command = False

        while True:
            # Reusing command from existing definitions check logic done below...

            print(f"Variable:  {term}")
            prompt_text = f"Replace with (Enter to auto-generate"
            if first_collision:
                prompt_text += ", or Enter again to skip this term"
            # --- UPDATED PROMPT TEXT ---
            prompt_text += ", 'skip one' to skip this, 'skip' to finish all): "

            user_input = input(prompt_text).strip()

            # --- SKIP ONE FUNCTIONALITY (NEW) ---
            if user_input.lower() == 'skip one':
                print(f"  [Skipped] Skipping individual term '{term}'.")
                break # Breaks 'while True', moving to next term in 'for' loop
            # ------------------------------------

            # --- SKIP ALL FUNCTIONALITY ---
            if user_input.lower() == 'skip':
                print("\n>>> Skipping remaining terms. Processing collected replacements...\n")
                stop_prompting = True
                break
            # ------------------------------

            command_to_use = ""

            # Case 1: Auto-generate
            if not user_input:
                if first_collision:
                    print(f"  [Skipped] Variable '{term}' will not be replaced.")
                    break

                stripped_term = ""
                for char in term:
                    if char.isalpha():
                        stripped_term += char
                    elif char.isdigit():
                        stripped_term += DIGIT_MAP.get(char, "")
                    elif char == "'":
                        stripped_term += "Prime"

                if not stripped_term:
                    print("  [Skipped] Term contains no valid characters for auto-generation.")
                    break

                command_to_use = f"\\T{stripped_term}"
                print(f"  -> Generated: {command_to_use}")

            # Case 2: Manual Input (UPDATED)
            else:
                # If user explicitly starts with \, allow it (e.g. \alpha)
                # Otherwise, prepend \T automatically
                if user_input.startswith('\\'):
                    command_to_use = user_input
                else:
                    command_to_use = f"\\T{user_input}"

            # --- COLLISION CHECK ---
            if command_to_use in existing_definitions:
                prev_definition = existing_definitions[command_to_use]

                if prev_definition == term:
                    print(f"  [Info] Re-using existing command '{command_to_use}' (matches '{term}').")
                    replacements[term] = command_to_use
                    is_reusing_command = True
                    break
                else:
                    print(f"  [Error] Command '{command_to_use}' is ALREADY defined for '{prev_definition}'.")
                    if not user_input:
                        first_collision = True
                    continue

            # Valid new command
            replacements[term] = command_to_use

            definitions.append(f"\\variableterm{{{command_to_use}}}{{{term}}}{{***DEF NEEDED***}}")
            dict_entries.append(f"$\\left( {command_to_use} \\right)$ \\textbf{{:}} {command_to_use}def \n")

            existing_definitions[command_to_use] = term
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

    if definitions:
        os.makedirs(os.path.dirname(COMMANDS_FILE), exist_ok=True)
        with open(COMMANDS_FILE, 'a', encoding='utf-8') as f:
            f.write("\n% --- New Append Batch ---\n")
            for line in definitions: f.write(line + "\n")
        print(f"Success! Appended {len(definitions)} commands to: {COMMANDS_FILE}")

    if dict_entries:
        os.makedirs(os.path.dirname(DICT_FILE), exist_ok=True)
        with open(DICT_FILE, 'a', encoding='utf-8') as f:
            f.write("\n% --- New Append Batch ---\n")
            for line in dict_entries: f.write(line + "\n")
        print(f"Success! Appended {len(dict_entries)} entries to: {DICT_FILE}")
    else:
        print("No new definitions to append.")

    print(f"Processed file saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_tex()