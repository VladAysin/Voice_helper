from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem


Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
Config.write()


Builder.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),"style.kv"))
                                
                                    

class Screen(BoxLayout):
    def __init__(self):

        super(Screen,self).__init__()

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




class MainApp(MDApp):
    def build(self):
        screen = Screen()

        return screen


if __name__=="__main__":
    MainApp().run()