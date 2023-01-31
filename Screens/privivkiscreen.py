import datetime

from kivy.clock import Clock
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class PrivivkiView(Screen):
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

    pass


class Privivki(Screen):
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

    def prof(self):
        vacin = self.s.get(f"https://lk.emias.mos.ru/api/3/vaccinations?ehrId={self.idus}",
                           headers={'X-Access-JWT': self.authtoken})
        jsvac = vacin.json()
        for i in range(len(jsvac['doneList'])):
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            title = MDLabel(
                text=f"{jsvac['doneList'][i]['infectionList'][0]['infectionName']}",
                theme_text_color='Custom',
                text_color='white',
            )
            title.font_size = 45
            title.pos_hint = {'center_x': .55, 'center_y': .8}
            layout.add_widget(title)
            time = datetime.datetime.fromisoformat(jsvac['doneList'][i]['dateVaccination'])
            timelab = MDLabel(
                text=f'{time.strftime("%a, %d %b %Y")}',
                theme_text_color='Custom',
                text_color='white',
            )
            timelab.font_size = 35
            timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
            age = MDLabel(
                text=f"{jsvac['doneList'][i]['age']}",
                theme_text_color='Custom',
                text_color='white',
            )
            age.font_size = 45
            age.pos_hint = {'center_x': 1.2, 'center_y': .3}
            layout.add_widget(age)
            layout.add_widget(timelab)
            card.add_widget(layout)
            self.manager.get_screen("privview").ids.scrollid.add_widget(card)
        self.manager.current = 'privview'

    def immuno(self):
        vacin = self.s.get(f"https://lk.emias.mos.ru/api/3/vaccinations?ehrId={self.idus}",
                           headers={'X-Access-JWT': self.authtoken})
        jsvac = vacin.json()
        for i in range(len(jsvac['tubList'])):
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            title = MDLabel(
                text=f"{jsvac['tubList'][i]['infectionList'][0]['infectionName']}",
                theme_text_color='Custom',
                text_color='white',
            )
            title.font_size = 45
            title.pos_hint = {'center_x': .55, 'center_y': .8}
            layout.add_widget(title)
            time = datetime.datetime.fromisoformat(jsvac['tubList'][i]['dateVaccination'])
            timelab = MDLabel(
                text=f'{time.strftime("%a, %d %b %Y")}',
                theme_text_color='Custom',
                text_color='white',
            )
            timelab.font_size = 35
            timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
            age = MDLabel(
                text=f"{jsvac['tubList'][i]['age']}",
                theme_text_color='Custom',
                text_color='white',
            )
            age.font_size = 45
            age.pos_hint = {'center_x': 1.2, 'center_y': .3}
            layout.add_widget(age)
            result = MDLabel(
                text=f"{jsvac['tubList'][i]['tubResultList'][0]['reactionKind']}",
                theme_text_color='Custom',
                text_color='white',
            )
            result.font_size = 45
            result.pos_hint = {'center_x': .55, 'center_y': .4}
            layout.add_widget(result)
            layout.add_widget(timelab)
            card.add_widget(layout)
            self.manager.get_screen("privview").ids.scrollid.add_widget(card)
        self.manager.current = 'privview'
