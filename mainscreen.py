from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image

# IconButton class
class IconButton(ButtonBehavior, BoxLayout):
    icon = StringProperty()
    text = StringProperty()

# MainScreen class
class MainScreen(Screen):
    pass
