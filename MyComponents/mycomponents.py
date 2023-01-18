from kivymd.app import MDApp
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton


class Tab(MDFloatLayout, MDTabsBase):
    pass

class MyToggleButton(MDRaisedButton, MDToggleButton):
    def perenesti(self, *args):
        sm = MDApp.get_running_app().sm
        sm.get_screen('loged').perenesti()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = (29 / 255, 89 / 255, 242 / 255, 1)
        self.background_normal = "grey"

    def on_state(self, widget, value):
        sm = MDApp.get_running_app().sm
        self.btn = MDRaisedButton(text='Записать')
        self.btn.font_size = 30
        self.btn.pos_hint = {'center_x': .65, 'center_y': .1}
        self.btn.size_hint = (.28, .13)
        self.btn.bind(on_release=self.perenesti)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            sm.get_screen('loged').perenosEnd = self.endTime
            sm.get_screen('loged').perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None


class MyToggleButtonNew(MDRaisedButton, MDToggleButton):
    def appointment(self, *args):
        sm = MDApp.get_running_app().sm
        sm.get_screen('loged').appointment()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = (29 / 255, 89 / 255, 242 / 255, 1)
        self.background_normal = "grey"

    def on_state(self, widget, value):
        sm = MDApp.get_running_app().sm
        self.btn = MDRaisedButton(text='Записать')
        self.btn.font_size = 30
        self.btn.pos_hint = {'center_x': .65, 'center_y': .1}
        self.btn.size_hint = (.28, .13)
        self.btn.bind(on_release=self.appointment)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            perenosEnd = self.endTime
            perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None