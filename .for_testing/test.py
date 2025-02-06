import re

def extract_latex_structure(filepath):
    structure_dict = {}
    counters = {
        "chapter": 0,
        "section": 0,
        "subsection": 0,
        "subsubsection": 0
    }

    with open(filepath, 'r') as f:
        for line in f:
            # Chapter matching
            match_chapter = re.match(r"\\chapter(?:\[[^\]]*\])?\{([^}]+)\}(?:\\label\{([^}]+)\})?", line)
            if match_chapter:
                counters["chapter"] += 1
                counters["section"] = 0
                counters["subsection"] = 0
                counters["subsubsection"] = 0
                title = match_chapter.group(1).strip()
                label = match_chapter.group(2).strip() if match_chapter.group(2) else None
                structure_dict[f"{counters['chapter']}"] = {"title": title, "label": label}
                continue

            # Section matching
            match_section = re.match(r"\\section(?:\[[^\]]*\])?\{([^}]+)\}(?:\\label\{([^}]+)\})?", line)
            if match_section:
                counters["section"] += 1
                counters["subsection"] = 0
                counters["subsubsection"] = 0
                title = match_section.group(1).strip()
                label = match_section.group(2).strip() if match_section.group(2) else None
                structure_dict[f"{counters['chapter']}.{counters['section']}"] = {"title": title, "label": label}
                continue

            # Subsection matching
            match_subsection = re.match(r"\\subsection(?:\[[^\]]*\])?\{([^}]+)\}(?:\\label\{([^}]+)\})?", line)
            if match_subsection:
                counters["subsection"] += 1
                counters["subsubsection"] = 0
                title = match_subsection.group(1).strip()
                label = match_subsection.group(2).strip() if match_subsection.group(2) else None
                structure_dict[f"{counters['chapter']}.{counters['section']}.{counters['subsection']}"] = {"title": title, "label": label}
                continue

            # Subsubsection matching
            match_subsubsection = re.match(r"\\subsubsection(?:\[[^\]]*\])?\{([^}]+)\}(?:\\label\{([^}]+)\})?", line)
            if match_subsubsection:
                counters["subsubsection"] += 1
                title = match_subsubsection.group(1).strip()
                label = match_subsubsection.group(2).strip() if match_subsubsection.group(2) else None
                structure_dict[f"{counters['chapter']}.{counters['section']}.{counters['subsection']}.{counters['subsubsection']}"] = {"title": title, "label": label}
                continue

    # Print the dictionary
    #for key, value in structure_dict.items():
    #    print(f"Number: {key}, Title: {value['title']}, Label: {value['label']}")

    return structure_dict

# Example usage:
filepath = "Main_Matter.tex"  # Replace with your LaTeX file path
latex_structure = extract_latex_structure(filepath)
