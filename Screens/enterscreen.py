from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.button import MDFillRoundFlatButton
import locale
locale.setlocale(locale.LC_ALL, '')
import datetime

class ENTERScreen(Screen):
    dialogs = None
    def oms(self):
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "down"
        self.manager.current = "oms"

    def mos(self):
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "up"
        self.manager.current = "mos"

    def show_alert_dialog_info(self):
        if not self.dialogs:
            self.dialogs = MDDialog(
                title="При входе по полису ОМС не доступно: первичный осмотр с использованием AI, анализ медкарты. Доступно: Запись по направлению, запись к врачу, перенос. Чтобы воспользоваться полной версией, войдите через mos.ru",
                md_bg_color=(49/255, 72/255, 73/255),
                shadow_softness=100,
                elevation=0,
                buttons=[
                    MDFillRoundFlatButton(
                        text="    ОК    ",
                        md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                        on_release=lambda _: self.dialogs.dismiss(),
                        font_size=35
                    )
                ],
            )
        self.dialogs.open()

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
        self.ids.days.text = f'[color=#D4F5EC]{days}[/color]'
        self.ids.months.text = f'[color=#D4F5EC]{months}[/color]'
        self.ids.time.text = f'[color=#D4F5EC]{time}[/color]'
        self.ids.week.text = f'[color=#D4F5EC]{week}[/color]'

    pass