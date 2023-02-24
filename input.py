import os
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

def create_submit_file():
    # Get input values from text boxes
    project_name = project_name_box.get()
    description = description_box.get('1.0', 'end-1c')
    tags = tags_box.get().split(', ')
    purpose = purpose_box.get('1.0', 'end-1c')

    # Define docstring format
    docstring = f'''"""
{project_name}
{'=' * len(project_name)}

{description}


Tags
----
{', '.join(tags)}


Purpose of Dataset
------------------
{purpose}
"""'''

    # Create directory if it does not exist
    if not os.path.exists(project_name):
        os.mkdir(project_name)
        open(f"src/delta_e/{project_name}/__init__.py", 'a').close()

    # Create file in the directory
    file_path = f"{project_name}/{project_name}.py"
    with open(file_path, 'w') as f:
        f.write(docstring)

    # Clear the form
    project_name_box.delete(0, 'end')
    description_box.delete('1.0', 'end')
    tags_box.delete(0, 'end')
    purpose_box.delete('1.0', 'end')

    # Save the current directory
    current_dir = os.getcwd()

    # Change to the directory where the Makefile is located
    makefile_dir = 'docs'
    os.chdir(makefile_dir)

    # Run the "make html" command
    subprocess.run(['make', 'html'])

    # Change back to the original directory
    os.chdir(current_dir)


# Create Tkinter window
window = tk.Tk()
window.title('Create Python File')
window.geometry('400x400')

# Add an image
img = Image.open('docs/_static/Logo2.png')
width, height = img.size
aspect_ratio = width/height
new_height = 50
new_width = int(new_height*aspect_ratio)
img = img.resize((new_width, new_height), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = tk.Label(window, image=img)
panel.pack(side='top', fill='both', expand='yes')

# Project name input
project_name_label = tk.Label(window, text='Project Name', font=('Arial', 18))
project_name_label.pack()
project_name_box = tk.Entry(window)
project_name_box.pack()

# Description input
description_label = tk.Label(window, text='Description', font=('Arial', 18))
description_label.pack()
description_box = tk.Text(window, height=5)
description_box.pack()

# Tags input
tags_label = tk.Label(window, text='Tags (comma separated)', font=('Arial', 18))
tags_label.pack()
tags_box = tk.Entry(window)
tags_box.pack()

# Purpose input
purpose_label = tk.Label(window, text='Purpose of Dataset', font=('Arial', 18))
purpose_label.pack()
purpose_box = tk.Text(window, height=5)
purpose_box.pack()

# Submit button
submit_button = tk.Button(window, text='Create File', command=create_submit_file, font=('Arial', 18))
submit_button.pack()

# Run window
window.mainloop()
