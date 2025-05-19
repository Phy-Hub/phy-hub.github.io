import os
import subprocess

svg_files = [f for f in os.listdir("svg") if f.endswith('.svg')]

# Loop over the svg files and convert each one to pdf
for svg_file in svg_files:
    pdf_file = os.path.join("pdf", os.path.splitext(svg_file)[0] + '.pdf')
    svg_file_path = os.path.join("svg", svg_file)

    # Check if the pdf file exists and is older than the svg file
    if not os.path.exists(pdf_file) or os.path.getmtime(svg_file_path) > os.path.getmtime(pdf_file):

        subprocess.run(['inkscape', '--export-filename=' + pdf_file, svg_file_path])

        print("pdf updated: ", pdf_file )
