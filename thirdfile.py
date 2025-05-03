from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class MediaSearchComponent(BoxLayout):
    def __init__(self, **kwargs):
        super(MediaSearchComponent, self).__init__(**kwargs)
        Clock.schedule_once(self.post_init)

    def post_init(self, dt):
        self.populate_media_dropdown()
        self.populate_language_dropdown()
        # Set default text for media_button by accessing the text of the first Button added to the media_dropdown
        if self.ids.media_dropdown.children:
            # Find the first Button in the children list (note: children are in reverse order)
            for child in reversed(self.ids.media_dropdown.children):
                if isinstance(child, Button):
                    self.ids.media_button.text = child.text
                    break
    def set_media_type(self, media_type):
        self.ids.media_button.text = media_type
        self.ids.media_dropdown.dismiss()

    dictionary = {
        "Videos from PEXEL": "pexelvideo",
        "Image from PEXEL": "pexelimg",
        "Image from GOOGLE \n(you may don't have rights for that image)": "googleimg"
    }

    def populate_media_dropdown(self):
        dropdown = self.ids['media_dropdown']
        for media_type in ["Videos from PEXEL", "Image from PEXEL", "Image from GOOGLE \n(you may don't have rights for that image)"]:
            btn = Button(text=media_type, size_hint_y=None, height=60)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
    def delete_self(self):
        # This function will be called to remove the widget from its parent
        self.parent.remove_widget(self)
    def populate_language_dropdown(self):
        dropdown = self.ids.language_dropdown
        languages = {
            'af': 'Afrikaans', 'ar': 'Arabic', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan', 'cs': 'Czech',
            'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'eo': 'Esperanto',
            'es': 'Spanish', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'hi': 'Hindi',
            'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'is': 'Icelandic',
            'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean',
            'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi',
            'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish',
            'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak',
            'sq': 'Albanian', 'sr': 'Serbian', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili',
            'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish',
            'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-CN': 'Chinese'
        }

        for code, lang in languages.items():
            btn = Button(text=f"{code} ({lang})", size_hint_y=None, height=60)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

    def get_data(self):
        # Collect data from the component's widgets
        media_type = self.ids.media_button.text
        keyword = self.ids.keyword_input.text
        text = self.ids.text_input.text
        language = self.ids.language_button.text

        return {
            'media_type': self.dictionary[media_type],
            'keyword': keyword,
            'text': text,
            'language': language
        }

    def validate_inputs(self):
        # Example validation logic
        errors = []
        if not self.ids.keyword_input.text.strip():
            errors.append("Keyword is empty")
        if not self.ids.text_input.text.strip():
            errors.append("Text is empty")
        if self.ids.media_button.text == 'Select Media Type':
            errors.append("Media type not selected")

        return errors

class MediaComponent(BoxLayout):
    global filepath
    def __init__(self, **kwargs):
        super(MediaComponent, self).__init__(**kwargs)
        self.file_path = None  # Initialize file_path attribute
        Clock.schedule_once(self.post_init)

    def post_init(self, dt):
        self.populate_media_dropdown()
        self.populate_language_dropdown()
        # Set default text for media_button by accessing the text of the first Button added to the media_dropdown
        if self.ids.media_dropdown.children:
            # Find the first Button in the children list (note: children are in reverse order)
            for child in reversed(self.ids.media_dropdown.children):
                if isinstance(child, Button):
                    self.ids.media_button.text = child.text
                    break
    def set_media_type(self, media_type):
        self.ids.media_button.text = media_type
        self.ids.media_dropdown.dismiss()

    def open_file_dialog(self):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.on_file_chosen)
        self.file_chooser = Popup(title="Choose a file", content=file_chooser, size_hint=(0.9, 0.9))
        self.file_chooser.open()

    def on_file_chosen(self, instance, value, *args):
        file_path = value[0]
        self.file_path = file_path  # Store the file_path as an attribute
        self.file_chooser.dismiss()
        self.ids.select_file.text = file_path

    def populate_media_dropdown(self):
        dropdown = self.ids['media_dropdown']
        for media_type in ["video", "image"]:
            btn = Button(text=media_type, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

    def delete_self(self):
        # This function will be called to remove the widget from its parent
        self.parent.remove_widget(self)
    def populate_language_dropdown(self):
        dropdown = self.ids.language_dropdown
        languages = {
            'current': 'o', 'te': 'Telugu', 'en': 'English', 'es': 'Spanish', 'fr': 'French',   # Add all other languages here
        }
        for code, lang in languages.items():
            btn = Button(text=f"{code} ({lang})", size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

    def get_data(self):
        # Collect data from the component's widgets
        media_type = self.ids.media_button.text
        text = self.ids.text_input.text
        language = self.ids.language_button.text

        return {
            'media_type': media_type,
            'file':  self.file_path,
            'text': text,
            'language': language
        }

    def validate_inputs(self):
        # Example validation logic
        errors = []
        if not self.file_path:
            errors.append("You didn't chosed file.")
        if not self.ids.text_input.text.strip():
            errors.append("Text is empty")
        if self.ids.media_button.text == 'Select Media Type':
            errors.append("Media type not selected")

        return errors


components =[]
class ThirdScreen(Screen):
    global components

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def add_media_search_component(self):
        component = MediaSearchComponent(size_hint_y=None, height=200)
        self.ids.container.add_widget(component, index=0)
        self.ids.container.do_layout()

    def add_media_component(self):
        component = MediaComponent(size_hint_y=None, height=200)
        self.ids.container.add_widget(component, index=0)
        self.ids.container.do_layout()

    def create_video(self):
        global components
        all_valid = True
        validation_messages = ""

        for component in reversed(self.ids.container.children):
            if isinstance(component, MediaSearchComponent):
                errors = component.validate_inputs()
                if errors:
                    all_valid = False
                    validation_messages += "\n".join(errors) + "\n---\n"
                else:
                    components.append(component.get_data())
                    self.ids.container.remove_widget(component)
            if isinstance(component, MediaComponent):
                errors = component.validate_inputs()
                if errors:
                    all_valid = False
                    validation_messages += "\n".join(errors) + "\n---\n"
                else:
                    components.append(component.get_data())
                    self.ids.container.remove_widget(component)

        if all_valid:
            # Proceed with creating video
            ret = ""
            print(components)
            #tu zmienić
            for c in components:
                n = ""
                t = c["language"].split(" ")[0]
                if t != "current":
                    n = ' lang="'+t+'"'
                if "keyword" in c and c["keyword"]:
                    ret += '<'+c["media_type"]+' keyword="'+c["keyword"]+'"'+n+">"+c["text"]+'</'+c["media_type"]+'>\n'
                if "file" in c and c["file"]:
                    ret += '<' + c["media_type"] + ' src="' + c["file"] + '"' + n + ">" + c["text"] + '</' + c["media_type"] + '>\n'
            print(ret)
            xml = self.video_data["video"]+ret+"</body>\n</data>"
            self.manager.get_screen('load').full_video = {"video": xml, "caption": self.video_data["caption"]}
            self.manager.get_screen('third').video_data = None
            xml = None

            self.manager.current = 'load'
            components = []

        else:
            # Show validation errors
            print("Validation Errors:\n", validation_messages)
            self.display_validation_errors(validation_messages)

    def display_validation_errors(self, messages):
        # Display the validation messages on the screen
        # This could be a Label or a Popup depending on how you want to show it
        self.ids.validation_label.text = messages