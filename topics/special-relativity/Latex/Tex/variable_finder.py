import re
import sys

# --- CONFIGURATION ---
INPUT_FILE = "Main_Matter.tex"
OUTPUT_FILE = "Main_Matter_Processed.tex"

# --- PART 1: DEFINITIONS ---

def get_greek_whitelist():
    return {
        r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon', r'\varepsilon',
        r'\zeta', r'\eta', r'\theta', r'\vartheta', r'\iota', r'\kappa',
        r'\lambda', r'\mu', r'\nu', r'\xi', r'\pi', r'\varpi', r'\rho',
        r'\varrho', r'\sigma', r'\varsigma', r'\tau', r'\upsilon', r'\phi',
        r'\varphi', r'\chi', r'\psi', r'\omega',
        r'\Gamma', r'\Delta', r'\Theta', r'\Lambda', r'\Xi', r'\Pi',
        r'\Sigma', r'\Upsilon', r'\Phi', r'\Psi', r'\Omega',
        r'\nabla', r'\partial', r'\ell'
    }

def get_math_segments(content):
    """
    Splits content into text and math segments.
    Updated to handle newlines in inline math (re.DOTALL for both).
    """
    # Pattern:
    # 1. Inline math: $...$
    # 2. Display math: \begin{equation}...\end{equation}
    # 3. Display shorthand: \[...\]
    pattern = re.compile(
        r'('
        r'(?<!\\)\$.*?(?<!\\)\$'          # $...$
        r'|'
        r'\\begin\{equation\}[\s\S]*?\\end\{equation\}' # Environment
        r'|'
        r'\\\[[\s\S]*?\\\]'               # \[...\]
        r')',
        re.DOTALL # Crucial: Allows . to match newlines (fixes multiline captions)
    )

    parts = pattern.split(content)
    segments = []

    for part in parts:
        if not part: continue

        # Identify if this chunk is math
        if part.startswith('$') or part.startswith(r'\begin{equation}') or part.startswith(r'\['):
            segments.append({'type': 'math', 'content': part})
        else:
            segments.append({'type': 'text', 'content': part})

    return segments

def extract_variables_from_math(math_content):
    found = set()

    # 1. CLEAN JUNK (Structural commands)
    # We remove these commands to expose the variables inside them.
    junk_commands = [
        r'\\begin\{.*?\}', r'\\end\{.*?\}',
        r'\\text\{.*?\}', r'\\label\{.*?\}', r'\\caption', # Remove caption command itself
        r'\\(frac|sqrt|sum|int|prod|lim)',
        r'\\(left|right|big|Big|bigg|Bigg)',
        r'\\(sin|cos|tan|exp|log|ln)',
        r'\\(mathbf|mathrm|mathcal|vec|hat|bar|tilde|dot|ddot|mathring|boldsymbol|hphantom)',
        r'\\(approx|equiv|geq|leq|ll|gg|neq|cdot|times|to|rightarrow|leftarrow|infty)',
        r'\\(color|gray)', r'&', r'\\\\', r'\^' # Remove ^ used for powers (but primes handled later)
    ]

    clean = math_content
    for junk in junk_commands:
        clean = re.sub(junk, ' ', clean)

    # Remove standard operators
    clean = re.sub(r'[=+\-><()\[\]/!|:;,\.]', ' ', clean)

    # 2. DEFINE PATTERNS
    greek_set = get_greek_whitelist()
    regex_underline = re.compile(r'\\underline\{[^{}]+\}') # Simple underline
    regex_latin = re.compile(r'\b[a-zA-Z]+\b')

    # Subscript Pattern: _i or _{ij}
    regex_subscript = re.compile(r'(_\{[a-zA-Z0-9,\+\-\\'']+\}|_[a-zA-Z0-9])')

    # Prime Pattern: ' or {'} or ''
    # Matches: ' or {'} or multiple ''
    regex_prime = re.compile(r"('|\{'\}|''+)")

    tokens = clean.split()

    # 3. ITERATE TOKENS
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Build a "Candidate" string by looking ahead for parts
        # Order of LaTeX often: Base + Subscript + Prime OR Base + Prime + Subscript
        # But cleaning might split them. We try to grab attached parts.

        base = token
        found_sub = ""
        found_prime = ""

        # -- Step A: Check for Prime attached to end of token --
        # e.g. "x'" -> base="x", prime="'"
        # e.g. "\underline{a}{'}" -> base="\underline{a}", prime="{'}"

        # Repeat stripping until clean (handle mixed orders roughly)
        matched_suffix = True
        while matched_suffix:
            matched_suffix = False

            # Check Prime
            p_match = regex_prime.search(base)
            if p_match:
                # Only if at the end
                if base.endswith(p_match.group(0)):
                    found_prime = p_match.group(0) + found_prime # Prepend if we found multiple (rare)
                    base = base[:-len(p_match.group(0))]
                    matched_suffix = True

            # Check Subscript
            s_match = regex_subscript.search(base)
            if s_match:
                if base.endswith(s_match.group(0)):
                    found_sub = s_match.group(0) + found_sub
                    base = base[:-len(s_match.group(0))]
                    matched_suffix = True

        # -- Step B: Check for separated parts (spaces between tokens) --
        # Look ahead at i+1, i+2
        has_more_parts = True
        offset = 1
        while has_more_parts:
            if i + offset >= len(tokens):
                break

            next_t = tokens[i+offset]

            # Is next token a Subscript? (_i)
            if regex_subscript.match(next_t):
                found_sub += next_t
                offset += 1
                continue

            # Is next token a Prime? (') or ({'})
            if regex_prime.match(next_t):
                found_prime += next_t
                offset += 1
                continue

            has_more_parts = False

        # Update main iterator loop
        i += offset

        # -- Step C: VALIDATE BASE --
        is_valid = False

        if regex_underline.fullmatch(base):
            is_valid = True
        elif base.startswith('\\') and base in greek_set:
            is_valid = True
        elif base.startswith('{') and base.endswith('}'):
            inner = base[1:-1]
            if (regex_latin.fullmatch(inner) or inner in greek_set) and inner not in ['pmatrix','split','aligned','gray']:
                is_valid = True
        elif regex_latin.fullmatch(base):
            is_valid = True

        if is_valid:
            # Reconstruct: Base + Sub + Prime
            # (Note: In your find/replace prompt, standardizing order helps,
            # but usually LaTeX is Base + Sub + Prime)
            full_var = base + found_sub + found_prime
            found.add(full_var)

    return found

