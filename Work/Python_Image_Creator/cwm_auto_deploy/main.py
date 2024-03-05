import os.path
import requests
import json
import tkinter as tk

# Class imports
import ApiCall
import AuthenticationPanel
import ImagePanel


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)  # create frame on top of Tk object - root
        self.image_panel = None
        self.parent = parent

        # Main Window Conf
        self.master.title("Create & Terminate QA VMs | By Orenb")
        self.master.geometry("600x500")
        # create a PhotoImage object from an image file
        self.my_image = tk.PhotoImage(file="logo.png")
        # create a Label widget and display the image
        self.label = tk.Label(self.master, image=self.my_image)
        self.label.pack()

        # Data
        self.api_call = ApiCall.ApiCall()  # Holds all data for the final api_call

        # Auth panel
        self.auth_panel_button = tk.Button(text="Open Authentication Panel", command=self.auth_panel_clicked)
        self.auth_panel_button.pack(pady=10)

        # Image Panel
        self.image_panel_button = tk.Button(text="Open Image Panel", command=self.image_panel_clicked)
        self.image_panel_button.pack(pady=10)

        # Show Summary of final images to create
        self.final_images_button = tk.Button(self, text="Show Final Images To Create", command=self.show_final_images)
        self.final_images_button.pack(pady=10)

        # Creation Of Images
        self.api_call.set_final_image_dict(self.image_panel)  # Update api_call with final images
        tk.Button(self, text="Create Images Based On 'Final Images To Create'", command=self.create_images).pack()

        # Terminate Of Images
        self.termination_button = tk.Button(self, text="Terminate Images (!After All Finished Creation!): all that "
                                                       "were created by the tool and exist",
                                            command=self.terminate_images)
        self.termination_button.pack(pady=10)

    def terminate_images(self):
        ## Termination Of Images ##
        # !!!! Change this function with care - Understand fully how it works first !!!!! #
        # This functionality is limited by CWM_API:
        # We can only terminate images based on ID right now, and also when creating new VM we don't get back its ID.
        # Since we can't get the ID of the VM created from the response we will stick to the following Rules:
        # We must call our images with a distinctive name that is very less likely be used by the customers:
        # testing.devopskb._qa_OMC${index} where ${index} will be provided by CWM (1,2,3...)
        def submit_termination():
            for server_id in filtered_data:
                confirm = "1"
                force = "1"
                params = {
                    "confirm": confirm,
                    "force": force
                }
                url = f"https://null.cloudwm.com/service/server/{server_id}/terminate"
                print(f"Terminating server ID: {server_id}")
                response = requests.delete(url, headers=headers, data=params)
                print(response.text)
                self.api_call.termination_response = response  # Update the termination response.
                tk.Label(termination_info_window, text=f"id:{server_id}, response:{self.api_call.termination_response}").pack()

        if self.api_call.get_id() == "" or self.api_call.get_secret() == "":
            error_dialog = tk.Toplevel()
            error_dialog.title("Error")
            error_dialog.geometry("400x70")
            error_label = tk.Label(error_dialog, text="Please Add Credentials to Authentication Panel")
            error_label.pack()
            ok_button = tk.Button(error_dialog, text="OK", command=error_dialog.destroy)
            ok_button.pack()
        else:
            # Get all VMs that correspond to the name testing.devopskb._qa_OMC${index}
            url = 'https://null.cloudwm.com/service/servers'
            headers = {
                'AuthClientId': self.api_call.get_id(),
                'AuthSecret': self.api_call.get_secret()
            }
            response = requests.get(url, headers=headers)

            # Careful! data variable contains all the servers related to user with given ID and Secret!
            data = json.loads(response.text)
            # filtered_data contains all the Server IDs with correspond to testing.devopskb._qa_OMC in their name
            filtered_data = [server['id'] for server in data if 'testing.devopskb._qa_OMC' in server['name']]
            print(f"IDs of servers to delete:\n{filtered_data}")
            filtered_data_names = [server['name'] for server in data if 'testing.devopskb._qa_OMC' in server['name']]

            ## Termination ##
            termination_info_window = tk.Toplevel(self.parent)
            termination_info_window.geometry("300x300")
            termination_info_window.title("Termination Info")
            ## Oren Testing - show data before termination ##
            listbox_termination = tk.Listbox(termination_info_window, width=120, selectmode=None)
            listbox_termination.pack()
            counter_list_box = 0
            for image_name in filtered_data_names:  # Values here are dicts
                counter_list_box += 1
                listbox_termination.insert(counter_list_box, image_name)
            tk.Button(termination_info_window, text="Confirm Termination", command=submit_termination).pack()



    def create_images(self):
        if self.api_call.get_id() == "" or self.api_call.get_secret() == "":
            error_dialog = tk.Toplevel()
            error_dialog.title("Error")
            error_dialog.geometry("400x70")
            error_label = tk.Label(error_dialog, text="Please Add Credentials to Authentication Panel")
            error_label.pack()
            ok_button = tk.Button(error_dialog, text="OK", command=error_dialog.destroy)
            ok_button.pack()

        else:
            # global create_label
            # Server Creation:
            vm_name = "testing.devopskb._qa_OMC"
            password = "Zaq1Xsw2Cde3"
            cpu = "2B"
            ram = "2048"
            disk_size_0 = "10"
            power = "0"
            network_name_0 = "wan"
            billing = "hourly"

            count = 1
            creation_info_window = tk.Toplevel(self.parent)
            creation_info_window.geometry("300x300")
            creation_info_window.title("Creation Info")
            #for key, value in self.image_panel.get_final_image_dict().items():
            for key, value in self.api_call.get_final_image_dict().items():
                # create_label["text"] += f"creating virtual machines for image: {key}\n"
                # print(f"creating virtual machine- {value}   in FULLCODE is- {key}")
                # current_image_ls = key.split(':') # List used to separate DC from Image Code
                # print(f"DC: {current_image_ls[0]}  in CODE is- {current_image_ls[1]}")
                # CWM Definitions:
                disk_src_0 = f"{key}"
                cwm_vm_config = {
                    "datacenter": f"{key.split(':')[0]}",
                    "name": f"{vm_name}",
                    "password": password,
                    "cpu": cpu,
                    "ram": ram,
                    "disk_size_0": disk_size_0,
                    "disk_src_0": disk_src_0,
                    "billing": billing,
                    "power": power,
                    "network_name_0": network_name_0,
                }
                # count += 1
                try:
                    print(f"creating {key}")
                    # create_label["text"] += f"instance number {str(i)}\n"
                    cwm_create_response_json = requests.post(url="https://console.kamatera.com/service/server",
                                                             headers=self.api_call.get_cwm_headers(), data=cwm_vm_config)
                    cwm_create_response_json.raise_for_status()
                    self.api_call.creation_response = cwm_create_response_json
                    tk.Label(creation_info_window, text=f"{value} response: {self.api_call.creation_response}").pack()
                except requests.exceptions.RequestException as e:
                    # error_label = Label(text=f"{e}", font=("Ariel", 8, "bold"))
                    # error_label.pack()
                    print("Error")

    def show_final_images(self):
        #self.image_panel.print_final_image_dict()
        final_image_window = tk.Toplevel(self.parent)

        #for key, value in self.image_panel.get_final_image_dict().items():
        if self.api_call.get_final_image_dict() != None:
            for key, value in self.api_call.get_final_image_dict().items():
                tk.Label(final_image_window, text=f"{(key, value)}").pack()

    def auth_panel_clicked(self):
        # Opens new window for authentication panel
        AuthenticationPanel.AuthenticationPanel(self.parent, self.api_call)
        print(self.api_call.get_id(), self.api_call.get_secret())

    def image_panel_clicked(self):
        # Opens new window for image panel
        self.image_panel = ImagePanel.ImagePanel(self.parent, self.api_call)


if __name__ == "__main__":
    root = tk.Tk()  # sent to parent(tk.Frame) of MainApplication class
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
