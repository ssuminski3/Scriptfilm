from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from webbrowser import open_new_tab
import requests
from kivy.logger import Logger


class SecondScreen(Screen):
    captions = False
    vertical = True

    def horizontal_alignment_pressed(self):
        self.ids.vertical_btn.disabled = False
        self.ids.horizontal_btn.disabled = True
        self.vertical = False
        Logger.info("Horizontal Alignment Button Pressed")

    def vertical_alignment_pressed(self):
        self.ids.vertical_btn.disabled = True
        self.ids.horizontal_btn.disabled = False
        self.vertical = True

    def validate_pexels_api_key(self, api_key):
        test_url = "https://api.pexels.com/v1/search?query=test"
        headers = {"Authorization": api_key}

        try:
            response = requests.get(test_url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            if response.status_code == 200:
                return True  # API key is valid
            else:
                return False
        except requests.exceptions.RequestException as e:
            self.ids.message_label.text = "Connect to internet"
            return False  # Return False in case of any exception

    def generate_xml(self, lang, api_key, title):
        global captions
        # Basic validation

        if not lang or not api_key or not title:
            print("Error: All fields are required.")
            self.ids.message_label.text = "Error: All fields are required."
            return

        if not self.validate_pexels_api_key(api_key):
            self.ids.message_label.text = "PEXEL API KEY is not working"
            return
        # Additional validations can be added here
        # For example, checking the length of the API key or the format of the language code

        # Extracting language code (assuming the format is 'code (language)')
        lang_code = lang.split(' ')[0] if ' ' in lang else lang
        v = "<vertical/>" if self.vertical else "<horizontal/>"
        # Generating XML
        xml_data = f"""<data>
        <head>
            <lang lang="{lang_code}"/>
            <pexel key="{api_key}"/>
            <output name="{title}"/>
            {v}
        </head>
        <body>"""

        # Output or process the XML data
        self.manager.get_screen('third').video_data = {"video": xml_data, "caption": self.captions}
        self.manager.current = 'third'

    def open_link(self):
        # Logic to open the link where users can get the Pexel API Key
        open_new_tab('https://www.pexels.com/api/new/')

    def on_checkbox_active(self, checkbox, value):
        global captions
        self.captions = value
    def build(self):
        return Builder.load_string(kv_string) # kv_string is the KV language string defined above
