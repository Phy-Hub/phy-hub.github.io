from bs4 import BeautifulSoup

# Load SVG file
with open('Interference_Pattern.svg', 'r') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'xml')

# Iterate over all <use> elements
for use in soup.find_all('use'):
    x = float(use['x'])
    y = float(use['y'])

    # Check if the point meets the criteria
    if (abs(y - 0.5) < 0.007 or abs(y - 0) < 0.007) or y/0.3 -0.4 > 1/abs(x) or y/0.3 -1.22 < -1/abs(x) and (x > 0.66 or x < -0.66):
        # Remove the point
        use.decompose()

# Write the modified SVG back to the file
with open('Interference_Pattern1.svg', 'w') as f:
    f.write(str(soup.prettify()))
