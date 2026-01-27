import re
import os

# --- CONFIGURATION ---
DEF_FILE = "../Tex/Terms/Definitions.tex"
MAIN_FILE = "../Main_matter.tex"

# 1. COMMANDS TO IGNORE (Content skipped completely)
# Note: These expect arguments in braces {}. \iffalse is handled separately.
IGNORE_CMDS = {
    'section', 'subsection', 'subsubsection', 'chapter', 'paragraph',
    'label', 'ref', 'cite', 'eqref', 'usepackage', 'input', 'include',
    'includegraphics', 'url', 'href', 'nocite', 'bibliographystyle'
}

# 2. CONTAINER ENVIRONMENTS (Text inside is IGNORED, but we look for \caption)
CONTAINER_ENVS = {
    'figure', 'figure*', 'table', 'table*', 'wrapfigure'
}

# 3. IGNORED ENVIRONMENTS (Content skipped completely)
IGNORE_ENVS = {
    'equation', 'equation*', 'align', 'align*', 'gather', 'gather*',
    'tikzpicture', 'verbatim', 'lstlisting', 'tabular', 'tabularx'
}

# 4. CAPTION COMMANDS (Enter CAPTION MODE -> Enable Replace + \protect)
CAPTION_CMDS = {
    'caption', 'captions', 'captionof'
}

class LatexEngine:
    @staticmethod
    def skip_comments_and_whitespace(text, index):
        while index < len(text):
            char = text[index]
            if char.isspace():
                index += 1
            elif char == '%':
                eol = text.find('\n', index)
                if eol == -1: return len(text)
                index = eol + 1
            else:
                break
        return index

    @staticmethod
    def find_balanced_brace(text, start_index):
        if start_index >= len(text) or text[start_index] != '{':
            return None, -1

        balance = 0
        i = start_index
        escaped = False
        in_comment = False

        while i < len(text):
            char = text[i]
            if in_comment:
                if char == '\n': in_comment = False
                i += 1
                continue
            if escaped:
                escaped = False
                i += 1
                continue
            if char == '\\': escaped = True
            elif char == '%': in_comment = True
            elif char == '{': balance += 1
            elif char == '}':
                balance -= 1
                if balance == 0:
                    return text[start_index+1 : i], i + 1
            i += 1
        return None, -1

