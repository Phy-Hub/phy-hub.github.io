from datetime import datetime
def calculate_checked_ratio(filename):
 """Calculates the percentage of checked boxes in a Markdown file.

 Args:
   filename: The name of the Markdown file to analyze.

 Returns:
   The percentage of checked boxes as a float, or None if no boxes are found.
 """

 checked_boxes = 0
 total_boxes = 0

 with open(filename, 'r') as file:
   for line in file:
     line = line.strip()

     # Search for checkboxes with both "[ ]" and "[x]" patterns
     if line.startswith('- [x]'):  # Checked box
       checked_boxes += 1
     elif line.startswith('- [ ]'):  # Unchecked box
       total_boxes += 1

 if total_boxes == 0:
   return None  # No boxes found
 else:
   percentage = checked_boxes / total_boxes * 100
   return percentage

if __name__ == '__main__':
 filename = 'TODO.md'
 percentage = calculate_checked_ratio(filename)

 if percentage:
   print(f"Percentage of checked boxes: {percentage:.2f}%")

   now = datetime.now()
   date_string = now.strftime("%H:%M %d/%m/%y")

   # Write the same information to the end of the file as a comment
   with open(__file__, 'a') as f:
     f.write(f"\n# Percentage of checked boxes: {percentage:.2f}% at {date_string}")

# Percentage of checked boxes: 11.90% at 13:21 12/03/24