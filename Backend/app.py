from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from ASR.ASR import SpeechToText, getResult, getResultCommand, setCommand, SpeechToTextButton
import time
import json
from threading import Thread


Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
Config.write()


Builder.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),"style.kv"))
                                
class WaitRecord(Thread):
    def __init__(self,handler):
        Thread.__init__(self)
        self.handler = handler
    def run(self):
        # while not(Record.END):
        #     time.sleep(0.5)
        Test.start()
        while Test.result == '':
            time.sleep(0.5)
        print(Test.result)
        self.handler.result = setCommand(Test.result)
        self.handler.text_from_asr = Test.result                              

class Screen(BoxLayout):
    def __init__(self):

        super(Screen,self).__init__()
        self.result = ''
        self.text_from_asr = ''
        self.chat = self.ids.chat
        for n in range(20):
            self.add_text_in_list(f"test {n}", n)

    def add_text_in_list(self,data,idx):
        align = "left" if idx%2 else "right"
        label = MDLabel(
            text = data,
            halign=align,
            size_hint_y=None,
            height=55)

        self.chat.add_widget(label)
        
    
    def say_hello(self):
        some = WaitRecord(self)
        some.start()



class MainApp(MDApp):
    def build(self):
        screen = Screen()

        return screen


if __name__=="__main__":
    MainApp().run()
    Test = SpeechToTextButton()