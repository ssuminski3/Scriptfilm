from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import webbrowser
from kivy.core.clipboard import Clipboard


# MainScreen class
class FourthScreen(Screen):
    captions = False
    def copy_text(self):
        # Copy text to clipboard
        Clipboard.copy("Act as someone who learn VideoXML. VideoXML is new markup language based of XML that you can use to create videos from text, so here are some tags: data - main tag in all document, head - tag with information about file, in head tag you put tags: lang - with lang attribute where you give a main language of output video, pexel - with key attribute where you put your api key to pexel API, output - with name attribute where you define output video file, horizontal or vertical to define resolution. After head tag you have body tag in this tag you put all content of output video. In body tag you use this tags: googleimg - this tag you use when you talk about specific person or not much popular place, with keyword attribut, for example a sentence is about Lebron James and in keyword you put 'Lebron James', pexelimg (tag) - you use when you talk about something generic, with keyword attribute, for example when you talk about economic you put 'economic' in keyword, pexelvideo (tag) - same as pexellimg just it's ads video and not image with voice. If you want use word with diffrent prounaunce than in main language use for googleimg, pexelimg, pexelvideo lang attribute with correct language.Keywords should be always in english even if default language is diffrent.Here you have example of using VideoXML: <data><head><lang lang='pl'/><pexel key='YOUR_PEXEL_API_KEY'/><output name='Najwyższe Polskie Góry - Tatry'/><horiontal/></head><body><googleimg keyword='europe'>Tatry to pasmo górskie w Europie,</googleimg><googleimg keyword='poland'>, które rozciąga się na granicy Polski i Słowacji.</googleimg><pexelvideo keyword='west'>Są częścią Karpat i obejmują zarówno Tatry Zachodnie,</pexelvideo><pexelvideo keyword='mountain'>jak i Tatry Wysokie.</pexelvideo><pexelvideo keyword='beutiful'> Tatry to region o pięknych</pexelvideo><pexelvideo keyword='landscape'>krajobrazach,</pexelvideo><pexelimg keyword='top of the mountain'>wysokich szczytach</pexelimg><pexelimg keyword='valley'>pięknych dolinach</pexelimg><pexelimg keyword='lake'>i jeziorach,</pexelimg><pexelvideo keyword='tourists'>o czyni je popularnym celem turystycznym.</pexelvideo><pexelvideo keyword='nature'>Są również ważnym obszarem dla zachowania przyrody i ochrony wielu gatunków roślin i zwierząt.</pexelvideo></body></data>Second example:<data><head><lang lang='en'/><pexel key='YOUR_PEXEL_API_KEY/><output name='Gym Workout'/><vertical/></head><body><pexelvideo keyword='workout'>In this video, we'll explore a variety of effective gym workouts</pexelvideo><pexelvideo keyword='strength'>Starting with strength training exercises that help you build muscle</pexelvideo><pexelvideo keyword='weightlifting'>Weightlifting is a great way to increase your overall strength and endurance</pexelvideo><pexelvideo keyword='cardio'>Don't forget the importance of cardio workouts to improve your heart health</pexelvideo><pexelimg keyword='dumbbell exercises'>Dumbbell exercises are versatile and can target multiple muscle groups</pexelimg><pexelimg keyword='squat'>Squats are essential for developing strong legs and glutes</pexelimg><pexelimg keyword='bench press'>The bench press is a classic for building chest and arm strength</pexelimg><pexelvideo keyword='stretching'>And, of course, remember to stretch to prevent injuries and improve flexibility</pexelvideo><pexelvideo keyword='cool down'>After your workout, a proper cool-down is crucial for muscle recovery</pexelvideo><pexelvideo keyword='nutrition'>Nutrition plays a vital role in achieving your fitness goals</pexelvideo><pexelvideo keyword='stay hydrated'>Stay hydrated and fuel your body with the right nutrients</pexelvideo><pexelvideo keyword='motivation'>Stay motivated and committed to your fitness journey</pexelvideo></body></data>In output name, should be exacly same title as in title table with all spaces and upper lettersRemember keywords should be a word that you will use to search for image or video that you want to use to present sentence in tag.Use spaces and upper letters in titles of videos, try not to use special characters and in any case dont use '_'. Answer as short as you can")

    def copy_proposition(self):
        # Copy proposition text to clipboard
        Clipboard.copy("Please generate a VideoXML code for a video about {topic}. The video should provide an engaging exploration of the topic, its history, significance, and any relevant details. Ensure the VideoXML code includes the <data> tag, the <head> section with language and Pexel API key, and the <body> section with content. Finally, summarize the video's title and description in a table format. In english. In no less than 10 tags. Make it {horizontal/vertical}")

    def open_link(self):
        # Open a web link
        webbrowser.open('https://www.pexels.com/api/documentation/')
    def open_chat(self):
        # Open a web link
        webbrowser.open('https://chat.openai.com')
    def on_checkbox_active(self, checkbox, value):
        global captions
        self.captions = value
    def create_video(self, xml):
        self.manager.get_screen('load').full_video = {"video": xml, "caption": self.captions}
        self.manager.current = 'load'

