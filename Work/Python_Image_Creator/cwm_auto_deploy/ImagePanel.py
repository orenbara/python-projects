import tkinter as tk
import requests
import json
from datetime import datetime
import re


class ImagePanel(tk.Toplevel):
    def __init__(self, parent, api_call, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # data:
        self.api_call = api_call
        self.optionsFile = "./options.json"
        self.cwm_headers = {
            "AuthClientId": api_call.get_id(),
            "AuthSecret": api_call.get_secret()
        }
        # Make json file from option_file
        with open(self.optionsFile, 'r') as options_file_opened:
            self.options_json = json.load(options_file_opened)
        self.filtered_dict = {}  # will hold filtered {"DC:ID" : "IMAGE NAME",...} data
        self.final_image_dict = {}  # holds final images to create

        # Widgets
        self.title = tk.Label(self, text="Follow the configuration from top to bottom, red are mandatory")
        # Refresh images
        self.refresh_label = tk.Label(self, text="\nOptional - Refresh data from CWM", fg="green")
        self.refresh_label.pack()
        self.refresh_options_button = tk.Button(self, text="Read Images From CWM - !!! 2 MINUTES PROCESS !!!",
                                                command=self.refresh_options_button_clicked)
        self.refresh_options_button.pack()
        # dc list
        self.dc_label = tk.Label(self, text="\nRemove irrelevant data-centers from the list", fg="red")
        self.dc_label.pack()
        self.dc_list = ["AS", "CA-TR", "EU", "EU-FR", "EU-LO", "IL", "IL-HA", "IL-PT", "IL-RH", "IL-TA", "US-NY2",
                        "US-SC", "US-TX"]
        self.dc_entry = tk.Entry(self, width=100)
        self.dc_entry.insert(0, string=f"{self.dc_list}")
        self.dc_entry.pack()
        self.filtered_dc_list = list(self.dc_entry.get().strip(" ").strip("[]").replace("'", "").replace(" ", "").split(
            ","))  # DC list filtered by user
        # pattern
        self.pattern_label = tk.Label(self, text="\nProvide Regex To Match Image Name", fg="red")
        self.pattern_label.pack()
        self.pattern = "(?=ubuntu_server_20.04_64-bit_optimized.*)(?!.*updated.*)"  # Regax pattern provided by the user
        self.pattern_entry = tk.Entry(self, width=100)
        self.pattern_entry.insert(0,
                                  string=f"REGAX here, EXAMPLE - (?=ubuntu_server_20.04_64-bit_optimized.*)(?!.*updated.*)")
        self.pattern_entry.pack()
        # search images (based on given dc and pattern)
        self.search_images_button = tk.Button(self, text="Search Images Based On Datacenters And Regex Pattern",
                                              command=self.search_images_button_clicked)
        self.search_images_button.pack()

    def search_images_button_clicked(self):

        def submit_button_clicked():
            selected_items = [listbox.get(idx) for idx in listbox.curselection()]
            print(selected_items)
            for current_tuple in selected_items:
                self.final_image_dict[current_tuple[0]] = current_tuple[1]
            self.api_call.set_final_image_dict(self.final_image_dict)
            filtered_images_window.destroy()
            self.destroy()

        # Will contain images as user filtered, structure: { DC : {disk_images_with_pattern - DICT} }
        self.filtered_dict = {}

        # Get DCs which the user chose
        self.filtered_dc_list = list(self.dc_entry.get().strip(" ").strip("[]").replace("'", "").replace(" ", "").split(
            ","))  # DC list filtered by user

        # Find Pattern, results (images: dc|imageID) placed in filtered_dict
        self.pattern = self.pattern_entry.get()
        for data_center in self.filtered_dc_list:
            disk_images_with_pattern = {disk_image["id"]: disk_image['description'] for disk_image in
                                        self.options_json['diskImages'][data_center] if
                                        bool(re.findall(self.pattern, disk_image['description']))}
            self.filtered_dict[data_center] = disk_images_with_pattern

        # Open new window with filtered image options:
        filtered_images_window = tk.Toplevel(self.parent)
        listbox = tk.Listbox(filtered_images_window, width=120, selectmode=tk.MULTIPLE)
        listbox.pack()
        counter_list_box = 0
        for optional_images_dict in self.filtered_dict.values():  # Values here are dicts
            counter_list_box += 1
            for key, value in optional_images_dict.items():
                listbox.insert(counter_list_box, (key, value))
        tk.Button(filtered_images_window, text="submit images", command=submit_button_clicked).pack()

        """
        OLD Version With checkboxes

        def submit_button_clicked():
            # Adds users chosen images to final_image_dict (the keys are the images codes for creation)
            for item in checkbox_vars:
                if item[1].get() == True:
                    #print(f"Adding {item[0]} to final images(if not already in)")
                    self.final_image_dict[item[0][0]]=item[0][1]
                elif item[0][0] in self.final_image_dict:
                    #print(f"Removing {item[0]} from final images(if exists)")
                    self.final_image_dict.pop(item[0][0])
        
        
        checkbox_vars = [] # will hold checked items
        # Create a dictionary to store the selected choices for each key
        for optional_images_dict in self.filtered_dict.values(): # Values here are dicts
            for key,value in optional_images_dict.items():
                #tk.Label(filtered_images_window,text=(key,value)).pack()
                checkbox_var = tk.BooleanVar()  # create a BooleanVar to hold the checkbox state
                checkbox = tk.Checkbutton(filtered_images_window, text=(key,value), variable=checkbox_var)
                checkbox.pack()
                checkbox_vars.append(((key,value), checkbox_var))  # add the BooleanVar to the list
        tk.Button(filtered_images_window, text="submit images", command=submit_button_clicked).pack()
        """

    def refresh_options_button_clicked(self):
        if self.api_call.get_id() == "" or self.api_call.get_secret() == "":
            error_dialog = tk.Toplevel()
            error_dialog.title("Error")
            error_dialog.geometry("400x70")
            error_label = tk.Label(error_dialog, text="Please Add Credentials to Authentication Panel")
            error_label.pack()
            ok_button = tk.Button(error_dialog, text="OK", command=error_dialog.destroy)
            ok_button.pack()

        else:
            with open(self.optionsFile, 'w') as options_file_opened:
                try:
                    self.refresh_label["text"] = "Refreshing"
                    cwm_response = requests.get(url="https://console.kamatera.com/service/server",
                                                headers=self.cwm_headers)
                    cwm_response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(e.response.text)
                    self.refresh_label["text"] = e.response.text
                else:
                    # Writing JSON to file to save time for adjacent executions.
                    options_file_opened = json.dump(cwm_response.json(), options_file_opened, indent=4)
                    self.refresh_label["text"] = f"Refreshed, {datetime.now()}"

    def get_final_image_dict(self):
        return self.final_image_dict

    def print_final_image_dict(self):
        json_formatted_str = json.dumps(self.final_image_dict, indent=2)
        print(json_formatted_str)
