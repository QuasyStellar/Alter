import datetime
from MyComponents.mycomponents import Tab, MyToggleButton, MyToggleButtonNew
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.utils import asynckivy
from kivy.uix.behaviors import ToggleButtonBehavior
import calendar
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.stacklayout import MDStackLayout as StackLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.tab import MDTabs
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
import requests
from kivymd.uix.card import MDCard


class OMSLoged(Screen):
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

    dialogsucc = None
    dialogsuccper = None
    news = None
    types = None

    def screenback(self):
        if self.types == 'oms':
            self.manager.current = 'loged'
        else:
            self.manager.current = 'mosloged'

    def succ(self):
        self.manager.current = 'otmenasucc'

    def succper(self):
        self.manager.current = 'perenossucc'

    def newd(self):
        self.manager.current = 'succ'

    def exits(self):
        self.manager.current = 'enter'

    def prikreplenia(self):
        try:
            inf = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getPatientInfo3',
                                json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE", "method": "getPatientInfo3",
                                      "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                 "typeAttach": [0, 1, 2],
                                                 "onlyMoscowPolicy": False}})
            jsinf = inf.json()
            for i in range(len(jsinf['result']['attachments']['attachment'])):
                layout = RelativeLayout(size_hint=(1, None), height=330)
                layout.add_widget(Image(source='Assets/omsloged/prikbutton.png'))
                name = MDLabel(
                    text=jsinf['result']['attachments']['attachment'][i]['lpu']['name'],
                    text_color=get_color_from_hex('#D4F5EC'),
                    theme_text_color='Custom'
                )
                name.font_name = 'Assets/fonts/roboto.ttf'
                name.font_size = 30
                name.pos_hint = {'center_x': .78, 'center_y': .7}
                layout.add_widget(name)
                address = MDLabel(
                    text=jsinf['result']['attachments']['attachment'][i]['lpu']['address'],
                    text_color=get_color_from_hex('#D4F5EC'),
                    theme_text_color='Custom'
                )
                address.font_name = 'Assets/fonts/roboto.ttf'
                address.font_size = 30
                address.pos_hint = {'center_x': .78, 'center_y': .5}
                layout.add_widget(address)
                time = datetime.datetime.fromisoformat(jsinf['result']['attachments']['attachment'][i]['createDate'])
                create = MDLabel(
                    text=f'{time.strftime("Прикреплено от %d %B %Y")}',
                    text_color=get_color_from_hex('#D4F5EC'),
                    theme_text_color='Custom'
                )
                create.font_name = 'Assets/fonts/roboto.ttf'
                create.font_size = 30
                create.pos_hint = {'center_x': .78, 'center_y': .3}
                layout.add_widget(create)
                self.manager.get_screen('prik').ids.lay.add_widget(layout)
            self.manager.current = 'prik'
        except:
            self.manager.current = 'omserrorunk'
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()

    def zapisi(self):
        try:
            prosmotr = requests.post("https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient",
                                     json={"jsonrpc": "2.0", "id": "tnSZKjovHE_X2b-JYQ0PB",
                                           "method": "getAppointmentReceptionsByPatient",
                                           "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsps = prosmotr.json()
            if len(jsps["result"]) == 0:
                layout = RelativeLayout(size_hint=(1, None), height=200)
                layout.add_widget(Image(source='Assets/omsloged/nozapis.png'))
                self.manager.get_screen("zapisi").ids.scrollid.add_widget(layout)
            else:
                for i in range(len(jsps['result'])):
                    if 'toDoctor' in jsps["result"][i]:
                        card = MDCard(size_hint=(1, None), height=330, md_bg_color=(0, 0, 0, 0))
                        layout = RelativeLayout()
                        layout.add_widget(Image(source='Assets/omsloged/zapisperenos.png', keep_ratio=False))
                        if 'Офтальмолог' in jsps["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                    " ") or 'офтальм' in \
                                jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/eyes.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .6}))
                        elif 'Оториноларинголог' in jsps["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                            " ") or 'оторин ' in \
                                jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/ear.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .6}))
                        elif 'Стоматолог' in jsps["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                     " ") or 'зуб' in \
                                jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " ") or 'стомат' in \
                                jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/tooth.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .6}))
                        elif 'Гастроэнтеролог' in jsps["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                          " ") or 'гастро' in \
                                jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/gastro.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .6}))
                        elif 'справ' in jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(
                                Image(source='Assets/omsloged/docicons/document.png', height=185, width=185,
                                      pos_hint={'center_x': .1, 'center_y': .6}))
                        elif 'ОРВИ' in jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(
                                Image(source='Assets/omsloged/docicons/covid19.png', height=185, width=185,
                                      pos_hint={'center_x': .1, 'center_y': .6}))
                        else:
                            layout.add_widget(
                                Image(source='Assets/omsloged/docicons/docdefault.png', height=185, width=185,
                                      pos_hint={'center_x': .1, 'center_y': .6}))
                        if len(jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " ")) <= 46:
                            specname = MDLabel(
                                text=f'{jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " ")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint_x=.8
                            )
                            specname.font_size = 30
                            specname.font_name = 'Assets/fonts/roboto.ttf'
                            specname.pos_hint = {'center_x': .6, 'center_y': .75}
                            layout.add_widget(specname)
                            time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                            timelab = MDLabel(
                                text=f'{time.strftime("%a, %d %b в %H:%M")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            timelab.font_size = 30
                            timelab.font_name = 'Assets/fonts/roboto.ttf'
                            timelab.pos_hint = {'center_x': 1.2, 'center_y': .45}
                            layout.add_widget(timelab)
                            address = MDLabel(
                                text=f'{jsps["result"][i]["nameLpu"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            address.font_size = 30
                            address.font_name = 'Assets/fonts/roboto.ttf'
                            address.pos_hint = {'center_x': .7, 'center_y': .65}
                            layout.add_widget(address)
                            addressbol = MDLabel(
                                text=f'{jsps["result"][i]["lpuAddress"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            addressbol.font_size = 30
                            addressbol.pos_hint = {'center_x': .7, 'center_y': .55}
                            addressbol.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(addressbol)
                            room = MDLabel(
                                text=f'Каб. {jsps["result"][i]["roomNumber"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            room.font_size = 30
                            room.font_name = 'Assets/fonts/roboto.ttf'
                            room.pos_hint = {'center_x': .7, 'center_y': .45}
                            layout.add_widget(room)
                            otmena = MDFlatButton(
                                text='Отмена',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint=(.4846, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            otmena.zapisid = jsps["result"][i]["id"]
                            otmena.bind(on_release=self.otmenas)
                            otmena.pos_hint = {'center_x': .748, 'center_y': .23}
                            otmena.font_size = 30
                            otmena.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(otmena)
                            perenesti = MDFlatButton(
                                text="Перенести",
                                theme_text_color='Custom',
                                text_color='white',
                                size_hint=(.49, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            perenesti.pos_hint = {'center_x': .253, 'center_y': .23}
                            perenesti.font_size = 30
                            perenesti.font_name = 'Assets/fonts/roboto.ttf'
                            perenesti.bind(on_release=self.perenoss)
                            perenesti.zapisid = i
                            try:
                                perenesti.refferal = jsps["result"][i]['referral']['referralId']
                            except:
                                pass
                            layout.add_widget(perenesti)
                            card.add_widget(layout)
                            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
                        else:
                            specname = MDLabel(
                                text=f'{jsps["result"][i]["toDoctor"]["specialityName"].replace("_", " ")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint_x=.8
                            )
                            specname.font_size = 30
                            specname.font_name = 'Assets/fonts/roboto.ttf'
                            specname.pos_hint = {'center_x': .6, 'center_y': .75}
                            layout.add_widget(specname)
                            time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                            timelab = MDLabel(
                                text=f'{time.strftime("%a, %d %b в %H:%M")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            timelab.font_size = 30
                            timelab.font_name = 'Assets/fonts/roboto.ttf'
                            timelab.pos_hint = {'center_x': 1.2, 'center_y': .38}
                            layout.add_widget(timelab)
                            address = MDLabel(
                                text=f'{jsps["result"][i]["nameLpu"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            address.font_size = 30
                            address.font_name = 'Assets/fonts/roboto.ttf'
                            address.pos_hint = {'center_x': .7, 'center_y': .58}
                            layout.add_widget(address)
                            addressbol = MDLabel(
                                text=f'{jsps["result"][i]["lpuAddress"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            addressbol.font_size = 30
                            addressbol.pos_hint = {'center_x': .7, 'center_y': .48}
                            addressbol.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(addressbol)
                            room = MDLabel(
                                text=f'Каб. {jsps["result"][i]["roomNumber"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            room.font_size = 30
                            room.font_name = 'Assets/fonts/roboto.ttf'
                            room.pos_hint = {'center_x': .7, 'center_y': .38}
                            layout.add_widget(room)
                            otmena = MDFlatButton(
                                text='Отмена',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint=(.4846, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            otmena.zapisid = jsps["result"][i]["id"]
                            otmena.bind(on_release=self.otmenas)
                            otmena.pos_hint = {'center_x': .748, 'center_y': .23}
                            otmena.font_size = 30
                            otmena.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(otmena)
                            perenesti = MDFlatButton(
                                text="Перенести",
                                theme_text_color='Custom',
                                text_color='white',
                                size_hint=(.49, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            perenesti.pos_hint = {'center_x': .253, 'center_y': .23}
                            perenesti.font_size = 30
                            perenesti.font_name = 'Assets/fonts/roboto.ttf'
                            perenesti.bind(on_release=self.perenoss)
                            perenesti.zapisid = i
                            try:
                                perenesti.refferal = jsps["result"][i]['referral']['referralId']
                            except:
                                pass
                            layout.add_widget(perenesti)
                            card.add_widget(layout)
                            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
                    else:
                        card = MDCard(size_hint=(1, None), height=330, md_bg_color=(0, 0, 0, 0))
                        layout = RelativeLayout()
                        layout.add_widget(Image(source='Assets/omsloged/zapisperenos.png', keep_ratio=False))
                        layout.add_widget(Image(source='Assets/omsloged/docicons/ldp.png', height=185, width=185,
                                                pos_hint={'center_x': .1, 'center_y': .6}))
                        if len(jsps["result"][i]["toLdp"]["ldpTypeName"])<=46:
                            specname = MDLabel(
                                text=jsps["result"][i]["toLdp"]["ldpTypeName"],
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            specname.font_size = 30
                            specname.font_name = 'Assets/fonts/roboto.ttf'
                            specname.pos_hint = {'center_x': .7, 'center_y': .75}
                            layout.add_widget(specname)
                            time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                            timelab = MDLabel(
                                text=f'{time.strftime("%a, %d %b в %H:%M")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            timelab.font_size = 30
                            timelab.font_name = 'Assets/fonts/roboto.ttf'
                            timelab.pos_hint = {'center_x': 1.2, 'center_y': .45}
                            layout.add_widget(timelab)
                            address = MDLabel(
                                text=f'{jsps["result"][i]["nameLpu"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            address.font_size = 30
                            address.font_name = 'Assets/fonts/roboto.ttf'
                            address.pos_hint = {'center_x': .7, 'center_y': .65}
                            layout.add_widget(address)
                            addressbol = MDLabel(
                                text=f'{jsps["result"][i]["lpuAddress"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            addressbol.font_size = 30
                            addressbol.pos_hint = {'center_x': .7, 'center_y': .55}
                            addressbol.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(addressbol)
                            room = MDLabel(
                                text=f'Каб. {jsps["result"][i]["roomNumber"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            room.font_size = 30
                            room.font_name = 'Assets/fonts/roboto.ttf'
                            room.pos_hint = {'center_x': .7, 'center_y': .45}
                            layout.add_widget(room)
                            otmena = MDFlatButton(
                                text='Отмена',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint=(.4846, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            otmena.zapisid = jsps["result"][i]["id"]
                            otmena.bind(on_release=self.otmenas)
                            otmena.pos_hint = {'center_x': .748, 'center_y': .23}
                            otmena.font_size = 30
                            otmena.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(otmena)
                            perenesti = MDFlatButton(
                                text="Перенести",
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint=(.49, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            perenesti.pos_hint = {'center_x': .253, 'center_y': .23}
                            perenesti.font_size = 30
                            perenesti.font_name = 'Assets/fonts/roboto.ttf'
                            perenesti.bind(on_release=self.perenoss)
                            perenesti.zapisid = i
                            perenesti.refferal = jsps["result"][i]['referral']['referralId']
                            layout.add_widget(perenesti)
                            card.add_widget(layout)
                            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
                        else:
                            specname = MDLabel(
                                text=jsps["result"][i]["toLdp"]["ldpTypeName"],
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            specname.font_size = 30
                            specname.font_name = 'Assets/fonts/roboto.ttf'
                            specname.pos_hint = {'center_x': .7, 'center_y': .75}
                            layout.add_widget(specname)
                            time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                            timelab = MDLabel(
                                text=f'{time.strftime("%a, %d %b в %H:%M")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            timelab.font_size = 30
                            timelab.font_name = 'Assets/fonts/roboto.ttf'
                            timelab.pos_hint = {'center_x': 1.2, 'center_y': .38}
                            layout.add_widget(timelab)
                            address = MDLabel(
                                text=f'{jsps["result"][i]["nameLpu"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            address.font_size = 30
                            address.font_name = 'Assets/fonts/roboto.ttf'
                            address.pos_hint = {'center_x': .7, 'center_y': .58}
                            layout.add_widget(address)
                            addressbol = MDLabel(
                                text=f'{jsps["result"][i]["lpuAddress"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            addressbol.font_size = 30
                            addressbol.pos_hint = {'center_x': .7, 'center_y': .48}
                            addressbol.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(addressbol)
                            room = MDLabel(
                                text=f'Каб. {jsps["result"][i]["roomNumber"]}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            room.font_size = 30
                            room.font_name = 'Assets/fonts/roboto.ttf'
                            room.pos_hint = {'center_x': .7, 'center_y': .38}
                            layout.add_widget(room)
                            otmena = MDFlatButton(
                                text='Отмена',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint=(.4846, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            otmena.zapisid = jsps["result"][i]["id"]
                            otmena.bind(on_release=self.otmenas)
                            otmena.pos_hint = {'center_x': .748, 'center_y': .23}
                            otmena.font_size = 30
                            otmena.font_name = 'Assets/fonts/roboto.ttf'
                            layout.add_widget(otmena)
                            perenesti = MDFlatButton(
                                text="Перенести",
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint=(.49, .17),
                                md_bg_color=(0, 0, 0, 0)
                            )
                            perenesti.pos_hint = {'center_x': .253, 'center_y': .23}
                            perenesti.font_size = 30
                            perenesti.font_name = 'Assets/fonts/roboto.ttf'
                            perenesti.bind(on_release=self.perenoss)
                            perenesti.zapisid = i
                            perenesti.refferal = jsps["result"][i]['referral']['referralId']
                            layout.add_widget(perenesti)
                            card.add_widget(layout)
                            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
            self.manager.get_screen('zapisi').ids.backgr.source = 'Assets/omsloged/bg/myzapisi.png'
            self.manager.get_screen('zapisi').ids.backgr.reload()
            self.manager.current = 'zapisi'
            self.manager.get_screen('perenos').precurrent = 'zapisi'
        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def otmenas(self, instance):
        try:
            otmenas = requests.post("https://emias.info/api/emc/appointment-eip/v1/?cancelAppointment",
                                    json={"jsonrpc": "2.0", "id": "lXe4h6pwr3IF-xCqBnESK",
                                          "method": "cancelAppointment",
                                          "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                     "appointmentId": instance.zapisid}})
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets_widgets()
            self.succ()
            self.manager.get_screen('loged').zapisi()
        except:
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def perenoss(self, instance):
        try:
            c = 0
            spisokzapisei = requests.post(
                "https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient",
                json={"jsonrpc": "2.0", "id": "H0XYtGjt9CtPQqfGt7NYp",
                      "method": "getAppointmentReceptionsByPatient",
                      "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspisok = spisokzapisei.json()
            zapisvibor = instance.zapisid
            if 'toDoctor' in jsspisok['result'][zapisvibor]:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
                self.recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                              json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                    "method": "getDoctorsInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                               "appointmentId": self.appID,
                                                               "specialityId": self.specID}})
                jsvrachi = spisokvrachei.json()
                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c += 1
                if c == 0:
                    layout = RelativeLayout(size_hint=(1, None), height=200)
                    layout.add_widget(Image(source='Assets/omsloged/unableperenos.png'))
                    self.manager.get_screen("perenos").ids.scrollid.add_widget(layout)
                else:
                    for i in range(len(jsvrachi["result"])):
                        for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                                layout = RelativeLayout()
                                layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                                if 'Офтальмолог' in jsvrachi['result'][i]["name"].replace("_", " ") or 'офтальм' in \
                                        jsvrachi['result'][i]["name"].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/eyes.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'Оториноларинголог' in jsvrachi['result'][i]["name"].replace("_",
                                                                                                  " ") or 'оторин ' in \
                                        jsvrachi['result'][i]["name"].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/ear.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'Стоматолог' in jsvrachi['result'][i]["name"].replace("_", " ") or 'зуб' in \
                                        jsvrachi['result'][i]["name"].replace("_", " ") or 'стомат' in \
                                        jsvrachi['result'][i]["name"].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/tooth.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'Гастроэнтеролог' in jsvrachi['result'][i]["name"].replace("_", " ") or 'гастро' in \
                                        jsvrachi['result'][i]["name"].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/gastro.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'справ' in jsvrachi['result'][i]["name"].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/document.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'ОРВИ' in jsvrachi['result'][i]["name"].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/covid19.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                else:
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/docdefault.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                if len(jsvrachi["result"][i]['name'].replace("_", " "))<=46:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .28}
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    address.pos_hint = {'center_x': .7, 'center_y': .58}
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .43}
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .28}
                                    layout.add_widget(cab)
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.bind(on_release=self.showdateandtime)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
                                else:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .20}
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    address.pos_hint = {'center_x': .7, 'center_y': .50}
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .35}
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .20}
                                    layout.add_widget(cab)
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.bind(on_release=self.showdateandtime)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            else:                       
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
                self.refferal = instance.refferal
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                              json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                    "method": "getDoctorsInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                               "appointmentId": self.appID}})
                jsvrachi = spisokvrachei.json()
                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c += 1
                if c == 0:
                    layout = RelativeLayout(size_hint=(1, None), height=200)
                    layout.add_widget(Image(source='Assets/omsloged/unableperenos.png'))
                    self.manager.get_screen("perenos").ids.scrollid.add_widget(layout)
                else:
                    for i in range(len(jsvrachi["result"])):
                        for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                                layout = RelativeLayout()
                                layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/ldp.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .5}))
                                if len(jsvrachi["result"][i]['name'].replace("_", " "))<=46:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .28}
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .28}
                                    layout.add_widget(cab)
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.pos_hint = {'center_x': .7, 'center_y': .58}
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .43}
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.bind(on_release=self.showdateandtime)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
                                else:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .20}
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .20}
                                    layout.add_widget(cab)
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.pos_hint = {'center_x': .7, 'center_y': .50}
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .35}
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.bind(on_release=self.showdateandtime)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            self.manager.current = 'perenos'
        except Exception as ex:
            print(ex)
            self.manager.current = 'omserrorunk'
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()

    def showdateandtime(self, instance):
        try:
            vrachchoose = instance.vrachnum
            zapisvibor = instance.zapisvibor
            spisokzapisei = requests.post(
                "https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient",
                json={"jsonrpc": "2.0", "id": "H0XYtGjt9CtPQqfGt7NYp",
                      "method": "getAppointmentReceptionsByPatient",
                      "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspisok = spisokzapisei.json()
            if 'toDoctor' in jsspisok["result"][zapisvibor]:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
                self.recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                              json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                    "method": "getDoctorsInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                               "appointmentId": self.appID,
                                                               "specialityId": self.specID}})
                jsvrachi = spisokvrachei.json()
                self.resID = jsvrachi["result"][vrachchoose]["id"]
                for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                    if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                        self.complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
                dati = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo',
                                     json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE",
                                           "method": "getAvailableResourceScheduleInfo",
                                           "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                      "availableResourceId": self.resID,
                                                      "complexResourceId": self.complID,
                                                      "appointmentId": self.appID, "specialityId": self.specID}})
                jsproczapis = dati.json()
                tabs = MDTabs(
                    radius=[10, 10, 0, 0],
                    allow_stretch=True,
                    background_color=get_color_from_hex('51857A'),
                    tab_hint_x=True,
                    tab_bar_height='90'
                )
                for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
                    tab = Tab(
                        title=time.strftime("%d\n%a")
                    )
                    tab.tab_label.font_size = '40sp'
                    scrolllayout = ScrollView(
                        size_hint=(.8, 1),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    scrolllayout.pos_hint = {'center_x': .57, 'center_y': .45}
                    layout = StackLayout(adaptive_height=True)
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButtonNew(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            group="x",
                            text_color=get_color_from_hex('#D4F5EC'),
                            md_bg_color=get_color_from_hex('#51857A'),
                        )
                        times.font_size = 60
                        times.size_hint_y = None
                        times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'endTime']
                        times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'startTime']
                        layout.add_widget(times)
                    layout.height = layout.minimum_height
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            else:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                              json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                    "method": "getDoctorsInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                               "appointmentId": self.appID}})
                jsvrachi = spisokvrachei.json()
                self.resID = jsvrachi["result"][vrachchoose]["id"]
                for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                    if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                        self.complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
                dati = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo',
                                     json={"jsonrpc": "2.0", "id": "ztx3sCBcVymGJdTnTxHTo",
                                           "method": "getAvailableResourceScheduleInfo", "params":
                                               {"omsNumber": self.oms, "birthDate": self.bdates,
                                                "availableResourceId": self.resID, "complexResourceId": self.complID,
                                                "appointmentId": self.appID, "referralId": self.refferal}})

                jsproczapis = dati.json()
                tabs = MDTabs(
                    radius=[10, 10, 0, 0],
                    allow_stretch=True,
                    background_color=get_color_from_hex('51857A'),
                    tab_hint_x=True,
                    tab_bar_height='90'
                )
                for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
                    tab = Tab(
                        title=time.strftime("%d\n%a")
                    )
                    tab.tab_label.font_size = '40sp'
                    scrolllayout = ScrollView(
                        size_hint=(.8, 1),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    scrolllayout.pos_hint = {'center_x': .57, 'center_y': .45}
                    layout = StackLayout(adaptive_height=True)
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButtonNew(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            group="x",
                            text_color=get_color_from_hex('#D4F5EC'),
                            md_bg_color=get_color_from_hex('#51857A'),
                        )
                        times.font_size = 60
                        times.size_hint_y = None
                        times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'endTime']
                        times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'startTime']
                        layout.add_widget(times)
                    layout.height = layout.minimum_height
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            self.manager.current = 'timetable'
        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def appointment(self):
        try:
            appocreate = requests.post("https://emias.info/api/emc/appointment-eip/v1/?createAppointment",
                                       json={"jsonrpc": "2.0", "id": "AvyJzHk1dm8eNqyg5uzLx",
                                             "method": "createAppointment",
                                             "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                        "availableResourceId": self.resID,
                                                        "complexResourceId": self.complID,
                                                        "receptionTypeId": self.recpID,
                                                        "startTime": self.perenosStart, "endTime": self.perenosEnd}})
            jscheck = appocreate.json()
            if "error" not in jscheck:
                self.newd()
                self.manager.get_screen('zapisi').ids.scrollid.clear_widgets_widgets()
                self.manager.get_screen('perenos').ids.scrollid.clear_widgets_widgets()
                self.manager.get_screen('timetable').ids.lay.clear_widgets_widgets()
                if self.manager.get_screen('timetable').children[0].check == True:
                    self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
                self.manager.get_screen('loged').zapisi()
            else:
                self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
                self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
                self.manager.get_screen('timetable').ids.lay.clear_widgets()
                if self.manager.get_screen('timetable').children[0].check == True:
                    self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
                self.manager.get_screen('prik').ids.lay.clear_widgets()
                self.manager.get_screen('napr').ids.scrollid.clear_widgets()
                self.manager.current = 'omserrorunk'
        except:
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            if self.manager.get_screen('timetable').children[0].check == True:
                self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def perenesti(self):
        try:
            perenes = requests.post("https://emias.info/api/emc/appointment-eip/v1/?shiftAppointment",
                                    json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB", "method": "shiftAppointment",
                                          "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                     "appointmentId": self.appID,
                                                     "availableResourceId": self.resID,
                                                     "complexResourceId": self.complID,
                                                     "receptionTypeId": self.recpID, "startTime": self.perenosStart,
                                                     "endTime": self.perenosEnd}})
            jscheck = perenes.json()
            if "error" not in jscheck:
                self.succper()
                self.manager.get_screen('zapisi').ids.scrollid.clear_widgets_widgets()
                self.manager.get_screen('perenos').ids.scrollid.clear_widgets_widgets()
                self.manager.get_screen('timetable').ids.lay.clear_widgets_widgets()
                if self.manager.get_screen('timetable').children[0].check == True:
                    self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
                self.manager.get_screen('loged').zapisi()
            else:
                self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
                self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
                self.manager.get_screen('timetable').ids.lay.clear_widgets()
                if self.manager.get_screen('timetable').children[0].check == True:
                    self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
                self.manager.get_screen('prik').ids.lay.clear_widgets()
                self.manager.get_screen('napr').ids.scrollid.clear_widgets()
                self.manager.current = 'omserrorunk'
        except:
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            if self.manager.get_screen('timetable').children[0].check == True:
                self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def prosmotrnapr(self):
        try:
            prosmotrnaprs = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getReferralsInfo',
                                          json={"jsonrpc": "2.0", "id": "6Ov41JqE7a1bQ3i98ofeF",
                                                "method": "getReferralsInfo",
                                                "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsnp = prosmotrnaprs.json()
            if len(jsnp["result"]) == 0:
                layout = RelativeLayout(size_hint=(1, None), height=200)
                layout.add_widget(Image(source='Assets/omsloged/nonapr.png'))
                self.manager.get_screen("napr").ids.scrollid.add_widget(layout)
            else:
                for i in range(len(jsnp["result"])):
                    if 'toDoctor' in jsnp['result'][i]:
                        card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                        layout = RelativeLayout()
                        layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                        if 'Офтальмолог' in jsnp["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                    " ") or 'офтальм' in \
                                jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/eyes.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .5}))
                        elif 'Оториноларинголог' in jsnp["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                            " ") or 'оторин ' in \
                                jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/ear.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .5}))
                        elif 'Стоматолог' in jsnp["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                     " ") or 'зуб' in \
                                jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " ") or 'стомат' in \
                                jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/tooth.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .5}))
                        elif 'Гастроэнтеролог' in jsnp["result"][i]["toDoctor"]["specialityName"].replace("_",
                                                                                                          " ") or 'гастро' in \
                                jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(Image(source='Assets/omsloged/docicons/gastro.png', height=185, width=185,
                                                    pos_hint={'center_x': .1, 'center_y': .5}))
                        elif 'справ' in jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(
                                Image(source='Assets/omsloged/docicons/document.png', height=185, width=185,
                                      pos_hint={'center_x': .1, 'center_y': .5}))
                        elif 'ОРВИ' in jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "):
                            layout.add_widget(
                                Image(source='Assets/omsloged/docicons/covid19.png', height=185, width=185,
                                      pos_hint={'center_x': .1, 'center_y': .5}))
                        else:
                            layout.add_widget(
                                Image(source='Assets/omsloged/docicons/docdefault.png', height=185, width=185,
                                      pos_hint={'center_x': .1, 'center_y': .5}))
                        if len(jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " ")) <= 46:
                            name = MDLabel(
                                text=jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "),
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint_x=.8
                            )
                            name.font_size = 30
                            name.font_name = 'Assets/fonts/roboto.ttf'
                            name.pos_hint = {'center_x': .6, 'center_y': .73}
                            layout.add_widget(name)
                            time = datetime.datetime.fromisoformat(jsnp["result"][i]["startTime"])
                            avail = MDLabel(
                                text=f'{time.strftime("Доступно с %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            avail.font_size = 30
                            avail.font_name = 'Assets/fonts/roboto.ttf'
                            avail.pos_hint = {'center_x': .7, 'center_y': .58}
                            layout.add_widget(avail)
                            endtime = datetime.datetime.fromisoformat(jsnp["result"][i]["endTime"])
                            end = MDLabel(
                                text=f'{endtime.strftime("До %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            end.font_name = 'Assets/fonts/roboto.ttf'
                            end.font_size = 30
                            end.pos_hint = {'center_x': .7, 'center_y': .43}
                            last = MDLabel(
                                text=f'Осталось {(endtime - datetime.datetime.now()).days + 1} дня',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            last.font_name = 'Assets/fonts/roboto.ttf'
                            last.font_size = 30
                            last.pos_hint = {'center_x': .7, 'center_y': .28}
                            layout.add_widget(last)
                            layout.add_widget(end)
                            card.add_widget(layout)
                            card.zapisid = i
                            card.refferal = jsnp["result"][i]['id']
                            card.specID = jsnp["result"][i]["toDoctor"]['specialityId']
                            card.doctor = True
                            card.bind(on_release=self.naprav)
                            self.manager.get_screen("napr").ids.scrollid.add_widget(card)
                        else:
                            name = MDLabel(
                                text=jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "),
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint_x=.8
                            )
                            name.font_size = 30
                            name.font_name = 'Assets/fonts/roboto.ttf'
                            name.pos_hint = {'center_x': .6, 'center_y': .73}
                            layout.add_widget(name)
                            time = datetime.datetime.fromisoformat(jsnp["result"][i]["startTime"])
                            avail = MDLabel(
                                text=f'{time.strftime("Доступно с %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            avail.font_size = 30
                            avail.font_name = 'Assets/fonts/roboto.ttf'
                            avail.pos_hint = {'center_x': .7, 'center_y': .50}
                            layout.add_widget(avail)
                            endtime = datetime.datetime.fromisoformat(jsnp["result"][i]["endTime"])
                            end = MDLabel(
                                text=f'{endtime.strftime("До %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            end.font_name = 'Assets/fonts/roboto.ttf'
                            end.font_size = 30
                            end.pos_hint = {'center_x': .7, 'center_y': .35}
                            last = MDLabel(
                                text=f'Осталось {(endtime - datetime.datetime.now()).days + 1} дня',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            last.font_name = 'Assets/fonts/roboto.ttf'
                            last.font_size = 30
                            last.pos_hint = {'center_x': .7, 'center_y': .20}
                            layout.add_widget(last)
                            layout.add_widget(end)
                            card.add_widget(layout)
                            card.zapisid = i
                            card.refferal = jsnp["result"][i]['id']
                            card.specID = jsnp["result"][i]["toDoctor"]['specialityId']
                            card.doctor = True
                            card.bind(on_release=self.naprav)
                            self.manager.get_screen("napr").ids.scrollid.add_widget(card)
                    else:
                        card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                        layout = RelativeLayout()
                        layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                        layout.add_widget(Image(source='Assets/omsloged/docicons/ldp.png', height=185, width=185,
                                                pos_hint={'center_x': .1, 'center_y': .5}))
                        if len(jsnp["result"][i]["toLdp"]["ldpTypeName"].replace("_", " ")) <= 46:
                            name = MDLabel(
                                text=jsnp["result"][i]["toLdp"]["ldpTypeName"].replace("_", " "),
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint_x=.8
                            )
                            name.font_size = 30
                            name.font_name = 'Assets/fonts/roboto.ttf'
                            name.pos_hint = {'center_x': .6, 'center_y': .73}
                            layout.add_widget(name)
                            time = datetime.datetime.fromisoformat(jsnp["result"][i]["startTime"])
                            avail = MDLabel(
                                text=f'{time.strftime("Доступно с %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            avail.font_size = 30
                            avail.font_name = 'Assets/fonts/roboto.ttf'
                            avail.pos_hint = {'center_x': .7, 'center_y': .58}
                            layout.add_widget(avail)
                            endtime = datetime.datetime.fromisoformat(jsnp["result"][i]["endTime"])
                            end = MDLabel(
                                text=f'{endtime.strftime("До %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            end.font_size = 30
                            end.font_name = 'Assets/fonts/roboto.ttf'
                            end.pos_hint = {'center_x': .7, 'center_y': .43}
                            layout.add_widget(end)
                            last = MDLabel(
                                text=f'Осталось {(endtime - datetime.datetime.now()).days + 1} дня',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            last.font_name = 'Assets/fonts/roboto.ttf'
                            last.font_size = 30
                            last.pos_hint = {'center_x': .7, 'center_y': .28}
                            layout.add_widget(last)
                            card.zapisid = i
                            card.refferal = jsnp["result"][i]['id']
                            card.recpID = jsnp["result"][i]["toLdp"]['ldpTypeId']
                            card.doctor = False
                            card.add_widget(layout)
                            card.bind(on_release=self.naprav)
                            self.manager.get_screen("napr").ids.scrollid.add_widget(card)
                        else:
                            name = MDLabel(
                                text=jsnp["result"][i]["toLdp"]["ldpTypeName"].replace("_", " "),
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                                size_hint_x=.8
                            )
                            name.font_size = 30
                            name.font_name = 'Assets/fonts/roboto.ttf'
                            name.pos_hint = {'center_x': .6, 'center_y': .73}
                            layout.add_widget(name)
                            time = datetime.datetime.fromisoformat(jsnp["result"][i]["startTime"])
                            avail = MDLabel(
                                text=f'{time.strftime("Доступно с %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            avail.font_size = 30
                            avail.font_name = 'Assets/fonts/roboto.ttf'
                            avail.pos_hint = {'center_x': .7, 'center_y': .50}
                            layout.add_widget(avail)
                            endtime = datetime.datetime.fromisoformat(jsnp["result"][i]["endTime"])
                            end = MDLabel(
                                text=f'{endtime.strftime("До %d %b")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            end.font_size = 30
                            end.font_name = 'Assets/fonts/roboto.ttf'
                            end.pos_hint = {'center_x': .7, 'center_y': .35}
                            layout.add_widget(end)
                            last = MDLabel(
                                text=f'Осталось {(endtime - datetime.datetime.now()).days + 1} дня',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            last.font_name = 'Assets/fonts/roboto.ttf'
                            last.font_size = 30
                            last.pos_hint = {'center_x': .7, 'center_y': .20}
                            layout.add_widget(last)
                            card.zapisid = i
                            card.refferal = jsnp["result"][i]['id']
                            card.recpID = jsnp["result"][i]["toLdp"]['ldpTypeId']
                            card.doctor = False
                            card.add_widget(layout)
                            card.bind(on_release=self.naprav)
                            self.manager.get_screen("napr").ids.scrollid.add_widget(card)
            self.manager.current = 'napr'
            self.manager.get_screen('perenos').precurrent = 'napr'
        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def naprav(self, instance):
        try:
            c = 0
            assignment = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                                       json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                             "method": "getAssignmentsInfo",
                                             "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsass = assignment.json()
            self.userid = jsass["id"]
            specialities = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                                         json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                               "method": "getSpecialitiesInfo",
                                               "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspec = specialities.json()
            if instance.doctor == True:
                zapisvibor = instance.zapisid
                self.refferal = instance.refferal
                self.specID = instance.specID
                zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                      json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                            "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                       "specialityId": self.specID, 'referralId': instance.refferal}})
                jsvrachi = zapis.json()
                self.appID = jsvrachi["result"][zapisvibor]['id']
                self.recpID = jsvrachi["result"][zapisvibor]["receptionType"][0]['code']

                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c += 1
                if c == 0:
                    layout = RelativeLayout(size_hint=(1, None), height=200)
                    layout.add_widget(Image(source='Assets/omsloged/nozapis.png'))
                    self.manager.get_screen("perenos").ids.scrollid.add_widget(layout)
                else:
                    for i in range(len(jsvrachi["result"])):
                        for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                                layout = RelativeLayout()
                                layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                                if 'Офтальмолог' in jsvrachi["result"][i]['name'].replace("_", " ") or 'офтальм' in \
                                        jsvrachi["result"][i]['name'].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/eyes.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'Оториноларинголог' in jsvrachi["result"][i]['name'].replace("_",
                                                                                                  " ") or 'оторин ' in \
                                        jsvrachi["result"][i]['name'].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/ear.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'Стоматолог' in jsvrachi["result"][i]['name'].replace("_", " ") or 'зуб' in \
                                        jsvrachi["result"][i]['name'].replace("_", " ") or 'стомат' in \
                                        jsvrachi["result"][i]['name'].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/tooth.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'Гастроэнтеролог' in jsvrachi["result"][i]['name'].replace("_", " ") or 'гастро' in \
                                        jsvrachi["result"][i]['name'].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/gastro.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'справ' in jsvrachi["result"][i]['name'].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/document.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                elif 'ОРВИ' in jsvrachi["result"][i]['name'].replace("_", " "):
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/covid19.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                else:
                                    layout.add_widget(
                                        Image(source='Assets/omsloged/docicons/docdefault.png', height=185, width=185,
                                              pos_hint={'center_x': .1, 'center_y': .5}))
                                if len(jsvrachi["result"][i]['name'].replace("_", " "))<=46:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .28}
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    address.pos_hint = {'center_x': .7, 'center_y': .58}
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .43}
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .28}
                                    layout.add_widget(cab)
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.resID = jsvrachi["result"][i]['complexResource'][j]['id']
                                    card.doctor = 'Napr'
                                    card.availRES = jsvrachi["result"][i]['id']
                                    card.bind(on_release=self.showdateandtimenew)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
                                else:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .2}
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    address.pos_hint = {'center_x': .7, 'center_y': .5}
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .35}
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .2}
                                    layout.add_widget(cab)
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.resID = jsvrachi["result"][i]['complexResource'][j]['id']
                                    card.doctor = 'Napr'
                                    card.availRES = jsvrachi["result"][i]['id']
                                    card.bind(on_release=self.showdateandtimenew)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            else:
                self.refferal = instance.refferal
                zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                      json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                            "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                       "referralId": instance.refferal}})
                jsspisok = zapis.json()

                zapisvibor = instance.zapisid
                self.appID = jsspisok["result"][zapisvibor]['id']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                              json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                    "method": "getDoctorsInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                               "referralId": self.refferal}})
                jsvrachi = spisokvrachei.json()
                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c += 1
                if c == 0:
                    layout = RelativeLayout(size_hint=(1, None), height=200)
                    layout.add_widget(Image(source='Assets/omsloged/nozapis.png'))
                    self.manager.get_screen("perenos").ids.scrollid.add_widget(layout)
                else:
                    for i in range(len(jsvrachi["result"])):
                        for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                                layout = RelativeLayout()
                                layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/ldp.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .5}))
                                if len(jsvrachi["result"][i]['name'].replace("_", " "))<=46:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .28}
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    address.pos_hint = {'center_x': .7, 'center_y': .58}
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .43}
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .28}
                                    layout.add_widget(cab)
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.resID = jsvrachi["result"][i]['complexResource'][j]['id']
                                    card.availRES = jsvrachi["result"][i]['id']
                                    card.doctor = False
                                    card.bind(on_release=self.showdateandtimenew)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
                                else:
                                    name = MDLabel(
                                        text=jsvrachi["result"][i]['name'].replace("_", " "),
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    name.font_size = 30
                                    name.font_name = 'Assets/fonts/roboto.ttf'
                                    name.pos_hint = {'center_x': .7, 'center_y': .73}
                                    layout.add_widget(name)
                                    time = datetime.datetime.fromisoformat(
                                        jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                    avail = MDLabel(
                                        text=f'{time.strftime("С %d %b, %a")}',
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    avail.font_size = 30
                                    avail.font_name = 'Assets/fonts/roboto.ttf'
                                    avail.pos_hint = {'center_x': 1.3, 'center_y': .2}
                                    layout.add_widget(avail)
                                    address = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    address.font_size = 30
                                    address.font_name = 'Assets/fonts/roboto.ttf'
                                    address.pos_hint = {'center_x': .7, 'center_y': .5}
                                    fulladdress = MDLabel(
                                        text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    fulladdress.font_size = 30
                                    fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                                    fulladdress.pos_hint = {'center_x': .7, 'center_y': .35}
                                    cab = MDLabel(
                                        text=f"Кабинет {jsvrachi['result'][i]['complexResource'][j]['room']['number']}",
                                        theme_text_color='Custom',
                                        text_color=get_color_from_hex('#D4F5EC'),
                                    )
                                    cab.font_size = 30
                                    cab.font_name = 'Assets/fonts/roboto.ttf'
                                    cab.pos_hint = {'center_x': .7, 'center_y': .2}
                                    layout.add_widget(cab)
                                    layout.add_widget(fulladdress)
                                    layout.add_widget(address)
                                    card.vrachnum = i
                                    card.zapisvibor = zapisvibor
                                    card.resID = jsvrachi["result"][i]['complexResource'][j]['id']
                                    card.availRES = jsvrachi["result"][i]['id']
                                    card.doctor = False
                                    card.bind(on_release=self.showdateandtimenew)
                                    card.add_widget(layout)
                                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            self.manager.current = 'perenos'
        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def newzapis(self):
        try:
            specialities = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                                         json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                               "method": "getSpecialitiesInfo",
                                               "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspec = specialities.json()
            for i in range(len(jsspec["result"])):
                choose = MDCard(size_hint=(1, None), height=180, md_bg_color=(0, 0, 0, 0))
                layout = RelativeLayout()
                layout.add_widget(Image(source='Assets/omsloged/newzapisbutton.png'))
                if 'Офтальмолог' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source='Assets/omsloged/docicons/eyes.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))
                elif 'Оториноларинголог' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source='Assets/omsloged/docicons/ear.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))
                elif 'Стоматолог' in jsspec['result'][i]["name"].replace("_", " ") or 'зуб' in jsspec['result'][i][
                    "name"].replace("_", " "):
                    layout.add_widget(Image(source='Assets/omsloged/docicons/tooth.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))
                elif 'Гастроэнтеролог' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source='Assets/omsloged/docicons/gastro.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))
                elif 'справ' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source='Assets/omsloged/docicons/document.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))
                elif 'ОРВИ' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source='Assets/omsloged/docicons/covid19.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))
                else:
                    layout.add_widget(Image(source='Assets/omsloged/docicons/docdefault.png', height=142, width=142,
                                            pos_hint={'center_x': .1, 'center_y': .49}))

                name = MDLabel(
                    text=jsspec['result'][i]["name"].replace("_", " "),
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#D4F5EC'),
                )
                name.font_size = 35
                name.font_name = 'Assets/fonts/roboto.ttf'
                name.pos_hint = {'center_x': .7, 'center_y': .5}
                choose.bind(on_release=self.new)
                choose.zapisid = i
                layout.add_widget(name)
                choose.add_widget(layout)
                self.manager.get_screen("zapisi").ids.scrollid.add_widget(choose)
            self.manager.get_screen('zapisi').ids.backgr.source = 'Assets/omsloged/newzapis.png'
            self.manager.get_screen('zapisi').ids.backgr.reload()
            self.manager.current = 'zapisi'
            self.manager.get_screen('perenos').precurrent = 'zapisi'

        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def new(self, instance):
        try:
            count = 0
            resid = None
            assignment = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                                       json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                             "method": "getAssignmentsInfo",
                                             "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsass = assignment.json()
            self.userid = jsass["id"]
            specialities = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                                         json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                               "method": "getSpecialitiesInfo",
                                               "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspec = specialities.json()
            self.specID = jsspec['result'][instance.zapisid]["code"]
            zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                  json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                        "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                   "specialityId": self.specID}})
            jszapis = zapis.json()
            for i in range(len(jszapis["result"])):
                for j in range(len(jszapis["result"][i]['complexResource'])):
                    if 'room' in jszapis["result"][i]['complexResource'][j]:
                        self.recpID = jszapis["result"][i]['receptionType'][0]['code']
                        count += 1
            if count == 0:
                layout = RelativeLayout(size_hint=(1, None), height=200)
                layout.add_widget(Image(source='Assets/omsloged/unable.png'))
                self.manager.get_screen("perenos").ids.scrollid.add_widget(layout)
            else:
                for i in range(len(jszapis["result"])):
                    for j in range(len(jszapis["result"][i]['complexResource'])):
                        if 'room' in jszapis["result"][i]['complexResource'][j]:
                            choose = MDCard(size_hint=(1, None), height=280, md_bg_color=(0, 0, 0, 0))
                            layout = RelativeLayout()
                            layout.add_widget(Image(source='Assets/omsloged/vrachchoosebutton.png'))
                            if 'Офтальмолог' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/eyes.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))
                            elif 'Оториноларинголог' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/ear.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))
                            elif 'Стоматолог' in jszapis['result'][i]["name"].replace("_", " ") or 'зуб' in \
                                    jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/tooth.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))
                            elif 'Гастроэнтеролог' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/gastro.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))
                            elif 'справ' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/document.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))
                            elif 'ОРВИ' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/covid19.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))
                            else:
                                layout.add_widget(
                                    Image(source='Assets/omsloged/docicons/docdefault.png', height=185, width=185,
                                          pos_hint={'center_x': .1, 'center_y': .49}))

                            name = MDLabel(
                                text=jszapis['result'][i]["name"].replace('_', " "),
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            name.font_size = 30
                            name.font_name = 'Assets/fonts/roboto.ttf'
                            name.pos_hint = {'center_x': .7, 'center_y': .73}
                            time = datetime.datetime.fromisoformat(
                                jszapis["result"][i]['complexResource'][j]['room']['availabilityDate'])
                            avail = MDLabel(
                                text=f'{time.strftime("С %d %b, %a")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            avail.font_name = 'Assets/fonts/roboto.ttf'
                            avail.font_size = 30
                            avail.pos_hint = {'center_x': 1.3, 'center_y': .28}
                            address = MDLabel(
                                text=jszapis["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            address.font_size = 30
                            address.font_name = 'Assets/fonts/roboto.ttf'
                            address.pos_hint = {'center_x': .7, 'center_y': .58}
                            fulladdress = MDLabel(
                                text=jszapis["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            fulladdress.font_size = 30
                            fulladdress.font_name = 'Assets/fonts/roboto.ttf'
                            fulladdress.pos_hint = {'center_x': .7, 'center_y': .43}
                            cab = MDLabel(
                                text=f"Кабинет {jszapis['result'][i]['complexResource'][j]['room']['number']}",
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            cab.font_size = 30
                            cab.font_name = 'Assets/fonts/roboto.ttf'
                            cab.pos_hint = {'center_x': .7, 'center_y': .28}
                            layout.add_widget(cab)
                            layout.add_widget(fulladdress)
                            layout.add_widget(address)
                            layout.add_widget(avail)
                            layout.add_widget(name)
                            choose.resID = jszapis["result"][i]['complexResource'][j]['id']
                            choose.availRES = jszapis["result"][i]['id']
                            choose.doctor = True
                            choose.bind(on_release=self.showdateandtimenew)
                            choose.add_widget(layout)
                            self.manager.get_screen("perenos").ids.scrollid.add_widget(choose)
            self.manager.current = 'perenos'
        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def showdateandtimenew(self, instance):
        try:
            if instance.doctor == True:
                zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                      json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                            "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                       "specialityId": self.specID}})
                jszapis = zapis.json()
                proczapis = requests.post(
                    'https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo',
                    json={"jsonrpc": "2.0", "id": "7g9bgvEa8VkCd6A2XHJ7p",
                          "method": "getAvailableResourceScheduleInfo",
                          "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                     "availableResourceId": instance.availRES,
                                     "complexResourceId": instance.resID,
                                     "specialityId": self.specID}})
                jsproczapis = proczapis.json()
                tabs = MDTabs(
                    radius=[10, 10, 0, 0],
                    allow_stretch=True,
                    background_color=get_color_from_hex('51857A'),
                    tab_hint_x=True,
                    tab_bar_height='90'
                )
                for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
                    tab = Tab(
                        title=time.strftime("%d\n%a"),
                    )
                    tab.tab_label.font_size = '40sp'
                    scrolllayout = ScrollView(
                        size_hint=(.8, 1),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    scrolllayout.pos_hint = {'center_x': .54, 'center_y': .45}
                    layout = StackLayout(adaptive_height=True)
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButtonNew(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            group="x",
                            text_color=get_color_from_hex('#D4F5EC'),
                            md_bg_color=get_color_from_hex('#51857A'),
                        )
                        times.font_size = 60
                        times.size_hint_y = None
                        times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'endTime']
                        times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'startTime']
                        layout.add_widget(times)
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            elif instance.doctor == 'Napr':
                zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                      json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                            "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                       "specialityId": self.specID}})
                jszapis = zapis.json()
                proczapis = requests.post(
                    'https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo',
                    json={"jsonrpc": "2.0", "id": "7g9bgvEa8VkCd6A2XHJ7p",
                          "method": "getAvailableResourceScheduleInfo",
                          "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                     "availableResourceId": instance.availRES,
                                     "complexResourceId": instance.resID,
                                     "specialityId": self.specID, 'referralId': self.refferal}})
                jsproczapis = proczapis.json()
                tabs = MDTabs(
                    radius=[10, 10, 0, 0],
                    allow_stretch=True,
                    background_color=get_color_from_hex('51857A'),
                    tab_hint_x=True,
                    tab_bar_height='90'
                )
                for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
                    tab = Tab(
                        title=time.strftime("%d\n%a")
                    )
                    tab.tab_label.font_size = '40sp'
                    scrolllayout = ScrollView(
                        size_hint=(.8, 1),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    scrolllayout.pos_hint = {'center_x': .54, 'center_y': .45}
                    layout = StackLayout(adaptive_height=True)
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButtonNew(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            group="x",
                            text_color=get_color_from_hex('#D4F5EC'),
                            md_bg_color=get_color_from_hex('#51857A'),
                        )
                        times.font_size = 60
                        times.size_hint_y = None
                        times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'endTime']
                        times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'startTime']
                        layout.add_widget(times)
                    layout.height = layout.minimum_height
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            else:
                zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo',
                                      json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                            "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                       "referralId": self.refferal}})
                jszapis = zapis.json()
                proczapis = requests.post(
                    'https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo',
                    json={"jsonrpc": "2.0", "id": "7g9bgvEa8VkCd6A2XHJ7p",
                          "method": "getAvailableResourceScheduleInfo",
                          "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                     "availableResourceId": instance.availRES,
                                     "complexResourceId": instance.resID,
                                     "referralId": self.refferal}})
                jsproczapis = proczapis.json()
                tabs = MDTabs(
                    radius=[10, 10, 0, 0],
                    allow_stretch=True,
                    background_color=get_color_from_hex('51857A'),
                    tab_hint_x=True,
                    tab_bar_height='90'
                )
                for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
                    tab = Tab(
                        title=time.strftime("%d\n%a")
                    )
                    tab.tab_label.font_size = '40sp'
                    scrolllayout = ScrollView(
                        size_hint=(.8, 1),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    scrolllayout.pos_hint = {'center_x': .54, 'center_y': .45}
                    layout = StackLayout(adaptive_height=True)
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButtonNew(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            group="x",
                            text_color=get_color_from_hex('#D4F5EC'),
                            md_bg_color=get_color_from_hex('#51857A'),
                        )
                        times.font_size = 60
                        times.size_hint_y = None
                        times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'endTime']
                        times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j][
                            'startTime']
                        layout.add_widget(times)
                    layout.height = layout.minimum_height
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)

            self.manager.current = 'timetable'
        except Exception as ex:
            print(ex)
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            self.manager.current = 'omserrorunk'

    def priem(self):
        self.manager.current = 'priem'


class OMSAlertScreen(Screen):
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

class SuccOtmena(Screen):
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

class SuccPerenos(Screen):
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

class Succ(Screen):
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