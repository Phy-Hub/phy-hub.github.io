import re

def compress_coordinates_to_single_line(svg_string):
    """
    Extracts coordinates and formats them into an ultra-compressed,
    single-line comma-separated string with no newlines or spaces.
    """
    use_tags = re.findall(r'<use\s+([^>]+)/>', svg_string)

    flat_coordinates = []

    for attrs in use_tags:
        if 'href="#a"' in attrs:
            x_match = re.search(r'x="([^"]+)"', attrs)
            y_match = re.search(r'y="([^"]+)"', attrs)

            # Extract as floats, defaulting to 0.0
            x = float(x_match.group(1)) if x_match else 0.0
            y = float(y_match.group(1)) if y_match else 0.0

            # The :g format specifier drops unnecessary .0 decimals to save bytes
            flat_coordinates.append(f"{x:g}")
            flat_coordinates.append(f"{y:g}")

    # Join the entire list with commas, resulting in zero newlines or spaces
    return ",".join(flat_coordinates)

# Example usage:
with open("DS_Pattern_optimised_old.svg", "r") as f:
    raw_svg = f.read()

# Get the ultra-compressed single line of data
compressed_data_string = compress_coordinates_to_single_line(raw_svg)

# Save directly to a text/CSV file using standard file writing
with open("DS_Pattern.csv", "w") as f:
    f.write(compressed_data_string)
