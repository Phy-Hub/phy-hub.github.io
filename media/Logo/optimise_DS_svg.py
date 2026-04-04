import re

def optimize_svg_linecap(svg_string):
    """
    Replaces all <use> tags referencing a circle with a single,
    highly-compressed <path> using the round linecap trick.
    """
    # 1. Find all <use> tags
    use_tags = re.findall(r'<use\s+([^>]+)/>', svg_string)

    path_commands = []

    # 2. Extract coordinates and build the path string
    for attrs in use_tags:
        # We only care about the #a references (your circle)
        if 'href="#a"' in attrs:
            x_match = re.search(r'x="([^"]+)"', attrs)
            y_match = re.search(r'y="([^"]+)"', attrs)

            # Default to "0" if an axis is omitted in the original tag
            x = x_match.group(1) if x_match else "0"
            y = y_match.group(1) if y_match else "0"

            # M = move to (x, y), h0 = draw horizontal line of 0 length
            path_commands.append(f"M{x} {y}h0")

    # Join the commands without spaces to compress the string as much as possible
    d_string = "".join(path_commands)

    # 3. Create the optimized path element
    # r=".007" so the stroke-width must be .014
    # We explicitly add stroke="black" since default fill won't apply to strokes
    optimized_path = f'<path d="{d_string}" stroke="black" stroke-width=".014" stroke-linecap="round"/>'

    # 4. Strip out the old DOM clutter
    # Remove all <use> tags
    svg_cleaned = re.sub(r'<use\s+[^>]+/>', '', svg_string)
    # Remove the <defs> containing the original circle
    svg_cleaned = re.sub(r'<defs>\s*<circle id="a"[^>]*/>\s*</defs>', '', svg_cleaned)

    # 5. Inject the new path right before the closing </svg> tag
    final_svg = svg_cleaned.replace('</svg>', f'{optimized_path}</svg>')

    return final_svg


with open("DS_Pattern_optimised.svg", "r") as f:
    raw_svg = f.read()

compressed_svg = optimize_svg_linecap(raw_svg)

with open("output.svg", "w") as f:
    f.write(compressed_svg)