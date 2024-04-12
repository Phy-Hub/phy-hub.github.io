import subprocess

topic_folder_name = "special-relativity"
pdf_name = "Handbook_of_Special_Relativity.pdf"
Topic_Name = "Special Relativity"

subprocess.run(["python", "../Scripts/ASM_Page.py", topic_folder_name, pdf_name, Topic_Name ])
