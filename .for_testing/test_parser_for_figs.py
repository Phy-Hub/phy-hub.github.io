import re

def create_dictionary_of_figures(filename):

    with open(filename, 'r') as f:
        content = f.read()

    figure_data = {}
    chapter_number = 0
    figure_number = 0
    label_count = 0

    chapters = re.split(r'\\chapter{', content)[1:]

    for chapter_content in chapters:
        chapter_number += 1
        figure_number = 0

        figure_matches = re.findall(r'\\begin{figure}(.*?)\\end{figure}', chapter_content, re.DOTALL)

        for figure_match in figure_matches:
            figure_number += 1

            label_count += len(re.findall(r'\\label{', figure_match))

            # Find main figure title and label (might be before or after subfigures)
            figure_title = ""
            figure_label = ""
            caption_match = re.search(r'\\caption\s*(\{.*?\})\s*(?:\\label\s*\{([^}]+)\})?', figure_match, re.DOTALL)
            #if caption_match:
            #    print( "*** ", {caption_match.group(1)})
            if caption_match:
                # Less greedy title extraction
                title_match = re.search(r'\\textbf{([^}]*?)}', caption_match.group(1))
                if title_match:
                    figure_title = title_match.group(1).strip()

            # Find label OUTSIDE of any subfigure environment
            # (this was the crucial fix)
            temp_figure_match = figure_match
            for subfigure_match in re.findall(r'\\begin{subfigure}(.*?)\\end{subfigure}', figure_match, re.DOTALL):
                temp_figure_match = temp_figure_match.replace(subfigure_match, "")

            label_match = re.search(r'\\label{([^}]*?)}', temp_figure_match)
            if label_match:
                figure_label = label_match.group(1).strip()

            figure_id = f"fig: {chapter_number}.{figure_number}"
            figure_data[figure_id] = (figure_title, figure_label)

            subfigure_matches = re.findall(r'\\begin{subfigure}(.*?)\\end{subfigure}', figure_match, re.DOTALL)

            for i, subfigure_match in enumerate(subfigure_matches):
                subfigure_letter = chr(ord('a') + i)

                # Find subfigure title
                subfigure_title = ""
                subfigure_label = ""

                subfigure_caption_match = re.search(r'\\caption{(.*?)}', subfigure_match, re.DOTALL)
                if subfigure_caption_match:
                    subfigure_title_match = re.search(r'\\textbf{([^}]*?)}', subfigure_caption_match.group(1))
                    if subfigure_title_match:
                        subfigure_title = subfigure_title_match.group(1).strip()

                    # Find label within the caption
                    label_match = re.search(r'\\label{([^}]*?)}', subfigure_caption_match.group(1))
                    if label_match:
                      subfigure_label = label_match.group(1).strip()
                    else:
                      # look for label outside of caption
                      label_match = re.search(r'\\label{([^}]*?)}', subfigure_match)
                      if label_match:
                        subfigure_label = label_match.group(1).strip()


                subfigure_id = f"fig: {chapter_number}.{figure_number}.{subfigure_letter}"
                figure_data[subfigure_id] = (subfigure_title, subfigure_label)

    #for figure_id, (title, label) in figure_data.items():
    #   print(f"ID: {figure_id}, Title: {title}, Label: {label}")

    non_empty_label_count = sum(1 for _, (_, label) in figure_data.items() if label)

    print(f"\nNumber of \\label occurrences within figure environments: {label_count}")
    print(f"Number of non-empty label entries in the dictionary: {non_empty_label_count}")
    print(f"Number of dictionary entries: {len(figure_data)}")

    if label_count != non_empty_label_count:
        print("Warning: The number of \\label occurrences and non-empty label entries do not match.")

    return figure_data

dictionary = create_dictionary_of_figures("Main_Matter.tex")

def duplicate_figurelabels_check(dictionary):

  labels = {}
  duplicates_found = False

  for figure_id, (figure_title, figure_label) in dictionary.items():
    # Ignore empty labels
    if figure_label:  # Check if figure_label is not empty
      if figure_label in labels:
        labels[figure_label].append(figure_id)
        duplicates_found = True
      else:
        labels[figure_label] = [figure_id]

  if duplicates_found:
    print("Duplicate labels found:")
    for label, figure_ids in labels.items():
      if len(figure_ids) > 1:
        print(f"  Label '{label}' is duplicated in figures: {', '.join(figure_ids)}")
  else:
    print("No duplicate labels found (excluding empty labels).")


duplicate_figurelabels_check(dictionary)