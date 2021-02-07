from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from ASR.ASR import SpeechToText, getResult, getResultCommand, setCommand
import time
import json
from threading import Thread


Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
Config.write()


Builder.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),"style.kv"))
                                
                                    

class Screen(BoxLayout):
    def __init__(self):

        super(Screen,self).__init__()
        self.text_from_asr = ''
        self.chat = self.ids.chat
        print(self.chat)
        for n in range(20):
            # if n%2==0:
            #     aling = "left"
            # else: 
            #     aling = "right"
            align = "left" if n%2 else "right"
            label = MDLabel(
                            text = str(n),
                            font_size="5",
                            halign = align,
                            valign="bottom",
                            markup=True
            )
            self.chat.add_widget(label)
    
    def say_hello(self):
        print("jopa")



class MainApp(MDApp):
    def build(self):
        screen = Screen()

        return screen


if __name__=="__main__":
    MainApp().run()