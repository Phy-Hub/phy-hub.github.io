import os
import subprocess

svg_files = [f for f in os.listdir("svg") if f.endswith('.svg')]
i=1

for svg_file in svg_files:
    svg_file_path = os.path.join("svg", svg_file)

    subprocess.run(['svgo', svg_file_path, '-o', svg_file_path], shell=True)

    print(i, "out of", len(svg_files))
    i = i + 1