class TermProcessor:
    def __init__(self, def_file):
        self.definitions = self.load_definitions(def_file)
        self.replacements_map = {}
        self.replace_counter = 0

    def load_definitions(self, path):
        if not os.path.exists(path):
            print(f"❌ Error: Definition file not found: {path}")
            return []

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        defs = []
        cursor = 0
        while True:
            match = re.search(r'\\term\s*\{', content[cursor:])
            if not match: break

            term_start = cursor + match.start()
            curr = cursor + match.end() - 1
            args = []
            valid = True

            for _ in range(4):
                curr = LatexEngine.skip_comments_and_whitespace(content, curr)
                val, next_idx = LatexEngine.find_balanced_brace(content, curr)
                if val is None:
                    valid = False
                    break
                args.append(val)
                curr = next_idx

            if valid and len(args) == 4:
                term_id = args[0]
                phrases_raw = args[2]
                for p in phrases_raw.split(','):
                    clean = p.strip()
                    if clean:
                        defs.append((term_id, clean))
                cursor = curr
            else:
                cursor = term_start + 1

        print(f"✅ Loaded {len(defs)} definition phrases.")
        # Sort Longest First
        defs.sort(key=lambda x: len(x[1]), reverse=True)

        compiled_defs = []
        for term_id, phrase in defs:
            # 1. Handle Spaces: Allow "Prime frame" to match "Prime\nframe"
            safe_phrase = re.escape(phrase).replace(r'\ ', r'\s+')

            # 2. Handle Suffixes: Allow s, 's, or '
            # Pattern: \b(Phrase)(s|'s|')?\b
            pattern_str = r'\b(' + safe_phrase + r")(s|'s|')?\b"

            pattern = re.compile(pattern_str, re.IGNORECASE)
            compiled_defs.append((term_id, pattern))

        return compiled_defs

    def process_safe_text(self, text, mode):
        """
        mode='NORMAL': Replace with \hyperlink
        mode='CAPTION': Replace with \protect\hyperlink
        mode='CONTAINER': Do NOT replace anything
        """
        if mode == 'CONTAINER':
            return text

        if mode == 'CAPTION':
            tmpl_start = "\\protect\\hyperlink{"
        else:
            tmpl_start = "\\hyperlink{"

        for term_id, pattern in self.definitions:
            if pattern.search(text):
                def sub_fn(m):
                    token = f"__LINK_PLACEHOLDER_{self.replace_counter}__"

                    base_word = m.group(1)
                    suffix = m.group(2) if m.group(2) else ""

                    # LOGIC:
                    # If suffix contains "'" (possessive), put it OUTSIDE the link.
                    # If suffix is just "s" (plural), put it INSIDE the link.

                    if "'" in suffix:
                        # Case: frame's -> \hyperlink{...}{frame}'s
                        replacement_latex = f"{tmpl_start}{term_id}}}{{{base_word}}}{suffix}"
                    else:
                        # Case: frames -> \hyperlink{...}{frames}
                        replacement_latex = f"{tmpl_start}{term_id}}}{{{base_word}{suffix}}}"

                    self.replacements_map[token] = replacement_latex
                    self.replace_counter += 1
                    return token

                text = pattern.sub(sub_fn, text)
        return text

    def scan_text(self, text, mode='NORMAL'):
        """
        Recursive Linear Scanner with Modes.
        Modes: 'NORMAL', 'CONTAINER' (No replace), 'CAPTION' (Protect replace)
        """
        output_parts = []
        cursor = 0
        total_len = len(text)

        while cursor < total_len:
            # 1. Find next special character (\ or %)
            next_bs = text.find('\\', cursor)
            next_pc = text.find('%', cursor)
            if next_bs == -1: next_bs = total_len
            if next_pc == -1: next_pc = total_len
            next_special = min(next_bs, next_pc)

            # 2. Process Safe Text block
            if next_special > cursor:
                safe_chunk = text[cursor:next_special]
                processed_chunk = self.process_safe_text(safe_chunk, mode)
                output_parts.append(processed_chunk)
                cursor = next_special

            if cursor >= total_len: break
            char = text[cursor]

            # --- CASE A: Comment ---
            if char == '%':
                eol = text.find('\n', cursor)
                end_pos = eol + 1 if eol != -1 else total_len
                output_parts.append(text[cursor:end_pos])
                cursor = end_pos
                continue

            # --- CASE B: Command ---
            match_cmd = re.match(r'\\([a-zA-Z@\*]+)', text[cursor:])
            if match_cmd:
                cmd_name = match_cmd.group(1)
                cmd_end = cursor + match_cmd.end()

                # -----------------------------------------------------------
                # 1. HANDLE \iffalse ... \fi BLOCKS
                # -----------------------------------------------------------
                if cmd_name == "iffalse":
                    # We need to skip everything until matching \fi
                    # We must respect nesting of other \if... \fi blocks
                    nesting = 1
                    search_cursor = cmd_end

                    # Regex to find next \if... or \fi
                    # Matches \ifsomething or \fi
                    # We treat any \if... as increasing nesting
                    cond_pattern = re.compile(r'\\(if[a-zA-Z@]*|fi)\b')

                    while nesting > 0 and search_cursor < total_len:
                        cond_match = cond_pattern.search(text, search_cursor)
                        if not cond_match:
                            # Error: No matching \fi found, skip rest of file or break
                            search_cursor = total_len
                            break

                        found_tag = cond_match.group(1)
                        if found_tag == 'fi':
                            nesting -= 1
                        else:
                            # It is an \if... (iffalse, iftrue, ifdefined, etc)
                            nesting += 1

                        search_cursor = cond_match.end()

                    # output raw text without processing
                    output_parts.append(text[cursor:search_cursor])
                    cursor = search_cursor
                    continue
                # -----------------------------------------------------------

                # 2. CHECK ENVIRONMENTS (\begin{...})
                if cmd_name == "begin":
                    arg_match = re.match(r'\s*\{([^}]+)\}', text[cmd_end:])
                    if arg_match:
                        env_name = arg_match.group(1)
                        end_pat = r'\\end\{' + re.escape(env_name) + r'\}'
                        end_match = re.search(end_pat, text[cursor:])

                        if end_match:
                            block_end = cursor + end_match.end()

                            # Decide how to recurse
                            if env_name in IGNORE_ENVS:
                                output_parts.append(text[cursor:block_end])
                            elif env_name in CONTAINER_ENVS:
                                # Recurse on INNER content in CONTAINER mode
                                inner_start = text.find('}', cmd_end) + 1
                                inner_end = cursor + end_match.start()

                                prefix = text[cursor:inner_start]
                                inner_text = text[inner_start:inner_end]
                                suffix = text[inner_end:block_end]

                                processed_inner = self.scan_text(inner_text, mode='CONTAINER')
                                output_parts.append(prefix + processed_inner + suffix)
                            else:
                                # Recurse on INNER content in current mode
                                inner_start = text.find('}', cmd_end) + 1
                                inner_end = cursor + end_match.start()

                                prefix = text[cursor:inner_start]
                                inner_text = text[inner_start:inner_end]
                                suffix = text[inner_end:block_end]

                                processed_inner = self.scan_text(inner_text, mode=mode)
                                output_parts.append(prefix + processed_inner + suffix)

                            cursor = block_end
                            continue

                # 3. CAPTION COMMANDS (Force CAPTION mode)
                if cmd_name in CAPTION_CMDS:
                    # Skip optional arg [..]
                    curr_chk = cmd_end
                    while curr_chk < len(text) and text[curr_chk].isspace(): curr_chk += 1
                    if curr_chk < len(text) and text[curr_chk] == '[':
                        end_bracket = text.find(']', curr_chk)
                        if end_bracket != -1: curr_chk = end_bracket + 1

                    brace_pos = text.find('{', curr_chk)
                    if brace_pos != -1 and text[curr_chk:brace_pos].strip() == "":
                        inner_content, close_pos = LatexEngine.find_balanced_brace(text, brace_pos)
                        if inner_content is not None:
                            # RECURSE with CAPTION mode
                            processed_inner = self.scan_text(inner_content, mode='CAPTION')

                            output_parts.append(text[cursor:brace_pos + 1])
                            output_parts.append(processed_inner)
                            output_parts.append('}')
                            cursor = close_pos
                            continue

                # 4. IGNORE COMMANDS (Skip content completely)
                if cmd_name in IGNORE_CMDS:
                    brace_pos = text.find('{', cmd_end)
                    if brace_pos != -1 and text[cmd_end:brace_pos].strip() == "":
                        _, close_pos = LatexEngine.find_balanced_brace(text, brace_pos)
                        if close_pos != -1:
                            output_parts.append(text[cursor:close_pos])
                            cursor = close_pos
                            continue

                # 5. EXISTING HYPERLINKS
                if cmd_name == "hyperlink":
                    b1 = text.find('{', cmd_end)
                    if b1 != -1:
                        _, e1 = LatexEngine.find_balanced_brace(text, b1)
                        if e1 != -1:
                            b2 = text.find('{', e1)
                            if b2 != -1 and text[e1:b2].strip() == "":
                                _, e2 = LatexEngine.find_balanced_brace(text, b2)
                                if e2 != -1:
                                    output_parts.append(text[cursor:e2])
                                    cursor = e2
                                    continue

            output_parts.append(text[cursor])
            cursor += 1

        return "".join(output_parts)

    def run(self, main_file):
        if not self.definitions: return

        if not os.path.exists(main_file):
            print(f"❌ Error: Main file not found: {main_file}")
            return

        print(f"Reading {main_file}...")
        with open(main_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        print("Scanning and replacing...")
        processed_text = self.scan_text(raw_text, mode='NORMAL')

        print(f"Finalizing {len(self.replacements_map)} links...")
        for token, latex in self.replacements_map.items():
            processed_text = processed_text.replace(token, latex)

        print(f"Writing output to {main_file}...")
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        print("Done!")

if __name__ == "__main__":
    processor = TermProcessor(DEF_FILE)
    processor.run(MAIN_FILE)