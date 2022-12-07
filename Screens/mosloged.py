import datetime
import locale
locale.setlocale(locale.LC_ALL, '')
from kivy.uix.screenmanager import Screen

class MOSLoged(Screen):
    def update(self, *args):
        today = datetime.datetime.now()
        dt = datetime.datetime.today()
        days = str(datetime.datetime.strftime(today, '%d'))
        months = str(datetime.datetime.strftime(today, '%B'))
        years = str(datetime.datetime.strftime(today, '%Y'))
        time = str(datetime.datetime.now().strftime("%H:%M"))
        week = datetime.datetime.weekday(today)
        if week == 0:
            week = 'ПН'
        elif week == 1:
            week = 'ВТ'
        elif week == 2:
            week = 'СР'
        elif week == 3:
            week = 'ЧТ'
        elif week == 4:
            week = 'ПТ'
        elif week == 5:
            week = 'СБ'
        elif week == 6:
            week = 'ВС'
        self.ids.days.text = days
        self.ids.months.text = months
        self.ids.years.text = years
        self.ids.time.text = time
        self.ids.week.text = week

    def exits(self):
        self.manager.current = "enter"

    pass