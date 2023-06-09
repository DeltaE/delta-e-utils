'''
NOTE: remove line 66:70 to run this file  

The code provided is a Python script that creates a graphical user interface (GUI) for a form using the tkinter module. It also converts a YAML file into form sections and widgets, and allows for navigation between these sections. Here is a detailed breakdown of each part of the code:

Imported modules:
- `os`: provides a way to interact with the operating system, e.g., reading and writing files.
- `subprocess`: allows running a command as a subprocess of the current Python process.
- `copy`: provides a way to copy objects, including deep copies of nested objects.
- `yaml`: allows reading and writing YAML files.

In addition to these modules, it also imports several classes and functions from the tkinter and Pillow modules:
- `tkinter.Tk`: the main window of the GUI.
- `tkinter.messagebox`: provides a way to display message boxes.
- `tkinter.font`: allows setting a custom font for labels.
- `PIL.Image`: provides a way to read and manipulate image files.
- `PIL.ImageTk`: allows displaying PIL images in a tkinter window.

The following functions and classes are defined in the script:

Function `create_section(title, widgets)`:
- Takes two arguments: `title` (a string) and `widgets` (a list of dictionaries).
- Returns a dictionary with two keys: "title" (the value of the `title` argument) and "widgets" (the value of the `widgets` argument).

Function `convert_yaml_to_sections(yaml_file)`:
- Takes one argument: `yaml_file` (a string representing the path to a YAML file).
- Opens the specified YAML file and converts it into a Python object using the `yaml.load()` function.
- Creates a list of sections (each section is a dictionary with "title" and "widgets" keys) by iterating through the items in the Python object.
- Returns the list of sections.

Class `FormUI`:
- Initializes the main window of the GUI (`self.window`) with a title ("Form UI").
- Defines several instance variables:
  - `self.current_section` (an integer representing the index of the currently displayed section).
  - `self.sections` (a list of dictionaries, each representing a form section).
  - `self.form_data` (a dictionary containing the user's input data for each widget).
  - `self.tags_data` (a dictionary containing the user's input data for each "tag" widget, which allows for selecting multiple options).
- Loads an image file and displays it in the window.
- Converts a YAML file into a list of sections using the `convert_yaml_to_sections()` function and creates a corresponding list of section dictionaries using the `create_section()` function.
- Defines two navigation buttons ("Prev" and "Next") and displays them in the window.
- Calls the `show_section()` method to display the first section.
- Defines several methods:
  - `create_section(label_text, widgets)`: similar to the `create_section()` function above, but creates a dictionary with "label" (a tkinter Label object) and "widgets" (a list of widget dictionaries) keys.
  - `show_section(section_index)`: displays the section at the specified index by packing the section label and each widget label and widget.
  - `hide_section(section_index)`: hides the section at the specified index by forgetting the section label and each widget label and widget.
  - `show_next_section()`: called when the "Next" button is clicked; saves the user's input data for the current section, hides the current section, displays the next section, and updates the navigation buttons.
  - `show_prev_section()` - Hides current section, saves data, and shows previous section in a multi-section form.
  - `update_navigation_buttons()` - Updates the state of the navigation buttons based on the current section in a multi-section form.
  - `save_data(section_index)` - Saves the user input data from the current section of a multi-section form.
  - `clear_form()` - Clears the user input data in a multi-section form.
  - `generate_page(docstring)` - Generates a page in HTML format by creating a directory, a file, and running the Makefile command.
  - `get_tags()` - Extracts the tag from the label of a multi-select dropdown widget and returns a formatted string.
  - `create_submit_file(data)` - Creates a submit file by formatting the data dictionary and returning a string representation.
  
  Important notes: 
  When running locally uncomment the lines having 'folder_path' in it, and comment the line just after that.  
'''
import os
import subprocess
import copy
import yaml
import sys
import re

import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk

# Get current folder path
folder_path = os.getcwd() + "\\"

# Get the path of the executable file
exe_dir = os.path.dirname(sys.executable)

# Change the working directory to the directory containing the executable file
os.chdir(exe_dir)

def create_section(title, widgets):
    section = {}
    section["title"] = title
    section["widgets"] = widgets
    return section

