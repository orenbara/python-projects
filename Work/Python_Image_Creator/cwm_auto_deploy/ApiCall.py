class ApiCall:
    def __init__(self):
        self.client_id = ""
        self.client_secret = ""
        self.final_image_dict = {}
        self.termination_response = None
        self.creation_response = None

    def get_id(self):
        return self.client_id

    def get_secret(self):
        return self.client_secret

    def get_cwm_headers(self):
        return {
            "AuthClientId": self.client_id,
            "AuthSecret": self.client_secret
        }

    def get_final_image_dict(self):
        return self.final_image_dict

    def set_id(self, new_id):
        self.client_id = new_id

    def set_secret(self, new_secret):
        self.client_secret = new_secret

    def set_final_image_dict(self, new_image_dict):
        self.final_image_dict = new_image_dict
