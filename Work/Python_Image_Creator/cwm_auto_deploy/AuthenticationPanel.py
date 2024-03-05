import tkinter as tk

class AuthenticationPanel(tk.Toplevel):
    def __init__(self,parent, api_call,*args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Widgets
        self.client_id_label = tk.Label(self, text="Client ID Key", font=("Ariel", 8, "bold"))
        self.client_id_label.pack()
        self.client_secret_label = tk.Label(self, text="Client Secret Key", font=("Ariel", 8, "bold"))
        self.client_secret_label.pack()
        self.client_id_entry = tk.Entry(self, width=70)
        self.client_id_entry.insert(0, string=f"AuthClientId here")
        self.client_id_entry.pack()
        self.client_secret_entry = tk.Entry(self, width=70)
        self.client_secret_entry.insert(0,string=f"AuthSecret here")
        self.client_secret_entry.pack()
        self.update_button = tk.Button(self, text="Update User Keys", command=self.update_button_clicked)
        self.update_button.pack()

        self.api_call = api_call

    def update_button_clicked(self):
        # Update the api_call object with the new Key data provided by the user.
        self.api_call.set_id(self.client_id_entry.get())
        self.api_call.set_secret(self.client_secret_entry.get())
        updated_auth_label = tk.Label(self, text="User Data Updated In The System", fg="green")
        updated_auth_label.pack()
