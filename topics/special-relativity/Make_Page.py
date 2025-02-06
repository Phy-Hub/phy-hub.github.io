import subprocess

Topic_Name = "Special Relativity"

topic_folder_name = Topic_Name.replace(" ", "-").lower()
pdf_name = "Handbook_of_" + Topic_Name.replace(" ", "_") + ".pdf"
subprocess.run(["python", "../Scripts/ASM_Page.py", topic_folder_name, pdf_name, Topic_Name ])
