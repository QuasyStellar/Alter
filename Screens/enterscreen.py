import datetime

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import Screen, FadeTransition


class ENTERScreen(Screen):
    dialogs = None
    timer = None

    def on_touch_down(self, touch=None):

        def inactive(*args):
            self.manager.get_screen('oms').ids.policy.text = ""
            self.manager.get_screen('oms').day = None
            self.manager.get_screen('oms').year = None
            self.manager.get_screen('oms').month = None
            self.manager.get_screen('oms').manager.current = 'enter'
            self.manager.get_screen('oms').ids.counts.text_color = 'white'
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            try:
                if self.manager.get_screen('timetable').children[0].check == True:
                    self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            except:
                pass

            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
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

        if self.manager.get_screen('enter').timer is not None:
            self.manager.get_screen('enter').timer.cancel()
        self.manager.get_screen('enter').timer = Clock.schedule_once(inactive, 300)
        if touch != None:
            return super(Screen, self).on_touch_down(touch)

    def oms(self):
        self.manager.transition = FadeTransition()
        self.manager.current = "oms"

    def mos(self):
        self.manager.transition = FadeTransition()
        self.manager.current = "mos"
        self.manager.get_screen('mos').widths = int(Window.size[0] * 0.476)
        self.manager.get_screen('mos').heights = int(Window.size[1] * 0.75)
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
        self.manager.get_screen('perenossucc').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('perenossucc').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('otmenasucc').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('otmenasucc').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('succnew').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('succnew').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('zapisi').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('zapisi').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('perenos').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('perenos').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('timetable').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('timetable').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('prik').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('prik').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('napr').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('napr').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('lkcard').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('lkcard').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('history').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('history').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('anamn').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('anamn').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('priv').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('priv').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('privview').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('privview').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('priem').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('priem').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
        self.manager.get_screen('decrypt').ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.manager.get_screen('decrypt').ids.week.text = f'[color=#D4F5EC]{week}, {days} {months}[/color]'
    pass
