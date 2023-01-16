import datetime
from kivymd.uix.label import MDLabel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard

class Privivki(Screen):
    def prof(self):
        vacin = self.s.get(f"https://lk.emias.mos.ru/api/3/vaccinations?ehrId={self.idus}", headers={'X-Access-JWT': self.authtoken})
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
        vacin = self.s.get(f"https://lk.emias.mos.ru/api/3/vaccinations?ehrId={self.idus}", headers={'X-Access-JWT': self.authtoken})
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