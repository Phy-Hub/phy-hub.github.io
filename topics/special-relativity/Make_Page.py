import subprocess

# cd .\topics\special-relativity\

Topic_Name = "Special Relativity"

topic_folder_name = Topic_Name.replace(" ", "-").lower()
pdf_name = "Handbook_of_" + Topic_Name.replace(" ", "_") + ".pdf"
subprocess.run(["python", "../SCRIPTS/ASM_Page.py", topic_folder_name, pdf_name, Topic_Name ])
