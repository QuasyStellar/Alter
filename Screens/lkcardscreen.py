import datetime
import locale
from kivy.uix.image import Image

locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from html2image import Html2Image
from cairosvg import svg2png
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from kivymd.uix.card import MDCard


class LKCard(Screen):
    def show_document(self, hei):
        dialog = None
        box = BoxLayout()
        lay = RelativeLayout()
        scrollview = ScrollView(size_hint=(.8, None))
        scrollview.height = 900
        lay.size_hint_y = None
        ima = Image(
            source='document.png',
        )
        ima.size_hint_y = None
        ima.reload()
        but = MDRaisedButton(
            text="Выйти",
            on_release=lambda _: self.dialog.dismiss(),
            size_hint=(None, None)
        )
        ima.height = hei
        lay.height = ima.height
        but.height = 150
        but.width = 200
        but.font_size = 30
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

    def documentview(self, instance):
        prosmotr = self.s.get(
            f'https://lk.emias.mos.ru/api/2/document?ehrId={self.idus}&documentId={instance.docid}',
            headers={'X-Access-JWT': self.authtoken})
        jspros = prosmotr.json()
        try:
            html = jspros['documentHtml']
        except:
            self.documentview(instance)
        html = html.replace('<span>Отклонение от нормы</span>', '<span style="color: red">ОТКЛОНЕНИЕ ОТ НОРМЫ</span>')
        html = html.replace('<span>отклонение от нормы</span>', '<span style="color: red">ОТКЛОНЕНИЕ ОТ НОРМЫ</span>')
        html = html.replace('<span>норма</span>', '<span style="color: green">НОРМА</span>')
        html = html.replace('<span>Норма</span>', '<span style="color: green">НОРМА</span>')
        hei = html.count('<tr>')*80
        hti = Html2Image()
        hti.screenshot(html_str=html, save_as='document.png', size=(1000, hei))
        self.show_document(hei)

    def historyanamnes(self, instance):
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
                        if 'doctorSpecialization' in jsanam['documents'][i] and jsanam['documents'][i]['doctorSpecialization'] != None:
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
                    if 'appointmentDate' in jsanam['documents'][i] and jsanam['documents'][i]['appointmentDate'] != None:
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

    def view(self, id):
        def covidtest(*args):
            covid = self.s.get(
                f"https://lk.emias.mos.ru/api/1/documents/covid-analyzes?ehrId={self.idus}&shortDateFilter=all_time",
                headers={'X-Access-JWT': self.authtoken})
            jscov = covid.json()
            for i in range(len(jscov['documents'])):
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                title = MDLabel(
                    text=f"{jscov['documents'][i]['title']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                title.font_size = 45
                title.pos_hint = {'center_x': .55, 'center_y': .8}
                layout.add_widget(title)
                time = datetime.datetime.fromisoformat(jscov['documents'][i]['date'])
                timelab = MDLabel(
                    text=f'{time.strftime("%a, %d %b %Y")}',
                    theme_text_color='Custom',
                    text_color='white',
                )
                timelab.font_size = 35
                timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
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
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                timelab = MDLabel(
                    text=f'Приемы за {i[0:4]} год.',
                    theme_text_color='Custom',
                    text_color='white',
                    halign='center'
                )
                timelab.font_size = 60
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
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                title = MDLabel(
                    text=f"{jsanaliz['documents'][i]['title']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                title.font_size = 45
                title.pos_hint = {'center_x': .55, 'center_y': .8}
                layout.add_widget(title)
                time = datetime.datetime.fromisoformat(jsanaliz['documents'][i]['date'])
                timelab = MDLabel(
                    text=f'{time.strftime("%a, %d %b %Y")}',
                    theme_text_color='Custom',
                    text_color='white',
                )
                timelab.font_size = 35
                timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
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
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                title = MDLabel(
                    text=f"{jsldp['documents'][i]['title']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                title.font_size = 45
                title.pos_hint = {'center_x': .55, 'center_y': .8}
                layout.add_widget(title)
                time = datetime.datetime.fromisoformat(jsldp['documents'][i]['date'])
                timelab = MDLabel(
                    text=f'{time.strftime("%a, %d %b %Y")}',
                    theme_text_color='Custom',
                    text_color='white',
                )
                timelab.font_size = 35
                timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                layout.add_widget(timelab)
                doctorname = MDLabel(
                    text=f"{jsldp['documents'][i]['muName']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                doctorname.font_size = 45
                doctorname.pos_hint = {'center_x': .55, 'center_y': .4}
                layout.add_widget(doctorname)
                card.add_widget(layout)
                card.docid = jsldp['documents'][i]['documentId']
                card.bind(on_release=self.documentview)
                self.manager.get_screen("history").ids.scrollid.add_widget(card)
            self.manager.current = 'history'

        def myboln(*args):
            None

        def myspravki(*args):
            spravki = self.s.get(
                f'https://lk.emias.mos.ru/api/1/documents/medical-certificates?ehrId={self.idus}&shortDateFilter=all_time',
                headers={'X-Access-JWT': self.authtoken})
            jssp = spravki.json()
            for i in range(len(jssp['certificates095'])):
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                title = MDLabel(
                    text=f"{jssp['certificates095'][i]['educationalName']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                title.font_size = 45
                title.pos_hint = {'center_x': .55, 'center_y': .8}
                layout.add_widget(title)

                doctorname = MDLabel(
                    text=f"{jssp['certificates095'][i]['medicalEmployeeName']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                doctorname.font_size = 45
                doctorname.pos_hint = {'center_x': .55, 'center_y': .4}
                layout.add_widget(doctorname)
                doctorspec = MDLabel(
                    text=f"{jssp['certificates095'][i]['medicalEmployeeSpeciality']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                doctorspec.font_size = 45
                doctorspec.pos_hint = {'center_x': .55, 'center_y': .6}
                layout.add_widget(doctorspec)
                mu = MDLabel(
                    text=f"{jssp['certificates095'][i]['muName']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                mu.font_size = 45
                mu.pos_hint = {'center_x': .55, 'center_y': .6}
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
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                title = MDLabel(
                    text=f"{jsstac['documents'][i]['organisation']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                title.font_size = 45
                title.pos_hint = {'center_x': .55, 'center_y': .8}
                layout.add_widget(title)
                time = datetime.datetime.strptime(jsstac['documents'][i]['dischargeDate'], "%Y-%m-%dT%H:%M:%S%z")
                timelab = MDLabel(
                    text=f'{time.strftime("%a, %d %b %Y")}',
                    theme_text_color='Custom',
                    text_color='white',
                )
                timelab.font_size = 35
                timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                layout.add_widget(timelab)
                card.add_widget(layout)
                card.docid = jsstac['documents'][i]['documentId']
                card.bind(on_release=self.documentview)
                self.manager.get_screen("history").ids.scrollid.add_widget(card)
            self.manager.current = 'history'

        def myrecepies(*args):
            recepies = self.s.get(f'https://lk.emias.mos.ru/api/2/receipt?ehrId={self.idus}&shortDateFilter=all_time',
                                  headers={'X-Access-JWT': self.authtoken})
            jsrec = recepies.json()
            for i in range(len(jsrec['receipts'])):
                layout = RelativeLayout()
                if jsrec['receipts'][i]['prescriptionStatus'] == 'expired':
                    doctorspec = MDLabel(
                        text=f"Cтатус: Просрочен",
                        theme_text_color='Custom',
                        text_color='white',
                    )
                    doctorspec.font_size = 45
                    doctorspec.pos_hint = {'center_x': .55, 'center_y': .6}
                    layout.add_widget(doctorspec)
                else:
                    doctorspec = MDLabel(
                        text=f"Cтатус: Действует",
                        theme_text_color='Custom',
                        text_color='white',
                    )
                    doctorspec.font_size = 45
                    doctorspec.pos_hint = {'center_x': .55, 'center_y': .6}
                    layout.add_widget(doctorspec)
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                title = MDLabel(
                    text=f"{jsrec['receipts'][i]['medicineName']}",
                    theme_text_color='Custom',
                    text_color='white',
                )
                title.font_size = 45
                title.pos_hint = {'center_x': .55, 'center_y': .8}
                layout.add_widget(title)
                time = datetime.datetime.fromisoformat(jsrec['receipts'][i]['prescriptionDate'])
                timelab = MDLabel(
                    text=f'{time.strftime("Выписан %d %b %Y")}',
                    theme_text_color='Custom',
                    text_color='white',
                )
                timelab.font_size = 35
                timelab.pos_hint = {'center_x': .55, 'center_y': .4}
                layout.add_widget(timelab)
                times = datetime.datetime.fromisoformat(jsrec['receipts'][i]['expirationDate'])
                timelabs = MDLabel(
                    text=f'{times.strftime("Истечет %d %b %Y")}',
                    theme_text_color='Custom',
                    text_color='white',
                )
                timelabs.font_size = 35
                timelabs.pos_hint = {'center_x': .55, 'center_y': .2}
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
