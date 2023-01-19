from kivy.clock import Clock
from Screens.enterscreen import ENTERScreen
from Screens.mosscreen import MOSScreen, HelpScreen
from Screens.omsscreen import OMSScreen, OMSErrorScreen, OMSErrorUnkScreen
from Screens.lkcardscreen import LKCard
from Screens.mosloged import MOSLoged
from kivy.utils import get_color_from_hex
from Screens.omsloged import OMSLoged, OMSAlertScreen
from Screens.privivkiscreen import Privivki
from Screens.priemscreen import Priem
from Screens.emiasscreen import EmiasScreen
from kivy.uix.scrollview import ScrollView
from Screens.decryptscreen import Decrypt
from kivymd.effects.fadingedge.fadingedge import FadingEdgeEffect
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager as ScreenManager
from kivymd.uix.screen import MDScreen as Screen
from os import listdir
import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
    )


#Window.maximize()
Window.size = (1920, 1080)

for kv in listdir('Kvfiles'):
    Builder.load_file(f"Kvfiles/{kv}")


class Loading(Screen):
    pass

class FadeScrollView(FadingEdgeEffect, ScrollView):
    pass


class Zapisi(Screen):
    pass


class Showdate(Screen):
    def back(self):
        self.manager.current = 'perenos'
        self.ids.lay.clear_widgets()
        try:
            if self.children[0].text == 'Записать':
                self.remove_widget(self.children[0])
                
            else:
                None
        except:
            None


class Perenos(Screen):
    pass

class Napravlenia(Screen):
    pass


class Prikreplenia(Screen):
    pass


class History(Screen):
    pass


class AnamnesView(Screen):
    pass

class AFK(Screen):
    pass 

class PrivivkiView(Screen):
    pass
class Alert(Screen):
    pass

class MyToggleButton(MDFlatButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = get_color_from_hex('#51857A')
        self.font_color_normal =  get_color_from_hex('#D4F5EC')
        self.font_color_down =  get_color_from_hex('#72C3AC')


class AlterApp(MDApp):
    sm = None
    def build(self):
        self.sm = ScreenManager()
        sm = self.sm
        sm.add_widget(AFK(name='afk'))#
        sm.add_widget(OMSErrorScreen(name='omserror'))#
        sm.add_widget(OMSErrorUnkScreen(name='omserrorunk'))#
        sm.add_widget(OMSAlertScreen(name='omsalert'))#
        sm.add_widget(EmiasScreen(name='emiasscreen'))#
        sm.add_widget(Alert(name='alert'))#
        sm.add_widget(HelpScreen(name='help'))#
        sm.add_widget(ENTERScreen(name="enter"))#
        sm.add_widget(OMSScreen(name="oms"))#
        sm.add_widget(MOSScreen(name="mos"))#
        sm.add_widget(OMSLoged(name="loged"))#
        sm.add_widget(MOSLoged(name="mosloged"))#
        sm.add_widget(Loading(name="load"))#
        sm.add_widget(Zapisi(name='zapisi'))#
        sm.add_widget(Perenos(name='perenos'))#
        sm.add_widget(Showdate(name='timetable'))
        sm.add_widget(Prikreplenia(name='prik'))#
        sm.add_widget(Napravlenia(name='napr'))
        sm.add_widget(LKCard(name="lkcard"))
        sm.add_widget(History(name='history'))
        sm.add_widget(AnamnesView(name='anamn'))
        sm.add_widget(Privivki(name='priv'))
        sm.add_widget((PrivivkiView(name='privview')))
        sm.add_widget(Priem(name='priem'))
        sm.add_widget(Decrypt(name='decrypt'))
        Clock.schedule_interval(sm.get_screen('enter').update, 2)
        for i in range(1,32):
            twl = MyToggleButton(halign="center", text=f'{i}', text_color=get_color_from_hex('#D4F5EC'), theme_text_color='Custom', font_style='H4', on_press = sm.get_screen('oms').days, md_bg_color = get_color_from_hex('#32494B'), size_hint = (1, .2), group="x")
            twl.date = i
            sm.get_screen('oms').ids.container1.add_widget(twl)
        months=[
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь'
        ]
        for i in months:
            twl = MyToggleButton(halign="center", text=f'{i}', text_color=get_color_from_hex('#D4F5EC'), theme_text_color='Custom', font_style='H4', on_press = sm.get_screen('oms').months, md_bg_color = get_color_from_hex('#32494B'), size_hint = (1, .2), group="y")
            twl.month = i
            sm.get_screen('oms').ids.container2.add_widget(twl)
        for i in reversed(range(1900, 2024)):
            twl = MyToggleButton(halign="center", text=f'{i}', text_color=get_color_from_hex('#D4F5EC'), theme_text_color='Custom', font_style='H4', on_press = sm.get_screen('oms').years, md_bg_color = get_color_from_hex('#32494B'), size_hint = (1, .2), group="z")
            twl.year = i
            sm.get_screen('oms').ids.container3.add_widget(twl)
        return sm
        

    


        


if __name__ == '__main__':
    AlterApp().run()
# 5494499745000410 1088989771000020
