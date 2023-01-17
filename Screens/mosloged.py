import datetime
from kivy.uix.screenmanager import Screen

class MOSLoged(Screen):
    def exits(self):
        self.manager.current = "enter"

    pass