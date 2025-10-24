import subprocess
from pathlib import Path

svg_files = list(Path("svg").glob("*.svg"))

for i, svg_path in enumerate(svg_files, 1):

    # svg check and optimize
    if 'data-optimized="true"' not in svg_path.read_text(encoding='utf-8'):
        subprocess.run(['svgo', str(svg_path), '-o', str(svg_path)], shell=True)
        svg_path.write_text(svg_path.read_text(encoding='utf-8').replace('<svg', '<svg data-optimized="true"', 1), encoding='utf-8')
        print("svg", i, "of", len(svg_files), "optimized")

    # SVG to PDF
    pdf_path = Path("pdf") / svg_path.with_suffix('.pdf').name
    if not pdf_path.exists() or svg_path.stat().st_mtime > pdf_path.stat().st_mtime:
        subprocess.run(['inkscape', f'--export-filename={pdf_path}', str(svg_path)], check=True)
        print("pdf", i, "of", len(svg_files), "updated")


# import os
# import subprocess

# svg_files = [f for f in os.listdir("svg") if f.endswith('.svg')]
# i=1

# for svg_file in svg_files:
#     svg_file_path = os.path.join("svg", svg_file)
#     pdf_file = os.path.join("pdf", os.path.splitext(svg_file)[0] + '.pdf')

#     # svg check if optimized
#     optimized = False
#     with open(svg_file_path, 'r', encoding='utf-8') as f:
#         content = f.read()
#         if 'data-optimized="true"' in content:
#             optimized = True

#     # svg optimize
#     if not optimized:
#         subprocess.run(['svgo', svg_file_path, '-o', svg_file_path], shell=True)
#         with open(svg_file_path, 'r', encoding='utf-8') as file:
#             content = file.read()
#         with open(svg_file_path, 'w', encoding='utf-8') as file:
#             file.write(content.replace('<svg', '<svg data-optimized="true"', 1))
#     print(i, "out of", len(svg_files))
#     i = i + 1

#     # SVG to PDF
#     if not os.path.exists(pdf_file) or os.path.getmtime(svg_file_path) > os.path.getmtime(pdf_file):
#         subprocess.run(['inkscape', '--export-filename=' + pdf_file, svg_file_path])
#         print("pdf updated: ", pdf_file )