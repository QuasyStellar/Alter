import locale
from Screens.enterscreen import ENTERScreen
from Screens.mosscreen import MOSScreen
from Screens.omsscreen import OMSScreen
from Screens.lkcardscreen import LKCard
from Screens.mosloged import MOSLoged
from Screens.omsloged import OMSLoged
from Screens.privivkiscreen import Privivki
locale.setlocale(locale.LC_ALL, '')
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from os import listdir



Window.size = (2048, 1440)
Window.maximize()
for kv in listdir('Kvfiles'):
    Builder.load_file(f"Kvfiles/{kv}")


class Loading(Screen):
    pass


class Loadingoms(Screen):
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


class PrivivkiView(Screen):
    pass


class AlterApp(MDApp):
    sm = None
    def build(self):
        self.sm = ScreenManager()
        sm = self.sm
        sm.add_widget(ENTERScreen(name="enter"))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(MOSScreen(name="mos"))
        sm.add_widget(OMSLoged(name="loged"))
        sm.add_widget(MOSLoged(name="mosloged"))
        sm.add_widget(Loading(name="load"))
        sm.add_widget(Loadingoms(name="loadoms"))
        sm.add_widget(Zapisi(name='zapisi'))
        sm.add_widget(Perenos(name='perenos'))
        sm.add_widget(Showdate(name=('timetable')))
        sm.add_widget(Prikreplenia(name='prik'))
        sm.add_widget(Napravlenia(name='napr'))
        sm.add_widget(LKCard(name="lkcard"))
        sm.add_widget(History(name='history'))
        sm.add_widget(AnamnesView(name='anamn'))
        sm.add_widget(Privivki(name='priv'))
        sm.add_widget((PrivivkiView(name='privview')))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return sm


if __name__ == '__main__':
    AlterApp().run()
# 5494499745000410 1088989771000020