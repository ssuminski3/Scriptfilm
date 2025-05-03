from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from mainscreen import MainScreen
from secondscreen import SecondScreen
from kivy.config import Config
from thirdfile import ThirdScreen
from kivy.logger import Logger
from LoadScreen import LoadScreen
from fourthScreen import FourthScreen
Logger.setLevel('WARNING')

Builder.load_file('mainscreen.kv')
Builder.load_file('secondscreen.kv')
Builder.load_file('thirdfile.kv')
Builder.load_file('load.kv')
Builder.load_file('fourth.kv')

class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name="third"))
        sm.add_widget(LoadScreen(name="load"))
        sm.add_widget(FourthScreen(name="fourth"))
        Config.set('kivy', 'window_icon', 'ScriptFilmIcon.ico')
        self.title = "ScriptFilm"
        return sm


if __name__ == '__main__':
    MyApp().run()
