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
from tkinter import messagebox, font, ttk
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
    yaml_raw_data = data
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
            if "editable" in widget:
                w["editable"] = widget["editable"]
            if "required" in widget:
                w["required"] = widget["required"]       
            if "default_text" in widget:
                w["default_text"] = widget["default_text"]   
            widgets.append(w)
        sections.append(create_section(title, widgets))
    return sections, yaml_raw_data

class FormUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Form UI")
        self.window.geometry("920x538")
        self.window.configure(bg = "#B1B3EC")
        self.window.resizable(False, False)
        self.current_section = 0
        self.sections = []
        self.form_data = {}
        self.tags_data = {}
        self.yaml_raw_data = []
        self.flag = {"Citation requirements" : True,
                     "Link to access" : True}    # Set and check if default value exists
        # Add an image
        img = Image.open(folder_path + 'docs\\_static\\Logo2-removebg-preview.png')
        width, height = img.size
        aspect_ratio = width/height
        new_height = 70
        new_width = int(new_height*aspect_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.window, image=img, bg= "#B1B3EC")
        panel.pack(side='top', fill='both', expand='yes')

        # create sections
        self.yaml_file_path = folder_path + "input.yaml" # testing yaml file
        self.sections_list, self.yaml_raw_data = convert_yaml_to_sections(self.yaml_file_path)
        self.sections = []
        for section in self.sections_list:
            self.sections.append(self.create_section(section['title'], section['widgets']))

        # create navigation buttons
        button_image_1 = ImageTk.PhotoImage(file=folder_path + 'docs\\_static\\button_1.png')
        button_image_2 = ImageTk.PhotoImage(file=folder_path + 'docs\\_static\\button_2.png')
        
        self.prev_button = tk.Button(self.window, 
                                     text="Prev", 
                                     state=tk.DISABLED, 
                                     command=self.show_prev_section, 
                                     image=button_image_1,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     activebackground="#B1B3EC")
        self.prev_button.pack(side=tk.LEFT, padx=30, pady= 200)
        self.next_button = tk.Button(self.window, text="Next", 
                                     command=self.show_next_section, 
                                     image=button_image_2,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     activebackground="#B1B3EC")
        self.next_button.pack(side=tk.RIGHT, padx=30, pady= 200)

        # show first section
        self.show_section(self.current_section)

        self.window.mainloop()

    def create_section(self, label_text, widgets):
        section = {
            "label": tk.Label(self.window, text=label_text, bg= "#B1B3EC"),
            "buffer": tk.Label(self.window, text="", bg= "#B1B3EC"), # buffer for spacing issues
            "widgets": []
        }
        
        for widget in widgets:
            if widget["type"] == "entry":
                frame = tk.Frame(self.window, bg= "#B1B3EC",width= 550, height = 50)
                try:
                    default_text = widget['default_text']
                except:
                    default_text = "Example: Placeholder"
                
                entry_widget = tk.Entry(frame, relief="solid")
                entry_widget.insert(0, default_text)
                entry_widget.config(fg='grey')
                section["widgets"].append({
                    "type": "entry",
                    "name": widget["label_text"],
                    "label": tk.Label(frame, text=widget["label_text"], bg= "#B1B3EC",pady=5),
                    "widget": entry_widget,
                    "required" : widget['required'],
                    "frame" : frame,
                    "default_text" : default_text
                })

            elif widget["type"] == "text":
                frame = tk.Frame(self.window, bg= "#B1B3EC",width= 550, height = 100)
                section["widgets"].append({
                    "type": "text",
                    "name": widget["label_text"],
                    "label": tk.Label(frame, text=widget["label_text"], bg= "#B1B3EC",pady=5),
                    "widget": tk.Text(frame, height=5,  width=30, relief="solid"),
                    "required" : widget['required'],
                    "frame" : frame
                })
            # elif widget["type"] == "checkbox":
            #     var1 = tk.IntVar()
            #     check_box = tk.Checkbutton(self.window, text='Python',variable=var1, onvalue=1, offvalue=0)
            #     section["widgets"].append({
            #         "type": "checkbox",
            #         "name": widget["label_text"],
            #         "widget": check_box,
            #         "required" : widget['required']
            #     })
            elif widget["type"] == "dropdown":
                if widget.get("multi_select"):
                    height_calculation = 120 if len(widget["options"])*20 <= 120 else len(widget["options"])*20 # To find the height of the multi choice dropbox
                    frame = tk.Frame(self.window, bg= "#B1B3EC", width= 550, height = height_calculation)
                    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, exportselection=0, height=len(widget["options"]), relief="solid")
                    for option in widget["options"]:
                        listbox.insert(tk.END, option)
                    section["widgets"].append({
                        "type": "dropdown_multi",
                        "name": widget["label_text"],
                        "label": tk.Label(frame, text=widget["label_text"]+" (Multi-Select)", bg= "#B1B3EC",pady=5),
                        "widget": listbox,
                        "is_tag": widget["Tags"],
                        "required" : widget['required'],
                        "frame" : frame
                    })
                else:
                    option_var = tk.StringVar()
                    frame = tk.Frame(self.window, bg= "#B1B3EC", width= 550, height = 50)
                    option_var.set(widget["options"][0])
                    widget_type = ttk.Combobox(frame, values=list(widget["options"]))  # , textvariable=option_var
                    widget_type['state'] = 'normal' if widget.get("editable")  else 'readonly'
                    section["widgets"].append({
                        "type": "dropdown_single",
                        "name": widget["label_text"],
                        "label": tk.Label(frame, text=widget["label_text"], bg= "#B1B3EC",pady=5),
                        "widget": widget_type, #readonly : if we want no editting
                        "options": option_var,
                        "is_tag": widget["Tags"],
                        "orig_data" : list(widget["options"]),
                        "required" : widget['required'],
                        "frame" : frame
                    })
        return section
    
    def validation(self, widg)->bool:
        for _ , widget in enumerate(widg):
            widget_type = widget["type"]
            if widget["required"] == True:
                if widget_type == "text":
                    data = "" if len(widget['widget'].get("1.0", tk.END)) == 1 else widget['widget'].get("1.0", tk.END)
                elif widget_type == "entry":
                    data = widget['widget'].get()
                elif widget_type == "dropdown_single":
                    data = widget['widget'].get()
                elif widget_type == "dropdown_multi":
                    selected_items = widget['widget'].curselection() #get selected items
                    data = [widget['widget'].get(i) for i in selected_items]

                if len(data) == 0:
                    messagebox.showinfo('Input Missing', widget['name'] + " can\'t be empty")
                    return False
         
        return True           
    
    def comboBoxUpdater(self,event):
        section = self.sections[self.current_section]
        countries_list = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
        if event.widget.get() == 'Country' or event.widget.get() == 'World' or event.widget.get() == 'Continent':
            index = 0
            for i, widget_dict in enumerate(section["widgets"]):
                if widget_dict["widget"] == event.widget:
                    index = i       
            temp = countries_list if event.widget.get() == 'Country' else [ 'Asia', 'South America', 'North America', 'Africa', 'Europe', 'Antarctica', 'Australia']
            section["widgets"][index + 1]["widget"]['values'] = temp
    
    def handle_focus_in(self,event,default_text):
        if event.widget.get() == default_text:
            event.widget.delete(0, tk.END)
        event.widget.config(fg='black')

    def handle_focus_out(self,event,default_text):
        if event.widget.get() == default_text or event.widget.get() == "":
            event.widget.delete(0, tk.END)
            event.widget.config(fg='grey')
            event.widget.insert(0, default_text)
             
    def show_section(self, section_index):

        section = self.sections[section_index]
        custom_font = font.Font(family='Helvetica', size=20, weight='bold')  # set a custom font
        custom_font_body = font.Font(family='Helvetica', size=14, weight='bold')  # set a custom font
        section_label = section["label"]
        section_label.config(font=custom_font)  # increase font size of the label
        section_label.pack()
        for widget_dict in section["widgets"]:
            widget_label = widget_dict["label"]
            widget_label.config(font=custom_font_body)
            widget_label.pack(side=tk.LEFT, pady = 10)
            widget_dict["widget"].pack(side=tk.RIGHT, pady = 10)
            widget_dict['frame'].pack(anchor =tk.W)
            widget_dict['frame'].pack_propagate(0)
            
            if widget_dict["name"] == "Citation requirements" and self.flag["Citation requirements"]: # Widget associated with the label and if it has already been changed.
                # Insert The Default value.
                default_text = 'For example "NREL (National Renewable Energy Laboratory). 2022. "2022 Annual Technology Baseline." Golden, CO: National Renewable Energy Laboratory. https://atb.nrel.gov/. "'
                widget_dict["widget"].insert(tk.END, default_text)     
                self.flag["Citation requirements"] = False 
                
            elif widget_dict["name"] == "Link to access" and self.flag["Link to access"]: # Widget associated with the label and if it has already been changed.
                # Insert The Default value.
                default_text = 'For example  https://atb.nrel.gov/'
                widget_dict["widget"].insert(tk.END, default_text)   
                self.flag["Link to access"] = False     

            widget_dict['widget'].bind('<<ComboboxSelected>>', self.comboBoxUpdater)
            if widget_dict["type"] == "entry": 
                widget_dict['widget'].bind("<FocusIn>", lambda event,default_text=widget_dict['default_text']:self.handle_focus_in(event,default_text))
                widget_dict['widget'].bind("<FocusOut>", lambda event,default_text=widget_dict['default_text']:self.handle_focus_out(event,default_text))
            
        buffer = section["buffer"]
        buffer.pack()
        
        self.current_section = section_index
        self.update_navigation_buttons()

    def hide_section(self, section_index):
        section = self.sections[section_index]
        section["label"].pack_forget()
        section['buffer'].pack_forget()
        for widget_dict in section["widgets"]:
            widget_dict["frame"].pack_forget()

    def show_next_section(self):
        section = self.sections[self.current_section ] # Retrieving data for the current page 
        # To enforce required condition
        local_flag = self.validation(section["widgets"])
       
        if self.current_section < len(self.sections) - 1 and local_flag == True:
            # save data from current section
            self.save_data(self.current_section)
            # hide current section
            self.hide_section(self.current_section)
            # show next section
            # Jump from spatial/temporal page to the citations page
            self.current_section = 4 if self.current_section == 2 or self.current_section == 3 or self.current_section == 4 else self.current_section
            # Assign current section value on the basis of wheather the user choose spatial or temporal as an option or nothing.
            self.current_section = self.current_section if self.current_section != 1 else (1 if section["widgets"][0]["widget"].get() == 'Spatial' else (3 if section["widgets"][0]["widget"].get() == "Spatial and Temporal" else 2))
            self.current_section += 1
            self.show_section(self.current_section)
        elif local_flag == True:
             self.submit_form()

    def show_prev_section(self):
        section = self.sections[1] # Retrieving data for the spatial/temporal option page 
        if self.current_section > 0:
            # save data from current section
            self.save_data(self.current_section)
            # hide current section
            self.hide_section(self.current_section)
            # show previous section     
            # Jump from spatial/temporal page to the options page
            self.current_section = 2 if self.current_section == 2 or self.current_section == 3 or self.current_section == 4 else self.current_section
            # Assign current section value on the basis of wheather the user choose spatial or temporal as an option or nothing.
            self.current_section = self.current_section if self.current_section != 5 else (3 if section["widgets"][0]["widget"].get() == 'Spatial' else (5 if section["widgets"][0]["widget"].get() == "Spatial and Temporal" else 4))
            self.current_section -= 1
            self.show_section(self.current_section)

    def update_navigation_buttons(self):
        if self.current_section == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.current_section == len(self.sections) - 1:
            self.next_button.config(text="Submit")
            self.next_button.config(command=self.show_next_section)
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
                data = widget_dict['widget'].get()
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
            messagebox.showerror("Error", "Dataset already exists!! Either check if data set is same or rename the dataset")
            return False

        os.mkdir(folder_path + f"src/delta_e/{dataset_name}")
        open(folder_path + f"src/delta_e/{dataset_name}/__init__.py", 'a').close()
        #open(folder_path + f"src/delta_e/{dataset_name}/{dataset_name}.py", 'a').close()

        # Create file in the directory
        file_path = folder_path + f"src/delta_e/{dataset_name}/__init__.py"
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
                tag_str+='\n\t'
        return tag_str

    def create_submit_file(self, data):
        # Define docstring format
        tags = self.get_tags()

        docstring = f'''"""\n        Module for {data['Dataset name']} Dataset

        '''
        # Add any remaining information to the docstring
        for key, value in data.items():
            docstring +="\n"
            docstring += f"        {key}:\n        {'-' * (len(key)+1)}\n        {value}\n"
        
        docstring+=f'''
        Tags:
        -----
        {tags}\n
        """'''

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
        
        #copy.deepcopy(self.form_data)
        self.update_yaml()
        docstring = self.create_submit_file(copy.deepcopy(self.form_data))

        if self.generate_page(docstring):
            messagebox.showinfo("Success", "Form submitted successfully! new file created at: " + folder_path + f"src/delta_e/{self.form_data['Dataset name']}/{self.form_data['Dataset name']}.py")
            self.clear_form()
            self.hide_section(self.current_section)
            self.show_section(0)
        
    def update_yaml(self)->None:
            if self.form_data['Project name'] not in self.sections[0]["widgets"][1]['orig_data']:
                # Create the updated list
                new_options = [self.form_data['Project name']] + self.sections[0]["widgets"][1]['orig_data']
                # Update the parent dictionary
                self.yaml_raw_data[0]['section']['widgets'][1].update({'options' : new_options})
                # Update the yaml file
                with open(self.yaml_file_path, mode="wt", encoding="utf-8") as file:
                    yaml.dump(self.yaml_raw_data, file)
              


if __name__ == "__main__":
    FormUI()
