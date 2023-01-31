from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


class Tab(MDFloatLayout, MDTabsBase):
    pass


class MyToggleButton(MDFlatButton, MDToggleButton):
    def perenesti(self, *args):
        sm = MDApp.get_running_app().sm
        sm.get_screen('loged').perenesti()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = get_color_from_hex('#00E4B6')
        self.font_color_normal = get_color_from_hex('#D4F5EC')
        self.font_color_down = get_color_from_hex('#D4F5EC')

    def on_state(self, widget, value):
        sm = MDApp.get_running_app().sm
        self.btn = MDCard(md_bg_color=(0, 0, 0, 0))
        im = Image(source='Assets/omsloged/zapis.png', center_x=self.parent.center_x, center_y=self.parent.center_y,
            allow_stretch=True, size=self.parent.size, )
        self.btn.add_widget(im)
        self.btn.pos_hint = {'center_x': .5, 'center_y': .1}
        self.btn.size_hint = (.5, .138)
        self.btn.check = True
        self.btn.bind(on_release=self.perenesti)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            sm.get_screen('loged').perenosEnd = self.endTime
            sm.get_screen('loged').perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None


class MyToggleButtonNew(MDFlatButton, MDToggleButton):
    def appointment(self, *args):
        sm = MDApp.get_running_app().sm
        sm.get_screen('loged').appointment()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = get_color_from_hex('#00E4B6')
        self.font_color_normal = get_color_from_hex('#D4F5EC')
        self.font_color_down = get_color_from_hex('#D4F5EC')

    def on_state(self, widget, value):
        sm = MDApp.get_running_app().sm
        self.btn = MDCard(md_bg_color=(0, 0, 0, 0))
        im = Image(source='Assets/omsloged/zapis.png', center_x=self.parent.center_x, center_y=self.parent.center_y,
            allow_stretch=True, size=self.parent.size, )
        self.btn.add_widget(im)
        self.btn.pos_hint = {'center_x': .5, 'center_y': .1}
        self.btn.size_hint = (.5, .138)
        self.btn.check = True
        self.btn.bind(on_release=self.appointment)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            perenosEnd = self.endTime
            perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None
