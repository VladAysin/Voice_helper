from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from ASR.ASR import SpeechToText, getResult, getResultCommand, setCommand, SpeechToTextButton
from kivymd.uix.textfield import MDTextField
import time
import json
from threading import Thread
from kivymd.uix.button import MDIconButton


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
        Test = SpeechToTextButton()
        Test.start()
        while Test.result == '':
            time.sleep(0.5)
        print(Test.result)
        # self.handler.result = setCommand(Test.result)
        # self.handler.text_from_asr = Test.result
        self.handler.idx += 1
        self.handler.add_text_in_list(Test.result)
        self.handler.idx += 1
        self.handler.add_text_in_list(str(setCommand(Test.result)))      


class Screen(BoxLayout):
    def __init__(self):

        super(Screen,self).__init__()
        self.result = ''
        self.text_from_asr = ''
        self.chat = self.ids.chat
        self.idx = 0
        self.hide_text_input = True
        
    
    def textInput(self):
        self.hide_text_input = not self.hide_text_input
        if not self.hide_text_input:
            self.layout = BoxLayout(orientation='horizontal',size_hint_y=.1)
            self.text_field = MDTextField(
                    hint_text="Введите команду", multiline=False
                )
            self.but = MDIconButton(icon="send" )
            self.but.bind(on_press=self.move_data)
            self.layout.add_widget(self.text_field)
            self.layout.add_widget(self.but)


            self.add_widget(self.layout)
        else:
            self.remove_widget(self.layout)

    def move_data(self,btn):
        text = self.text_field.text
        if text:
            self.idx+=1
            self.add_text_in_list(text)
            self.idx+=1
            self.text_field.text = ""
            self.add_text_in_list(setCommand(text))


    def add_text_in_list(self,data):
        align = "left" if self.idx%2 else "right"
        label = MDLabel(
            text = str(data),
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
    
