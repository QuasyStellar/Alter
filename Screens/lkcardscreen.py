import datetime
import os

from cairosvg import svg2png
from kivy.clock import Clock
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class LKCard(Screen):
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

    def show_document(self):
        try:
            dialog = None
            lay = RelativeLayout()
            scrollview = ScrollView(size_hint=(.8, None))
            scrollview.height = 500
            lay.size_hint_y = None
            ima = Image(
                source='document.png',
            )
            ima.size_hint_y = None
            ima.reload()
            but = MDRaisedButton(
                text="Выйти",
                on_release=lambda _: self.dialog.dismiss(),
                size_hint=(None, None),
                theme_text_color='Custom',
                line_width=3,
                line_color=get_color_from_hex('#2E4547'),
                text_color=get_color_from_hex('#D4F5EC'),
                md_bg_color=get_color_from_hex('#51857A')
            )
            ima.height = ima.texture_size[1]
            lay.height = ima.height
            but.height = 300
            but.width = 300
            lay.add_widget(ima)
            scrollview.add_widget(lay)
            self.dialog = MDDialog(
                type='custom',
                content_cls=scrollview,
                size_hint_x=.5,
                elevation=0,
                buttons=[
                    but,
                ]
            )
            self.dialog.open()
        except:
            self.manager.current = 'omserrorunk'
            self.manager.get_screen('privview').ids.scrollid.clear_widgets()
            self.manager.get_screen('history').ids.scrollid.clear_widgets()
            self.manager.get_screen('anamn').ids.scrollid.clear_widgets()
            self.manager.get_screen('decrypt').ids.scrollid.clear_widgets()
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()

    def documentview(self, instance):
        try:
            prosmotr = self.s.get(
                f'https://lk.emias.mos.ru/api/2/document?ehrId={self.idus}&documentId={instance.docid}',
                headers={'X-Access-JWT': self.authtoken})
            jspros = prosmotr.json()
            try:
                html = jspros['documentHtml']
                html = html.replace('<span>Отклонение от нормы</span>',
                                    '<span style="color: red">ОТКЛОНЕНИЕ ОТ НОРМЫ</span>')
                html = html.replace('<span>отклонение от нормы</span>',
                                    '<span style="color: red">ОТКЛОНЕНИЕ ОТ НОРМЫ</span>')
                html = html.replace('<span>норма</span>', '<span style="color: green">НОРМА</span>')
                html = html.replace('<span>Норма</span>', '<span style="color: green">НОРМА</span>')
                Html_file = open("document.html", "w", encoding="utf-8")
                Html_file.write(html)
                Html_file.close()
                options = Options()
                options.headless = True
                options.add_argument("--width=1000")
                driver = webdriver.Firefox(options=options)
                driver.get(f'file://{os.path.abspath("document.html")}')
                driver.get_full_page_screenshot_as_file('document.png')
                driver.close()
                self.show_document()
            except:
                self.documentview(instance)
        except:
            self.manager.current = 'omserrorunk'
            self.manager.get_screen('privview').ids.scrollid.clear_widgets()
            self.manager.get_screen('history').ids.scrollid.clear_widgets()
            self.manager.get_screen('anamn').ids.scrollid.clear_widgets()
            self.manager.get_screen('decrypt').ids.scrollid.clear_widgets()
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()

    def historyanamnes(self, instance):
        try:
            anamnes = self.s.get(
                f'https://lk.emias.mos.ru/api/1/documents/inspections?ehrId={self.idus}&shortDateFilter=all_time',
                headers={'X-Access-JWT': self.authtoken})
            jsanam = anamnes.json()
            for i in range(len(jsanam['documents'])):
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                if 'appointmentDate' in jsanam['documents'][i]:
                    date = jsanam['documents'][i]['appointmentDate']
                    if date[0:4] == instance.year:
                        flag = False
                        try:
                            if 'doctorSpecialization' in jsanam['documents'][i] and jsanam['documents'][i][
                                'doctorSpecialization'] != None:
                                doctorspec = MDLabel(
                                    text=f"{jsanam['documents'][i]['doctorSpecialization']}",
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                doctorspec.font_size = 45
                                doctorspec.pos_hint = {'center_x': .55, 'center_y': .8}
                                layout.add_widget(doctorspec)
                        except:
                            if 'title' in jsanam['documents'][i] and jsanam['documents'][i]['title'] != None:
                                title = MDLabel(
                                    text=f"{jsanam['documents'][i]['title']}",
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                title.font_size = 45
                                title.pos_hint = {'center_x': .55, 'center_y': .8}
                                layout.add_widget(title)
                                flag = True
                        if flag == False:
                            if 'title' in jsanam['documents'][i] and jsanam['documents'][i]['title'] != None:
                                title = MDLabel(
                                    text=f"{jsanam['documents'][i]['title']}",
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                title.font_size = 45
                                title.pos_hint = {'center_x': .55, 'center_y': .6}
                                layout.add_widget(title)
                        if 'doctorName' in jsanam['documents'][i] and jsanam['documents'][i]['doctorName'] != None:
                            doctorname = MDLabel(
                                text=f"{jsanam['documents'][i]['doctorName']}",
                                theme_text_color='Custom',
                                text_color='white',
                            )
                            doctorname.font_size = 45
                            doctorname.pos_hint = {'center_x': .55, 'center_y': .4}
                            layout.add_widget(doctorname)
                        if 'appointmentDate' in jsanam['documents'][i] and jsanam['documents'][i][
                            'appointmentDate'] != None:
                            time = datetime.datetime.fromisoformat(jsanam['documents'][i]['appointmentDate'])
                            timelab = MDLabel(
                                text=f'{time.strftime("%a, %d %b %Y")}',
                                theme_text_color='Custom',
                                text_color='white',
                            )
                            timelab.font_size = 35
                            timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                            layout.add_widget(timelab)
                        if 'organisation' in jsanam['documents'][i] and jsanam['documents'][i]['organisation'] != None:
                            address = MDLabel(
                                text=jsanam['documents'][i]['organisation'],
                                theme_text_color='Custom',
                                text_color='white',
                            )
                            address.font_size = 30
                            address.pos_hint = {'center_x': .55, 'center_y': .2}
                            layout.add_widget(address)
                        card.add_widget(layout)
                        card.docid = jsanam["documents"][i]["documentId"]
                        card.bind(on_release=self.documentview)
                        self.manager.get_screen("anamn").ids.scrollid.add_widget(card)
                    self.manager.current = 'anamn'
        except:
            self.manager.current = 'omserrorunk'
            self.manager.get_screen('privview').ids.scrollid.clear_widgets()
            self.manager.get_screen('history').ids.scrollid.clear_widgets()
            self.manager.get_screen('anamn').ids.scrollid.clear_widgets()
            self.manager.get_screen('decrypt').ids.scrollid.clear_widgets()
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()

    def view(self, id):
        try:
            def covidtest(*args):
                covid = self.s.get(
                    f"https://lk.emias.mos.ru/api/1/documents/covid-analyzes?ehrId={self.idus}&shortDateFilter=all_time",
                    headers={'X-Access-JWT': self.authtoken})
                jscov = covid.json()
                for i in range(len(jscov['documents'])):
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout = RelativeLayout()
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    title = MDLabel(
                        text=f"{jscov['documents'][i]['title']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    if len(jscov['documents'][i]['title']) < 88:
                        title.font_size = 40
                    else:
                        title.font_size = 30
                    title.font_name = 'Assets/fonts/roboto.ttf'
                    title.pos_hint = {'center_x': .5, 'center_y': .6}
                    layout.add_widget(title)
                    time = datetime.datetime.fromisoformat(jscov['documents'][i]['date'])
                    timelab = MDLabel(
                        text=f'{time.strftime("%a, %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelab.font_size = 30
                    timelab.font_name = 'Assets/fonts/roboto.ttf'
                    timelab.pos_hint = {'center_x': .5, 'center_y': .2}
                    layout.add_widget(timelab)
                    card.docid = jscov["documents"][i]["documentId"]
                    card.bind(on_release=self.documentview)
                    card.add_widget(layout)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def myanamnes(*args):
                anamnes = self.s.get(
                    f'https://lk.emias.mos.ru/api/1/documents/inspections?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jsanam = anamnes.json()
                filt = []
                for i in range(len(jsanam['documents'])):
                    if 'appointmentDate' in jsanam['documents'][i]:
                        date = jsanam['documents'][i]['appointmentDate']
                        if date[0:4] not in filt:
                            filt.append(date[0:4])
                for i in filt:
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout = RelativeLayout()
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    timelab = MDLabel(
                        text=f'Приемы за {i[0:4]} год.',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelab.font_size = 60
                    timelab.font_name = 'Assets/fonts/roboto.ttf'
                    timelab.pos_hint = {'center_x': .5, 'center_y': .5}
                    layout.add_widget(timelab)
                    card.add_widget(layout)
                    card.bind(on_release=self.historyanamnes)
                    card.year = i[0:4]
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def myanaliz(*args):
                analiz = self.s.get(
                    f'https://lk.emias.mos.ru/api/1/documents/analyzes?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jsanaliz = analiz.json()
                for i in range(len(jsanaliz['documents'])):
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout = RelativeLayout()
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    title = MDLabel(
                        text=f"{jsanaliz['documents'][i]['title']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    title.font_name = 'Assets/fonts/roboto.ttf'
                    if len(jsanaliz['documents'][i]['title']) < 88:
                        title.font_size = 40
                    else:
                        title.font_size = 30
                    title.pos_hint = {'center_x': .5, 'center_y': .6}
                    layout.add_widget(title)
                    time = datetime.datetime.fromisoformat(jsanaliz['documents'][i]['date'])
                    timelab = MDLabel(
                        text=f'{time.strftime("%a, %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelab.font_size = 30
                    timelab.font_name = 'Assets/fonts/roboto.ttf'
                    timelab.pos_hint = {'center_x': .5, 'center_y': .2}
                    layout.add_widget(timelab)
                    card.add_widget(layout)
                    card.docid = jsanaliz['documents'][i]['documentId']
                    card.bind(on_release=self.documentview)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def myldp(*args):
                ldp = self.s.get(
                    f'https://lk.emias.mos.ru/api/1/documents/research?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jsldp = ldp.json()
                for i in range(len(jsldp['documents'])):
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout = RelativeLayout()
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    title = MDLabel(
                        text=f"{jsldp['documents'][i]['title']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    title.font_name = 'Assets/fonts/roboto.ttf'
                    if len(jsldp['documents'][i]['title']) < 88:
                        title.font_size = 40
                    else:
                        title.font_size = 30
                    title.pos_hint = {'center_x': .5, 'center_y': .6}
                    layout.add_widget(title)
                    time = datetime.datetime.fromisoformat(jsldp['documents'][i]['date'])
                    timelab = MDLabel(
                        text=f'{time.strftime("%a, %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelab.font_size = 30
                    timelab.font_name = 'Assets/fonts/roboto.ttf'
                    timelab.pos_hint = {'center_x': .5, 'center_y': .2}
                    layout.add_widget(timelab)
                    doctorname = MDLabel(
                        text=f"{jsldp['documents'][i]['muName']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    doctorname.font_size = 30
                    doctorname.font_name = 'Assets/fonts/roboto.ttf'
                    doctorname.pos_hint = {'center_x': .5, 'center_y': .4}
                    layout.add_widget(doctorname)
                    card.add_widget(layout)
                    card.docid = jsldp['documents'][i]['documentId']
                    card.bind(on_release=self.documentview)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def myboln(*args):
                pass

            def myspravki(*args):
                spravki = self.s.get(
                    f'https://lk.emias.mos.ru/api/1/documents/medical-certificates?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jssp = spravki.json()
                for i in range(len(jssp['certificates095'])):
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout = RelativeLayout()
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    try:
                        title = MDLabel(
                            text=f"{jssp['certificates095'][i]['educationalName']}",
                            theme_text_color='Custom',
                            text_color=get_color_from_hex('#D4F5EC'),
                            halign='center'
                        )
                        title.font_name = 'Assets/fonts/roboto.ttf'
                        if len(jssp['certificates095'][i]['educationalName']) < 88:
                            title.font_size = 40
                        else:
                            title.font_size = 30
                    except:
                        title = MDLabel(
                            text=f"Справка",
                            theme_text_color='Custom',
                            text_color=get_color_from_hex('#D4F5EC'),
                            halign='center'
                        )
                        title.font_size = 40
                    title.font_name = 'Assets/fonts/roboto.ttf'
                    title.pos_hint = {'center_x': .5, 'center_y': .7}
                    layout.add_widget(title)
                    doctorname = MDLabel(
                        text=f"{jssp['certificates095'][i]['medicalEmployeeName']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    doctorname.font_size = 30
                    doctorname.font_name = 'Assets/fonts/roboto.ttf'
                    doctorname.pos_hint = {'center_x': .5, 'center_y': .5}
                    layout.add_widget(doctorname)
                    doctorspec = MDLabel(
                        text=f"{jssp['certificates095'][i]['medicalEmployeeSpeciality']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    doctorspec.font_size = 30
                    doctorspec.font_name = 'Assets/fonts/roboto.ttf'
                    doctorspec.pos_hint = {'center_x': .5, 'center_y': .3}
                    layout.add_widget(doctorspec)
                    mu = MDLabel(
                        text=f"{jssp['certificates095'][i]['muName']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    mu.font_size = 30
                    mu.font_name = 'Assets/fonts/roboto.ttf'
                    mu.pos_hint = {'center_x': .5, 'center_y': .2}
                    layout.add_widget(mu)
                    card.docid = jssp['certificates095'][i]['documentId']
                    card.bind(on_release=self.documentview)
                    card.add_widget(layout)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def mystacionar(*args):
                stacionar = self.s.get(
                    f'https://lk.emias.mos.ru/api/1/documents/epicrisis?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jsstac = stacionar.json()
                for i in range(len(jsstac['documents'])):
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout = RelativeLayout()
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    title = MDLabel(
                        text=f"{jsstac['documents'][i]['organisation']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    if len(jsstac['documents'][i]['organisation']) < 88:
                        title.font_size = 40
                    else:
                        title.font_size = 30
                    title.font_name = 'Assets/fonts/roboto.ttf'
                    title.pos_hint = {'center_x': .5, 'center_y': .6}
                    layout.add_widget(title)
                    time = datetime.datetime.strptime(jsstac['documents'][i]['dischargeDate'], "%Y-%m-%dT%H:%M:%S%z")
                    timelab = MDLabel(
                        text=f'{time.strftime("%a, %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelab.font_size = 30
                    timelab.font_name = 'Assets/fonts/roboto.ttf'
                    timelab.pos_hint = {'center_x': .5, 'center_y': .2}
                    layout.add_widget(timelab)
                    card.add_widget(layout)
                    card.docid = jsstac['documents'][i]['documentId']
                    card.bind(on_release=self.documentview)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def myrecepies(*args):
                recepies = self.s.get(
                    f'https://lk.emias.mos.ru/api/2/receipt?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jsrec = recepies.json()
                for i in range(len(jsrec['receipts'])):
                    layout = RelativeLayout()
                    if jsrec['receipts'][i]['prescriptionStatus'] == 'expired':
                        doctorspec = MDLabel(
                            text=f"Cтатус: Просрочен",
                            theme_text_color='Custom',
                            text_color=get_color_from_hex('#D4F5EC'),
                            halign='center'
                        )
                        doctorspec.font_size = 30
                        doctorspec.font_name = 'Assets/fonts/roboto.ttf'
                        doctorspec.pos_hint = {'center_x': .5, 'center_y': .8}
                        layout.add_widget(doctorspec)
                    else:
                        doctorspec = MDLabel(
                            text=f"Cтатус: Действует",
                            theme_text_color='Custom',
                            text_color=get_color_from_hex('#D4F5EC'),
                            halign='center'
                        )
                        doctorspec.font_size = 30
                        doctorspec.font_name = 'Assets/fonts/roboto.ttf'
                        doctorspec.pos_hint = {'center_x': .5, 'center_y': .8}
                        layout.add_widget(doctorspec)
                    card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                    layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                    title = MDLabel(
                        text=f"{jsrec['receipts'][i]['medicineName']}",
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    if len(jsrec['receipts'][i]['medicineName']) < 88:
                        title.font_size = 40
                    else:
                        title.font_size = 30
                    title.pos_hint = {'center_x': .5, 'center_y': .6}
                    title.font_name = 'Assets/fonts/roboto.ttf'
                    layout.add_widget(title)
                    time = datetime.datetime.fromisoformat(jsrec['receipts'][i]['prescriptionDate'])
                    timelab = MDLabel(
                        text=f'{time.strftime("Выписан %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelab.font_size = 30
                    timelab.font_name = 'Assets/fonts/roboto.ttf'
                    timelab.pos_hint = {'center_x': .5, 'center_y': .4}
                    layout.add_widget(timelab)
                    times = datetime.datetime.fromisoformat(jsrec['receipts'][i]['expirationDate'])
                    timelabs = MDLabel(
                        text=f'{times.strftime("Истечет %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color=get_color_from_hex('#D4F5EC'),
                        halign='center'
                    )
                    timelabs.font_size = 30
                    timelabs.font_name = 'Assets/fonts/roboto.ttf'
                    timelabs.pos_hint = {'center_x': .5, 'center_y': .2}
                    prosmotr = self.s.get(
                        f"https://lk.emias.mos.ru/api/3/receipt/details?ehrId={self.idus}&prescriptionNumber={jsrec['receipts'][i]['prescriptionNumber']}",
                        headers={'X-Access-JWT': self.authtoken})
                    jspros = prosmotr.json()
                    svg_code = jspros['qrCode']
                    svg2png(bytestring=svg_code, output_width=350, output_height=350, write_to='document.png',
                            negate_colors=(1, 1, 1, 1))
                    ima = Image(
                        source='document.png',
                        size_hint=(None, None)
                    )
                    ima.height = 300
                    ima.width = 300
                    ima.pos_hint = {'center_x': .85, 'center_y': .5}
                    ima.reload()
                    layout.add_widget(ima)
                    layout.add_widget(timelabs)
                    card.add_widget(layout)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            def myemergency(*args):
                emergency = self.s.get(
                    f'https://lk.emias.mos.ru/api/1/documents/ambulance?ehrId={self.idus}&shortDateFilter=all_time',
                    headers={'X-Access-JWT': self.authtoken})
                jsemg = emergency.json()
                for i in range(len(jsemg['documents'])):
                    card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                  md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                    layout = RelativeLayout()
                    title = MDLabel(
                        text=f"{jsemg['documents'][i]['diagnosis']}",
                        theme_text_color='Custom',
                        text_color='white',
                    )
                    title.font_size = 45
                    title.pos_hint = {'center_x': .55, 'center_y': .8}
                    layout.add_widget(title)
                    timeclean = jsemg['documents'][i]['callDate']
                    time = datetime.datetime.strptime(timeclean[0:16], "%Y-%m-%dT%H:%M")
                    timelab = MDLabel(
                        text=f'{time.strftime("%a, %d %b %Y")}',
                        theme_text_color='Custom',
                        text_color='white',
                    )
                    timelab.font_size = 35
                    timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                    layout.add_widget(timelab)
                    card.add_widget(layout)
                    card.docid = jsemg['documents'][i]['documentId']
                    card.bind(on_release=self.documentview)
                    self.manager.get_screen("history").ids.scrollid.add_widget(card)
                self.manager.current = 'history'

            if id == 1:
                Clock.schedule_once(covidtest)
            elif id == 3:
                Clock.schedule_once(myanamnes)
            elif id == 4:
                Clock.schedule_once(myanaliz)
            elif id == 5:
                Clock.schedule_once(myldp)
            elif id == 6:
                Clock.schedule_once(myboln)
            elif id == 7:
                Clock.schedule_once(myspravki)
            elif id == 8:
                Clock.schedule_once(mystacionar)
            elif id == 9:
                Clock.schedule_once(myrecepies)
            elif id == 10:
                Clock.schedule_once(myemergency)
        except:
            self.manager.current = 'omserrorunk'
            self.manager.get_screen('privview').ids.scrollid.clear_widgets()
            self.manager.get_screen('history').ids.scrollid.clear_widgets()
            self.manager.get_screen('anamn').ids.scrollid.clear_widgets()
            self.manager.get_screen('decrypt').ids.scrollid.clear_widgets()
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
