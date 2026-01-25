*** code setup:

- github
- git
    - winget install --id Git.Git -e --source winget

- python 3.12.4
    - winget install --id Python.Python.3.12.4 -e --source winget --scope user

- miktex

- strawberry perl
    - winget install StrawberryPerl.StrawberryPerl

- pdf2svg
    - git clone https://github.com/jalios/pdf2svg-windows.git pdf2svg
    - add C:\pdf2svg\dist-64bits; to PATH

- svgo (makes svg files smaller)
    - git clone https://github.com/svg/svgo.git svgo
    or
    - winget install OpenJS.NodeJS.LTS
    - npm install -g svgo


- GPL ghostscript (to minify pdfs)

- Inkscape
    - winget install -e --id Inkscape.Inkscape
    - add to path C:\Program Files\Inkscape\bin