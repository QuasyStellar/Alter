from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen, FadeTransition
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
import datetime

class ENTERScreen(Screen):
    dialogs = None
    timer = None
    def on_touch_down(self, touch=None):
        def inactive(*args):
            self.manager.get_screen('oms').ids.policy.text =""
            self.manager.get_screen('oms').day = None
            self.manager.get_screen('oms').year = None
            self.manager.get_screen('oms').month = None
            self.manager.get_screen('oms').manager.current = 'enter'
            self.manager.get_screen('oms').ids.counts.text_color ='white'
            x = ToggleButtonBehavior.get_widgets('x')
            for i in x:
                i.state = 'normal'
            y = ToggleButtonBehavior.get_widgets('y')
            for i in y:
                i.state = 'normal'
            z = ToggleButtonBehavior.get_widgets('z')
            for i in z:
                i.state = 'normal'
            self.manager.get_screen('mos').check(flag=True)
            self.manager.current = 'afk'

        if self.timer is not None:
            self.timer.cancel()
        self.timer = Clock.schedule_once(inactive, 300)
        if touch !=None:
            return super(ENTERScreen, self).on_touch_down(touch)
    def oms(self):
        self.manager.transition = FadeTransition()
        self.manager.current = "oms"

    def mos(self):
        self.manager.transition = FadeTransition()
        self.manager.current = "mos"
        self.manager.get_screen('mos').widths = int(Window.size[0]*0.476)
        self.manager.get_screen('mos').heights = int(Window.size[1]*0.75)
        self.manager.get_screen('mos').check()
    def show_alert_dialog_info(self):
        self.manager.current = 'alert'
    def update(self, *args):
        today = datetime.datetime.now()
        dt = datetime.datetime.today()
        days = str(datetime.datetime.strftime(today, '%d'))
        months = str(datetime.datetime.strftime(today, '%b')).upper()
        time = str(datetime.datetime.now().strftime("%H:%M"))
        week = datetime.datetime.weekday(today)
        if week == 0:
            week = '[color=#D4F5EC]ПН[/color]'
        elif week == 1:
            week = '[color=#D4F5EC]ВТ[/color]'
        elif week == 2:
            week = '[color=#D4F5EC]СР[/color]'
        elif week == 3:
            week = '[color=#D4F5EC]ЧТ[/color]'
        elif week == 4:
            week = '[color=#D4F5EC]ПТ[/color]'
        elif week == 5:
            week = '[color=#D4F5EC]СБ[/color]'
        elif week == 6:
            week = '[color=#D4F5EC]ВС[/color]'
        self.ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('oms').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('oms').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('mos').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('mos').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('alert').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('alert').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('emiasscreen').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('emiasscreen').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('help').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('help').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('mosloged').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('mosloged').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('loged').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('loged').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('omsalert').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('omsalert').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('omserror').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('omserror').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('omserrorunk').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('omserrorunk').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
    pass