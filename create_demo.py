import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, "demo_workspace")

# Clear the workspace if it exists
if os.path.exists(WORKSPACE_DIR):
    shutil.rmtree(WORKSPACE_DIR)

os.makedirs(WORKSPACE_DIR)

files_to_create = [
    "notes.txt", "financial_report.pdf", "data_dump.xlsx",
    "vacation_photo.jpeg", "company_logo.png",
    "cool_script.py", "website_index.html",
    "old_backup.zip", "unknown_file.xyz"
]

for filename in files_to_create:
    filepath = os.path.join(WORKSPACE_DIR, filename)
    with open(filepath, 'w') as f:
        f.write("This is a mock file for testing the Self-Learning AI Agent.\n")

print(f"Demo environment created successfully at {WORKSPACE_DIR}")
