"""import os
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
'''
{project_name}
{'=' * len(project_name)}

{description}


Tags
----
{', '.join(tags)}


Purpose of Dataset
------------------
{purpose}'''
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
"""

"""
Section 1:
Researcher name : Short written answer
Project name : Drop down menu (Checklist)
Dataset name : Short written answer
Description : Long written answer
Version : Short written answer
Private or public : Drop down menu (Checklist)



Section 2:
Region : Drop down menu (Checklist)
Time horizon : Drop down menu (Checklist)
Spatial resolution : Drop down menu (Checklist)
Temporal resolution : Drop down menu (Checklist)
Units : Long written answer


Section 3:
Link to access : Long written answer
Citation requirements : Long written answer
"""
import os
import subprocess

import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk


class FormUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Form UI")
        self.current_section = 0
        self.sections = []
        self.form_data = {}

        # Add an image
        img = Image.open('docs/_static/Logo2.png')
        width, height = img.size
        aspect_ratio = width/height
        new_height = 50
        new_width = int(new_height*aspect_ratio)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.window, image=img)
        panel.pack(side='top', fill='both', expand='yes')

        # create sections
        widgets_1 = [
            {"type": "entry", "label_text": "Researcher Name:"},
            {"type": "dropdown", "label_text": "Project name", "options": ['Atlantic Canada', 'BC Nexus', 'BC PyPSA', 'Canada-USA', 'CLEWs Canada', 'CLEWs Global', 'CLEWs Kenya', 'Energy Storage Modelling', 'Fleet Electrification', 'LCA', 'Laos Cascading Hydro', 'OSeMOSYS Global', 'Vancouver Island PyPSA'], "multi_select": False},
            {"type": "entry", "label_text": "Dataset name"},
            {"type": "entry", "label_text": "Version"},
            {"type": "dropdown", "label_text": "Private or public", "options": ["Private", "Public"], "multi_select": False}
        ]
        section_1 = self.create_section("Section 1", widgets_1)

        widgets_2 = [
            {"type": "dropdown", "label_text": "Region:", "options": ["World", "Continent", "Country"], "multi_select": False},
            {"type": "dropdown", "label_text": "Time Horizon From", "options": [2010,2011], "multi_select": False},
            {"type": "dropdown", "label_text": "Time Horizon To", "options": [2010,2011], "multi_select": False},

            {"type": "dropdown", "label_text": "Spatial Resolution (km^2)", "options": ['1-10', '10-100', '100-1000', '>1000'], "multi_select": False},
            {"type": "dropdown", "label_text": "Temporal Resolution", "options": ['Years', 'Months', 'Days', 'Hours', 'Minutes', 'Seconds'], "multi_select": True},
            {"type": "dropdown", "label_text": "Sector", "options": ['Agriculture', 'Residential', 'Commercial', 'Industrial', 'Transportation', 'Power'], "multi_select": True}
        ]
        section_2 = self.create_section("Section 2", widgets_2)


        widgets_3 = [            
            {"type": "text", "label_text": "Link to access"},
            {"type": "text", "label_text": "Citation requirements"}
        ]
        section_3 = self.create_section("Section 3", widgets_3)


        widgets_4 = [
            {"type": "dropdown", "label_text": "Sector", "options": ['Agriculture', 'Residential', 'Commercial', 'Industrial', 'Transportation', 'Power'], "multi_select": True},
            {"type": "dropdown", "label_text": "Uses", "options": ['Demand', 'Generation', 'Transmission', 'Infrastructure', 'Storage'], "multi_select": True},
            {"type": "dropdown", "label_text": "Area of Focus", "options": ['Technical', 'Environment', 'Economic', 'Social'], "multi_select": True},
        ]
        section_4 = self.create_section("TAGS", widgets_4)

        widgets_5 = [
            {"type": "dropdown", "label_text": "Data Type", "options": ['Geospatial', 'Tabular', 'Timeseries'], "multi_select": True},
            {"type": "dropdown", "label_text": "Resource Carrier", "options": ['Water', 'Gas', 'Wind', 'Oil', 'Biomass', 'Heating/Cooling', 'Hydro', 'Temperature', 'Land', 'Solar', 'Nuclear', 'Emissions', 'Waste', 'Hydrogen', 'Geothermal', 'Electricity'], "multi_select": True}
        ]
        section_5 = self.create_section("TAGS", widgets_5)


        self.sections = [section_1, section_2, section_3, section_4, section_5]

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
                    "widget": tk.Text(self.window, height=5)
                })
            elif widget["type"] == "dropdown":
                if widget.get("multi_select"):
                    listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE, exportselection=0)
                    for option in widget["options"]:
                        listbox.insert(tk.END, option)
                    section["widgets"].append({
                        "type": "dropdown_multi",
                        "name": widget["label_text"],
                        "label": tk.Label(self.window, text=widget["label_text"]),
                        "widget": listbox
                    })
                else:
                    option_var = tk.StringVar()
                    option_var.set(widget["options"][0])
                    section["widgets"].append({
                        "type": "dropdown_single",
                        "name": widget["label_text"],
                        "label": tk.Label(self.window, text=widget["label_text"]),
                        "widget": tk.OptionMenu(self.window, option_var, *widget["options"]),
                        "options": option_var
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
            
            print(data)
            label_text = widget_dict["label"]["text"]
            self.form_data[label_text] = data
    
    def clear_form(self):
        for section in self.sections:
            for widget_dict in section["widgets"]:
                widget_type = widget_dict["type"]
                widget_name = widget_dict["name"]
                widget = widget_dict["widget"]
                print(widget_name, widget_type)
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
        if not os.path.exists(f"src/delta_e/{dataset_name}"):
            os.mkdir(f"src/delta_e/{dataset_name}")
            open(f"src/delta_e/{dataset_name}/__init__.py", 'a').close()
            open(f"src/delta_e/{dataset_name}/{dataset_name}.py", 'a').close()


        # Create file in the directory
        file_path = f"src/delta_e/{dataset_name}/{dataset_name}.py"
        with open(file_path, 'w') as f:
            f.write(docstring)

        current_dir = os.getcwd()

        # Change to the directory where the Makefile is located
        makefile_dir = 'docs'
        os.chdir(makefile_dir)

        # Run the "make html" command
        subprocess.run(['make', 'html'])

        # Change back to the original directory
        os.chdir(current_dir)
    
    def create_labels(self):
        ## 
        return

    def create_page(self):
        ## 
        return
    def create_submit_file(self, data):
        # Get input values from data dictionary
        researcher_name = data['Researcher Name:']
        project_name = data['Project name']
        dataset_name = data['Dataset name']
        version = data['Version']
        private_or_public = data['Private or public']
        region = data['Region:']
        time_horizon_from = data['Time Horizon From']
        time_horizon_to = data['Time Horizon To']
        spatial_resolution = data['Spatial Resolution (km^2)']
        temporal_resolution = ', '.join(data['Temporal Resolution'])
        sector = ', '.join(data['Sector'])
        link_to_access = data['Link to access']
        citation_requirements = data['Citation requirements']
        uses = ', '.join(data['Uses'])
        area_of_focus = ', '.join(data['Area of Focus'])
        data_type = ', '.join(data['Data Type'])
        resource_carrier = ', '.join(data['Resource Carrier'])

        # Define docstring format
        docstring = f'''"""
    Researcher Name:
    ----------------
    {researcher_name}


    Project name:
    -------------
    {project_name}


    Dataset name:
    -------------
    {dataset_name}


    Version:
    --------
    {version}


    Private or public:
    ------------------
    {private_or_public}


    Region:
    -------
    {region}


    Time Horizon:
    -------------
    {time_horizon_from} : {time_horizon_to}


    Spatial Resolution:
    -------------------
    {spatial_resolution}


    Temporal Resolution:
    --------------------
    {temporal_resolution}


    Sector:
    -------
    {sector}


    Link to access:
    ---------------
    {link_to_access}


    Citation requirements:
    -----------------------
    {citation_requirements}


    Uses:
    -----
    {uses}


    Area of Focus:
    --------------
    {area_of_focus}


    Data Type:
    ----------
    {data_type}


    Resource Carrier:
    ------------------
    {resource_carrier}"""
    '''
        return docstring

    
    def submit_form(self):
        # process the form data and submit it to the backend or perform any other action
        # you can access the form data stored in the self.form_data dictionary
        # for example, to print the form data to the console, you can do the following:
        self.save_data(len(self.sections) - 1)
        print(self.form_data)

        docstring = self.create_submit_file(self.form_data)
        self.generate_page(docstring)

    
        messagebox.showinfo("Success", "Form submitted successfully!")

        self.clear_form()
        self.hide_section(self.current_section)
        self.show_section(0)

        self.create_page()

if __name__ == "__main__":
    FormUI()