def convert_yaml_to_sections(yaml_file):
    with open(yaml_file, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    sections = []
    for section in data:
        title = section["section"]["title"]
        widgets = []
        for widget in section["section"]["widgets"]:
            w = {}
            w["type"] = widget["type"]
            w["label_text"] = widget["label_text"]
            if "options" in widget:
                w["options"] = widget["options"]
            if "multi_select" in widget:
                w["multi_select"] = widget["multi_select"]
            if "Tags" in widget:
                w["Tags"] = widget["Tags"]
            widgets.append(w)
        sections.append(create_section(title, widgets))
    return sections

class FormUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Form UI")
        self.current_section = 0
        self.sections = []
        self.form_data = {}
        self.tags_data = {}

        # Add an image
        img = Image.open(folder_path + 'docs/_static/Logo2.png')
        width, height = img.size
        aspect_ratio = width/height
        new_height = 50
        new_width = int(new_height*aspect_ratio)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.window, image=img)
        panel.pack(side='top', fill='both', expand='yes')

        # create sections
        self.sections_list = convert_yaml_to_sections(folder_path + "input.yaml")
        self.sections = []
        for section in self.sections_list:
            self.sections.append(self.create_section(section['title'], section['widgets']))

        # create navigation buttons
        self.prev_button = tk.Button(self.window, text="Prev", state=tk.DISABLED, command=self.show_prev_section)
        self.prev_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.window, text="Next", command=self.show_next_section)
        self.next_button.pack(side=tk.RIGHT)

        # show first section
        self.show_section(self.current_section)

        self.window.mainloop()

    def create_section(self, label_text, widgets):
        section = {
            "label": tk.Label(self.window, text=label_text),
            "widgets": []
        }
        for widget in widgets:
            if widget["type"] == "entry":
                section["widgets"].append({
                    "type": "entry",
                    "name": widget["label_text"],
                    "label": tk.Label(self.window, text=widget["label_text"]),
                    "widget": tk.Entry(self.window)
                })
            elif widget["type"] == "text":
                section["widgets"].append({
                    "type": "text",
                    "name": widget["label_text"],
                    "label": tk.Label(self.window, text=widget["label_text"]),
                    "widget": tk.Text(self.window, height=5,  width=40)
                })
            elif widget["type"] == "dropdown":
                if widget.get("multi_select"):
                    listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE, exportselection=0, height=len(widget["options"]))
                    for option in widget["options"]:
                        listbox.insert(tk.END, option)
                    section["widgets"].append({
                        "type": "dropdown_multi",
                        "name": widget["label_text"],
                        "label": tk.Label(self.window, text=widget["label_text"]+" (Multi-Select)"),
                        "widget": listbox,
                        "is_tag":widget["Tags"]
                    })
                else:
                    option_var = tk.StringVar()
                    option_var.set(widget["options"][0])
                    section["widgets"].append({
                        "type": "dropdown_single",
                        "name": widget["label_text"],
                        "label": tk.Label(self.window, text=widget["label_text"]),
                        "widget": tk.OptionMenu(self.window, option_var, *widget["options"]),
                        "options": option_var,
                        "is_tag":widget["Tags"]
                    })
        return section

    def show_section(self, section_index):

        section = self.sections[section_index]
        custom_font = font.Font(family='Helvetica', size=20, weight='bold')  # set a custom font
        section_label = section["label"]
        section_label.config(font=custom_font)  # increase font size of the label
        section_label.pack()
        for widget_dict in section["widgets"]:
            widget_dict["label"].pack()
            widget_dict["widget"].pack()
        self.current_section = section_index
        self.update_navigation_buttons()

    def hide_section(self, section_index):
        section = self.sections[section_index]
        section["label"].pack_forget()
        for widget_dict in section["widgets"]:
            widget_dict["label"].pack_forget()
            widget_dict["widget"].pack_forget()

    def show_next_section(self):
        if self.current_section < len(self.sections) - 1:
            # save data from current section
            self.save_data(self.current_section)
            # hide current section
            self.hide_section(self.current_section)
            # show next section
            self.current_section += 1
            self.show_section(self.current_section)

    def show_prev_section(self):
        if self.current_section > 0:
            # save data from current section
            self.save_data(self.current_section)
            # hide current section
            self.hide_section(self.current_section)
            # show previous section
            self.current_section -= 1
            self.show_section(self.current_section)

    def update_navigation_buttons(self):
        if self.current_section == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.current_section == len(self.sections) - 1:
            self.next_button.config(text="Submit")
            self.next_button.config(command=self.submit_form)
        else:
            self.next_button.config(text="Next")
            self.next_button.config(command=self.show_next_section)

    def save_data(self, section_index):
        section = self.sections[section_index]
        for widget_dict in section["widgets"]:
            widget = widget_dict["widget"]
            widget_type = widget_dict["type"]
            if widget_type == "text":
                data = widget.get("1.0", tk.END)
            elif widget_type == "entry":
                data = widget.get()
            elif widget_type == "dropdown_single":
                data = widget_dict['options'].get()
            elif widget_type == "dropdown_multi":
                selected_items = widget_dict['widget'].curselection() #get selected items
                data = [widget_dict['widget'].get(i) for i in selected_items]
                label_text = widget_dict["label"]["text"]
                self.tags_data[label_text] = data
            label_text = widget_dict["label"]["text"]
            if widget_type == "dropdown_multi" and widget_dict["is_tag"]:
                self.tags_data[label_text] = data
            else:
                self.form_data[label_text] = data
    
    def clear_form(self):
        for section in self.sections:
            for widget_dict in section["widgets"]:
                widget_type = widget_dict["type"]
                widget_name = widget_dict["name"]
                widget = widget_dict["widget"]
                if widget_type == "entry":
                    widget.delete("0", tk.END)  # clear the widget's value
                elif widget_type == "text":
                    widget.delete("1.0", tk.END)  # clear the widget's value
                elif widget_type == "dropdown":
                    #widget_options = widget_dict["options"]
                    #widget.set(widget_options[0])  # set dropdown back to first option
                    print("WARNING: dropdown were not cleared")
                self.form_data[widget_name] = ""  # clear the corresponding form data

    def generate_page(self, docstring):
        # Create directory if it does not exist
        # TODO: change the working to current directory
        current_dir = ''
        dataset_name = self.form_data['Dataset name']
        if os.path.exists(folder_path + f"src\\delta_e\\{dataset_name}"):
            messagebox.showinfo("Errror", "Dataset already exists!! either check if data set is same or rename the dataset")
            return False

        os.mkdir(folder_path + f"src/delta_e/{dataset_name}")
        open(folder_path + f"src/delta_e/{dataset_name}/__init__.py", 'a').close()
        open(folder_path + f"src/delta_e/{dataset_name}/{dataset_name}.py", 'a').close()

        # Create file in the directory
        file_path = folder_path + f"src/delta_e/{dataset_name}/{dataset_name}.py"
        with open(file_path, 'w') as f:
            f.write(docstring)

        current_dir = os.getcwd()

        # Change to the directory where the Makefile is located
        makefile_dir = 'docs'
        os.chdir(folder_path + makefile_dir)

        # Run the "make html" command
        #subprocess.run(['make', 'html'])

        # Change back to the original directory
        os.chdir(current_dir)

        return True
    
    def get_tags(self):
        #.replace("(Multi-Select)", "").strip()
        # TODO: {data.pop('Dataset name', 'N/A')}
        tag_str = ""
        for key, values in self.tags_data.items():
            # Extract the tag from the key by removing '(Multi-Select)', 'when adding Tags:', and trimming whitespace
            tag = key.replace('(Multi-Select)', '').strip()
            # Extract the values from the list and join them with commas
            if values!=[]:
                for value in values:
                    # Add the tag and values to the tag_str
                    tag_str += f'{tag}:{value}, '
                tag_str+='\n'
        return tag_str

    def create_submit_file(self, data):
        # Define docstring format
        tags = self.get_tags()

        docstring = f'''"""module for {data['Dataset name']} dataset

Project name:
-------------
{data.pop('Project name', 'N/A')}

Tags:
-----
{tags}
Researcher Name:
----------------
{data.pop('Researcher Name', 'N/A')}

Dataset name:
-------------
{data.pop('Dataset name', 'N/A')}

Description
-------------
{data.pop('Description', 'N/A')}
Version:
---------
{data.pop('Version', 'N/A')}

Private or public:
-------------------
{data.pop('Private or public', 'N/A')}

Region:
--------
{data.pop('Region', 'N/A')}

Time Horizon:
-------------
{data.pop('Time Horizon From', 'N/A')} : {data.pop('Time Horizon To', 'N/A')}

Spatial Resolution:
-------------------
{data.pop('Spatial Resolution (km^2)', 'N/A')}

Link to access:
---------------
{data.pop('Link to access', 'N/A')}
Citation requirements:
----------------------
{data.pop('Citation requirements', 'N/A')}
Licensing requirements:
-----------------------
{data.pop('Licensing requirements', 'N/A')}
'''
        # Add any remaining information to the docstring
        for key, value in data.items():
            docstring+="\n"
            docstring += f"{key}:\n{'-' * (len(key)+1)}\n{value}\n"
        
        docstring+=f'"""'

        # Return docstring
        return docstring

    def validate_dataset_name(self):
        dataset_name = self.form_data['Dataset name']
        
        # Check if dataset name is empty
        if not dataset_name:
            messagebox.showinfo("", "Dataset name cannot be empty.")
            return False
        
        # Check for spaces/numbers/special characters and replace with underscore
        dataset_name = re.sub(r"[^a-zA-Z_]", "_", dataset_name)

        # Remove underscores at the beginning of the string until a character is encountered
        self.form_data['Dataset name'] = re.sub(r"^_+", "", dataset_name)
    
        return True
    
    def submit_form(self):
        # process the form data and submit it to the backend or perform any other action
        # you can access the form data stored in the self.form_data dictionary

        self.save_data(len(self.sections) - 1)

        if not self.validate_dataset_name():
            return
        
        copy.deepcopy(self.form_data)
        docstring = self.create_submit_file(copy.deepcopy(self.form_data))

        if self.generate_page(docstring):
            messagebox.showinfo("Success", "Form submitted successfully! new file created at:" + folder_path + f"src/delta_e/{self.form_data['Dataset name']}/{self.form_data['Dataset name']}.py")
            self.clear_form()
            self.hide_section(self.current_section)
            self.show_section(0)


if __name__ == "__main__":
    FormUI()
