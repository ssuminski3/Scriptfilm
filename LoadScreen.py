from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import XMLReader
from threading import Thread
from threading import Event
from kivy.clock import Clock
import time
from kivy.uix.button import Button
import sys

class CustomOutputStream:
    def __init__(self, update_function):
        self.update_function = update_function

    def write(self, text):
        # Call the update function with the new text
        self.update_function(text)

    def flush(self):
        pass

class LoadScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadScreen, self).__init__(**kwargs)
        # Redirect sys.stdout to custom stream
        sys.stdout = CustomOutputStream(self.update_label)
    def on_enter(self):
        # Start the background task
        self.task_complete_event = Event()
        thread = Thread(target=self.read_xml, args=(self.full_video["video"], self.full_video["caption"], self.task_complete_event))

        thread.start()
        # Schedule the check for task completion
        Clock.schedule_interval(self.check_task_status, 1)

    def read_xml(self, video_path, caption_path, task_complete_event):
        try:
            XMLReader.Read(video_path, caption_path, task_complete_event)
        except Exception as e:
            # Handle the exception here, you might want to log the error
            print(f"Error in XMLReader: {e}")
            e = str(e)
            self.ids.status_label.text = e
        finally:
            # Set the event to notify the completion of the task, whether it succeeded or failed
            task_complete_event.set()

    def long_running_task(self):
        # This is your long-running task
        time.sleep(10)  # Example task: sleep for 10 seconds
        self.task_complete_event.set()

    def transition_to_main_screen(self, instance):
        # Remove the button from the layout
        self.ids.loading_image.source = 'loading.gif'
        self.ids.status_label.text = 'Loading...'
        for child in list(self.ids.layout.children):
            if isinstance(child, Button):
                self.ids.layout.remove_widget(child)
        # Transition to the main screen
        self.manager.current = 'main'
    def check_task_status(self, dt):
        if self.task_complete_event.is_set():
            self.ids.status_label.text = 'Task Complete!'
            self.manager.get_screen('load').full_video = None
            self.ids.loading_image.source = 'static_image.png'  # Stopping the animation
            Clock.unschedule(self.check_task_status)
            go_to_main_button = Button(
                text='Go to Main Screen',
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'center_y': 0.3}
            )
            go_to_main_button.bind(on_release=self.transition_to_main_screen)

            # Add the button to the layout
            self.ids.layout.add_widget(go_to_main_button)

    def update_label(self, text):
        # Split the text by new lines and filter out empty lines
        lines = [line for line in text.strip().split('\n') if line.strip()]
        # Get the last non-empty line if there is any
        if lines:
            last_non_empty_line = lines[-1]
            self.ids.status_label.text = last_non_empty_line