def make_safe_regex(variable):
    """
    Creates a Regex pattern for the variable.
    Handles special characters like \ { } and ^
    """
    # Escape everything first (handles \, {, }, ^, etc.)
    esc_var = re.escape(variable)

    # Add boundaries
    # If it starts with a letter, ensure word boundary
    prefix = r'(?<!\\)\b' if variable[0].isalnum() else r''

    # If it ends with a letter, ensure word boundary
    # If it ends with ' or }, we generally don't need a boundary check
    suffix = r'\b' if variable[-1].isalnum() else r''

    return re.compile(prefix + esc_var + suffix)

# --- PART 2: MAIN EXECUTION ---

def main():
    print(f"Reading {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            full_content = f.read()
    except FileNotFoundError:
        print(f"File {INPUT_FILE} not found.")
        return

    # 1. Parse File into Text/Math Segments
    segments = get_math_segments(full_content)

    # 2. Identify Variables
    print("Scanning for variables (including primes ' and subscripts)...")
    all_vars = set()
    for seg in segments:
        if seg['type'] == 'math':
            vars_in_block = extract_variables_from_math(seg['content'])
            all_vars.update(vars_in_block)

    # 3. Sort Longest to Shortest
    sorted_vars = sorted(list(all_vars), key=len, reverse=True)

    print("-" * 50)
    print(f"Found {len(sorted_vars)} unique variables.")
    print("Starting interactive find & replace...")
    print("-" * 50)

    # 4. Interactive Loop
    for var in sorted_vars:
        print(f"\nVariable found:  \033[94m{var}\033[0m") # Blue text

        user_input = input(f"  Replace '{var}' with (Press Enter to skip): ")

        if user_input.strip():
            new_val = user_input.strip()
            pattern = make_safe_regex(var)

            count_in_var = 0
            for seg in segments:
                if seg['type'] == 'math':
                    new_content, n = pattern.subn(new_val, seg['content'])
                    if n > 0:
                        seg['content'] = new_content
                        count_in_var += n

            print(f"  -> Replaced {count_in_var} occurrences.")
        else:
            print("  -> Skipped.")

    # 5. Save
    print("-" * 50)
    final_output = "".join([s['content'] for s in segments])
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_output)
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()