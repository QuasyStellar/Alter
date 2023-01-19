import datetime
from MyComponents.mycomponents import Tab, MyToggleButton, MyToggleButtonNew
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.tab import MDTabs
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
import requests
from kivymd.uix.card import MDCard

class OMSLoged(Screen):
    dialogsucc = None
    dialogsuccper = None
    news = None
    types = None
    #
    def screenback(self):
        if self.types == 'oms':
            self.manager.current = 'loged'
        else:
            self.manager.current = 'mosloged'

    def succ(self):
        if not self.dialogsucc:
            self.dialogsucc = MDDialog(
                title="Запись успешно отменена",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogsucc.dismiss(),
                    )
                ],
            )
        self.dialogsucc.open()


    def succper(self):
        if not self.dialogsuccper:
            self.dialogsuccper = MDDialog(
                title="Запись успешно перенесена",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogsuccper.dismiss(),
                    )
                ],
            )
        self.dialogsuccper.open()

    def newd(self):
        if not self.news:
            self.news = MDDialog(
                title="Вы успешно записаны",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.news.dismiss(),
                    )
                ],
            )
        self.news.open()


    def exits(self):
        self.manager.current = 'enter'

    def prikreplenia(self):
        try:
            inf = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getPatientInfo3', json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE", "method": "getPatientInfo3",
                                            "params": {"omsNumber": self.oms, "birthDate": self.bdates, "typeAttach": [0, 1, 2],
                                                       "onlyMoscowPolicy": False}})
            jsinf = inf.json()
            for i in range(len(jsinf['result']['attachments']['attachment'])):
                layout = RelativeLayout(size_hint=(1, None), height=330)
                layout.add_widget(Image(source= 'Assets/omsloged/prikbutton.png'))
                name = MDLabel(
                    text=jsinf['result']['attachments']['attachment'][i]['lpu']['name'],
                    text_color=get_color_from_hex('#D4F5EC'), 
                    theme_text_color='Custom'
                )
                name.font_name =  'Assets/fonts/roboto.ttf'
                name.font_size = 30
                name.pos_hint = {'center_x': .78, 'center_y': .7}
                layout.add_widget(name)
                address = MDLabel(
                    text=jsinf['result']['attachments']['attachment'][i]['lpu']['address'],
                    text_color=get_color_from_hex('#D4F5EC'), 
                    theme_text_color='Custom'
                )
                address.font_name =  'Assets/fonts/roboto.ttf'
                address.font_size = 30
                address.pos_hint = {'center_x': .78, 'center_y': .5}
                layout.add_widget(address)
                time = datetime.datetime.fromisoformat(jsinf['result']['attachments']['attachment'][i]['createDate'])
                create = MDLabel(
                    text=f'{time.strftime("Прикреплено от %d %B %Y")}',
                    text_color=get_color_from_hex('#D4F5EC'), 
                    theme_text_color='Custom'
                )
                create.font_name =  'Assets/fonts/roboto.ttf'
                create.font_size = 30
                create.pos_hint = {'center_x': .78, 'center_y': .3}
                layout.add_widget(create)
                self.manager.get_screen('prik').ids.lay.add_widget(layout)
            self.manager.current = 'prik'
        except:
            self.manager.current = 'omserrorunk'

    def zapisi(self):
        try:
            prosmotr = requests.post("https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient", json={"jsonrpc": "2.0", "id": "tnSZKjovHE_X2b-JYQ0PB",
                                                "method": "getAppointmentReceptionsByPatient",
                                                "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsps = prosmotr.json()
            if len(jsps["result"]) == 0:
                layout = RelativeLayout(size_hint=(1, None), height=200)
                layout.add_widget(Image(source= 'Assets/omsloged/nozapis.png'))
                self.manager.get_screen("zapisi").ids.scrollid.add_widget(layout)
            else:
                for i in range(len(jsps['result'])):
                    if 'toDoctor' in jsps["result"][i]:
                        card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                      md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                        layout = RelativeLayout()
                        specname = MDLabel(
                            text=f'{jsps["result"][i]["toDoctor"]["specialityName"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        specname.font_size = 45
                        specname.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(specname)
                        time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                        timelab = MDLabel(
                            text=f'{time.strftime("%a, %d %b в %H:%M")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        timelab.font_size = 35
                        timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                        layout.add_widget(timelab)
                        address = MDLabel(
                            text=f'{jsps["result"][i]["nameLpu"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        address.font_size = 35
                        address.pos_hint = {'center_x': .55, 'center_y': .27}
                        layout.add_widget(address)
                        addressbol = MDLabel(
                            text=f'{jsps["result"][i]["lpuAddress"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        addressbol.font_size = 35
                        addressbol.pos_hint = {'center_x': .55, 'center_y': .15}
                        layout.add_widget(addressbol)
                        room = MDLabel(
                            text=f'Каб. {jsps["result"][i]["roomNumber"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        room.font_size = 40
                        room.pos_hint = {'center_x': 1.2, 'center_y': .5}
                        layout.add_widget(room)
                        fio = MDLabel(
                            text=f'{jsps["result"][i]["toDoctor"]["doctorFio"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        fio.font_size = 30
                        fio.pos_hint = {'center_x': .55, 'center_y': .66}
                        layout.add_widget(fio)
                        otmena = MDIconButton(
                            theme_text_color='Custom',
                            text_color='red',
                            icon='delete'
                        )
                        otmena.zapisid = jsps["result"][i]["id"]
                        otmena.bind(on_release=self.otmenas)
                        otmena.pos_hint = {'center_x': .95, 'center_y': .2}
                        otmena.icon_size = '60dp'
                        layout.add_widget(otmena)

                        perenos = MDFillRoundFlatButton(
                            text="Перенести",
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        perenos.zapisid = jsps["result"][i]["id"]
                        perenos.bind(on_release=self.perenoss)
                        perenos.pos_hint = {'center_x': .8, 'center_y': .2}
                        perenos.font_size = 40
                        perenos.zapisid = i
                        layout.add_widget(perenos)
                        card.add_widget(layout)
                        self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
                    else:
                        card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                      md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                        layout = RelativeLayout()
                        specname = MDLabel(
                            text=jsps["result"][i]["toLdp"]["ldpTypeName"],
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        specname.font_size = 45
                        specname.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(specname)
                        time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                        timelab = MDLabel(
                            text=f'{time.strftime("%a, %d %b в %H:%M")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        timelab.font_size = 35
                        timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                        layout.add_widget(timelab)
                        address = MDLabel(
                            text=f'{jsps["result"][i]["nameLpu"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        address.font_size = 35
                        address.pos_hint = {'center_x': .55, 'center_y': .27}
                        layout.add_widget(address)
                        addressbol = MDLabel(
                            text=f'{jsps["result"][i]["lpuAddress"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        addressbol.font_size = 35
                        addressbol.pos_hint = {'center_x': .55, 'center_y': .15}
                        layout.add_widget(addressbol)
                        room = MDLabel(
                            text=f'Каб. {jsps["result"][i]["roomNumber"]}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        room.font_size = 40
                        room.pos_hint = {'center_x': 1.2, 'center_y': .5}
                        layout.add_widget(room)
                        otmena = MDIconButton(
                            theme_text_color='Custom',
                            text_color='red',
                            icon='delete'
                        )
                        otmena.zapisid = jsps["result"][i]["id"]
                        otmena.bind(on_release=self.otmenas)
                        otmena.pos_hint = {'center_x': .95, 'center_y': .2}
                        otmena.icon_size = '60dp'
                        layout.add_widget(otmena)

                        perenos = MDFillRoundFlatButton(
                            text="Перенести",
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        perenos.bind(on_release=self.perenoss)
                        perenos.pos_hint = {'center_x': .8, 'center_y': .2}
                        perenos.font_size = 40
                        perenos.zapisid = i
                        layout.add_widget(perenos)
                        card.add_widget(layout)
                        self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
            self.manager.get_screen('zapisi').ids.backgr.source = 'Assets/omsloged/myzapisi.png'
            self.manager.get_screen('zapisi').ids.backgr.reload()
            self.manager.current = 'zapisi'
        except Exception as ex:
            print(ex)
            self.manager.current = 'omserrorunk'

    def otmenas(self, instance):
        try:
            otmenas = requests.post("https://emias.info/api/emc/appointment-eip/v1/?cancelAppointment",
                                    json={"jsonrpc": "2.0", "id": "lXe4h6pwr3IF-xCqBnESK", "method": "cancelAppointment",
                                          "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                     "appointmentId": instance.zapisid}})
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.succ()
            self.manager.get_screen('loged').zapisi()
        except:
            self.manager.current = 'omserrorunk'

    def perenoss(self, instance):
        try:
            c = 0
            spisokzapisei = requests.post("https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient", json={"jsonrpc": "2.0", "id": "H0XYtGjt9CtPQqfGt7NYp",
                                                         "method": "getAppointmentReceptionsByPatient",
                                                         "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspisok = spisokzapisei.json()
            zapisvibor = instance.zapisid
            if 'toDoctor' in jsspisok['result'][zapisvibor]:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
                self.recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo', json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                              "method": "getDoctorsInfo",
                                                              "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                         "appointmentId": self.appID, "specialityId": self.specID}})
                jsvrachi = spisokvrachei.json()
                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c += 1
                if c == 0:
                    card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                  md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                    layout = RelativeLayout()
                    label = MDLabel(
                        text='Перенос не доступен',
                        theme_text_color='Custom',
                        text_color='white',
                        halign='center'
                    )
                    label.font_size = 40
                    label.pos_hint = {'center_x': .5, 'center_y': .5}
                    layout.add_widget(label)
                    card.add_widget(layout)
                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
                else:
                    for i in range(len(jsvrachi["result"])):
                        for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                                layout = RelativeLayout()
                                name = MDLabel(
                                    text=jsvrachi["result"][i]['name'].replace("_", " "),
                                    theme_text_color='Custom',
                                    text_color='white'
                                )
                                name.font_size = 45
                                name.pos_hint = {'center_x': .55, 'center_y': .8}
                                layout.add_widget(name)
                                time = datetime.datetime.fromisoformat(
                                    jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                avail = MDLabel(
                                    text=f'{time.strftime("С %d %b, %a")}',
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                avail.font_size = 35
                                avail.pos_hint = {'center_x': .55, 'center_y': .6}
                                layout.add_widget(avail)
                                address = MDLabel(
                                    text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                address.font_size = 30
                                address.pos_hint = {'center_x': .55, 'center_y': .4}
                                fulladdress = MDLabel(
                                    text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                fulladdress.font_size = 30
                                fulladdress.pos_hint = {'center_x': .55, 'center_y': .2}
                                layout.add_widget(fulladdress)
                                layout.add_widget(address)
                                perenos = MDFillRoundFlatButton(
                                    text="Выбрать",
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                perenos.vrachnum = i
                                perenos.zapisvibor = zapisvibor
                                perenos.bind(on_release=self.showdateandtime)
                                perenos.pos_hint = {'center_x': .85, 'center_y': .2}
                                perenos.font_size = 40
                                layout.add_widget(perenos)
                                card.add_widget(layout)
                                self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            else:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo', json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                              "method": "getDoctorsInfo",
                                                              "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                         "appointmentId": self.appID}})
                jsvrachi = spisokvrachei.json()
                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c += 1
                if c == 0:
                    card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                  md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                    layout = RelativeLayout()
                    label = MDLabel(
                        text='Перенос не доступен',
                        theme_text_color='Custom',
                        text_color='white',
                        halign='center'
                    )
                    label.font_size = 40
                    label.pos_hint = {'center_x': .5, 'center_y': .5}
                    layout.add_widget(label)
                    card.add_widget(layout)
                    self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
                else:
                    for i in range(len(jsvrachi["result"])):
                        for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                                layout = RelativeLayout()
                                name = MDLabel(
                                    text=jsvrachi["result"][i]['name'].replace("_", " "),
                                    theme_text_color='Custom',
                                    text_color='white'
                                )
                                name.font_size = 45
                                name.pos_hint = {'center_x': .55, 'center_y': .8}
                                layout.add_widget(name)
                                time = datetime.datetime.fromisoformat(
                                    jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                avail = MDLabel(
                                    text=f'{time.strftime("С %d %b, %a")}',
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                avail.font_size = 35
                                avail.pos_hint = {'center_x': .55, 'center_y': .6}
                                layout.add_widget(avail)
                                address = MDLabel(
                                    text=jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                address.font_size = 30
                                address.pos_hint = {'center_x': .55, 'center_y': .4}
                                fulladdress = MDLabel(
                                    text=jsvrachi["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                fulladdress.font_size = 30
                                fulladdress.pos_hint = {'center_x': .55, 'center_y': .2}
                                layout.add_widget(fulladdress)
                                layout.add_widget(address)
                                perenos = MDFillRoundFlatButton(
                                    text="Выбрать",
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                perenos.vrachnum = i
                                perenos.zapisvibor = zapisvibor
                                perenos.bind(on_release=self.showdateandtime)
                                perenos.pos_hint = {'center_x': .85, 'center_y': .2}
                                perenos.font_size = 40
                                layout.add_widget(perenos)
                                card.add_widget(layout)
                                self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            self.manager.current = 'perenos'
        except:
            self.manager.current = 'omserrorunk'

    def showdateandtime(self, instance):
        try:
            vrachchoose = instance.vrachnum
            zapisvibor =  instance.zapisvibor
            spisokzapisei = requests.post("https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient", json={"jsonrpc": "2.0", "id": "H0XYtGjt9CtPQqfGt7NYp",
                                                         "method": "getAppointmentReceptionsByPatient",
                                                         "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspisok = spisokzapisei.json()
            if 'toDoctor' in jsspisok["result"][zapisvibor]:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
                self.recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo', json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                              "method": "getDoctorsInfo",
                                                              "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                         "appointmentId": self.appID, "specialityId": self.specID}})
                jsvrachi = spisokvrachei.json()
                self.resID = jsvrachi["result"][vrachchoose]["id"]
                for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                    if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                        self.complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
                dati = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo', json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE",
                                                     "method": "getAvailableResourceScheduleInfo",
                                                     "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                "availableResourceId": self.resID, "complexResourceId": self.complID,
                                                                "appointmentId": self.appID, "specialityId": self.specID}})
                jsdati = dati.json()
                tabs = MDTabs(
                    radius=[30, 30, 0, 0],
                    allow_stretch=True,
                    tab_hint_x=True,
                    tab_bar_height='150'
                )
                for i in range(len(jsdati["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsdati["result"]['scheduleOfDay'][i]['date'])
                    tab = Tab(
                        title=f'{time.strftime("%d %a")}'
                    )
                    tab.tab_label.font_size = '30sp'
                    scrolllayout = ScrollView(
                        size_hint=(1, .9),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    layout = StackLayout()
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButton(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            text_color='white',
                            md_bg_color='grey',
                            group="x"
                        )
                        times.font_size = 35
                        times.height = 100
                        times.width = 100
                        times.endTime = jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['endTime']
                        times.startTime = jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime']
                        layout.add_widget(times)
                    layout.height = layout.minimum_height
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            else:
                self.appID = jsspisok["result"][zapisvibor]['id']
                self.recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
                spisokvrachei = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo', json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB",
                                                              "method": "getDoctorsInfo",
                                                              "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                         "appointmentId": self.appID}})
                jsvrachi = spisokvrachei.json()
                self.resID = jsvrachi["result"][vrachchoose]["id"]
                for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                    if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                        self.complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
                dati = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo', json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE",
                                                     "method": "getAvailableResourceScheduleInfo",
                                                     "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                "availableResourceId": self.resID, "complexResourceId": self.complID,
                                                                "appointmentId": self.appID, "specialityId": self.specID}})
                jsdati = dati.json()
                tabs = MDTabs(
                    radius=[30, 30, 0, 0],
                    allow_stretch=True,
                    tab_hint_x=True,
                    tab_bar_height='150'
                )
                for i in range(len(jsdati["result"]['scheduleOfDay'])):
                    time = datetime.datetime.fromisoformat(jsdati["result"]['scheduleOfDay'][i]['date'])
                    tab = Tab(
                        title=f'{time.strftime("%d %a")}'
                    )
                    tab.tab_label.font_size = '40sp'
                    scrolllayout = ScrollView(
                        size_hint=(1, .9),
                        md_bg_color=(1, 1, 1, 0)
                    )
                    layout = StackLayout()
                    layout.size_hint_y = None
                    layout.spacing = 40
                    for j in range(len(jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                        timeF = datetime.datetime.fromisoformat(
                            jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                        times = MyToggleButton(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color='Custom',
                            text_color='white',
                            md_bg_color='grey',
                            group="x"
                        )
                        times.font_size = 35
                        times.height = 100
                        times.width = 100
                        times.endTime = jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['endTime']
                        times.startTime = jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime']
                        layout.add_widget(times)
                    layout.height = layout.minimum_height
                    scrolllayout.add_widget(layout)
                    tab.add_widget(scrolllayout)
                    tabs.add_widget(tab)
                self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            self.manager.current = 'timetable'
        except:
            self.manager.current = 'omserrorunk'

    def appointment(self):
        try:
            appocreate = requests.post("https://emias.info/api/emc/appointment-eip/v1/?createAppointment",
                                       json={"jsonrpc": "2.0", "id": "AvyJzHk1dm8eNqyg5uzLx", "method": "createAppointment",
                                             "params": {"omsNumber": self.oms, "birthDate": self.bdates, "availableResourceId": self.resID,
                                                        "complexResourceId": self.complID, "receptionTypeId": self.recpID,
                                                        "startTime": self.perenosStart, "endTime": self.perenosEnd}})
            jscheck = appocreate.json()
            if "error" not in jscheck:
                self.newd()
                self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
                self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
                self.manager.get_screen('timetable').ids.lay.clear_widgets()
                self.manager.get_screen('loged').zapisi()
            else:
                self.manager.current = 'omserrorunk'
        except:
            self.manager.current = 'omserrorunk'

    def perenesti(self):
        try:
            perenes = requests.post("https://emias.info/api/emc/appointment-eip/v1/?shiftAppointment",
                                    json={"jsonrpc": "2.0", "id": "7LIqTOs9j1zSf-c7ohSzB", "method": "shiftAppointment",
                                          "params": {"omsNumber": self.oms, "birthDate": self.bdates, "appointmentId": self.appID,
                                                     "availableResourceId": self.resID, "complexResourceId": self.complID,
                                                     "receptionTypeId": self.recpID, "startTime": self.perenosStart,
                                                     "endTime": self.perenosEnd}})
            jscheck = perenes.json()
            if "error" not in jscheck:
                self.succper()
                self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
                self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
                self.manager.get_screen('timetable').ids.lay.clear_widgets()
                self.manager.get_screen('loged').zapisi()
            else:
                self.manager.current = 'omserrorunk'
        except:
            self.manager.current = 'omserrorunk'

    def prosmotrnapr(self):
        try:
            prosmotrnaprs = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getReferralsInfo', json={"jsonrpc": "2.0", "id": "6Ov41JqE7a1bQ3i98ofeF",
                                                     "method": "getReferralsInfo",
                                                     "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsnp = prosmotrnaprs.json()
            if len(jsnp["result"]) == 0:
                layout = RelativeLayout(size_hint=(1, None), height=200)
                layout.add_widget(Image(source= 'Assets/omsloged/nonapr.png'))
                self.manager.get_screen("napr").ids.scrollid.add_widget(layout)
            else:
                for i in range(len(jsnp["result"])):
                    if 'toDoctor' in jsnp['result'][i]:
                        card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                      md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                        layout = RelativeLayout()
                        name = MDLabel(
                            text=jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "),
                            theme_text_color='Custom',
                            text_color='white'
                        )
                        name.font_size = 35
                        name.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(name)
                        time = datetime.datetime.fromisoformat(jsnp["result"][i]["startTime"])
                        avail = MDLabel(
                            text=f'{time.strftime("С %d %b, %a")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        avail.font_size = 35
                        avail.pos_hint = {'center_x': .55, 'center_y': .6}
                        layout.add_widget(avail)
                        end = MDLabel(
                            text=jsnp["result"][i]["endTime"],
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        end.font_size = 30
                        end.pos_hint = {'center_x': .55, 'center_y': .4}
                        layout.add_widget(end)
                        card.add_widget(layout)
                        self.manager.get_screen("napr").ids.scrollid.add_widget(card)
                    else:
                        card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                      md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                        layout = RelativeLayout()
                        name = MDLabel(
                            text=jsnp["result"][i]["toLdp"]["ldpTypeName"].replace("_", " "),
                            theme_text_color='Custom',
                            text_color='white'
                        )
                        name.font_size = 35
                        name.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(name)
                        time = datetime.datetime.fromisoformat(jsnp["result"][i]["startTime"])
                        avail = MDLabel(
                            text=f'{time.strftime("С %d %b, %a")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        avail.font_size = 35
                        avail.pos_hint = {'center_x': .55, 'center_y': .6}
                        layout.add_widget(avail)
                        end = MDLabel(
                            text=jsnp["result"][i]["endTime"],
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        end.font_size = 30
                        end.pos_hint = {'center_x': .55, 'center_y': .4}
                        layout.add_widget(end)
                        card.add_widget(layout)
                        self.manager.get_screen("napr").ids.scrollid.add_widget(card)
            self.manager.current = 'napr'
        except:
            self.manager.current = 'omserrorunk'

    def newzapis(self):
        try:
            specialities = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo', json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                                    "method": "getSpecialitiesInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspec = specialities.json()
            for i in range(len(jsspec["result"])):
                choose = MDCard(size_hint=(1, None), height=180, md_bg_color = (0,0,0,0))
                layout = RelativeLayout()
                layout.add_widget(Image(source= 'Assets/omsloged/newzapisbutton.png', height = 142, width = 142))
                if 'Офтальмолог' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/eyes.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))
                elif 'Оториноларинголог' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/ear.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))
                elif 'Стоматолог' in jsspec['result'][i]["name"].replace("_", " ") or 'зуб' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/tooth.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))
                elif 'Гастроэнтеролог' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/gastro.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))
                elif 'справ' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/document.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))
                elif 'ОРВИ' in jsspec['result'][i]["name"].replace("_", " "):
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/covid19.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))
                else:
                    layout.add_widget(Image(source= 'Assets/omsloged/docicons/docdefault.png', height = 142, width = 142, pos_hint={'center_x':.1 , 'center_y':.49}))

                name = MDLabel(
                    text=jsspec['result'][i]["name"].replace("_", " "),
                    theme_text_color='Custom',
                    text_color=get_color_from_hex('#D4F5EC'),
                )
                name.font_size = 35
                name.font_name =  'Assets/fonts/roboto.ttf'
                name.pos_hint = {'center_x': .7, 'center_y': .5}
                choose.bind(on_release=self.new)
                choose.zapisid = i
                layout.add_widget(name)
                choose.add_widget(layout)
                self.manager.get_screen("zapisi").ids.scrollid.add_widget(choose)
            self.manager.get_screen('zapisi').ids.backgr.source = 'Assets/omsloged/newzapis.png'
            self.manager.get_screen('zapisi').ids.backgr.reload()
            self.manager.current = 'zapisi'

        except:
            self.manager.current = 'omserrorunk'

    def new(self, instance):
        try:
            count = 0
            resid = None
            assignment = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo', json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                                  "method": "getAssignmentsInfo",
                                                  "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsass = assignment.json()
            self.userid = jsass["id"]
            specialities = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo', json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                                    "method": "getSpecialitiesInfo",
                                                    "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
            jsspec = specialities.json()
            self.specID = jsspec['result'][instance.zapisid]["code"]
            zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo', json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
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
                layout.add_widget(Image(source= 'Assets/omsloged/unable.png'))
                self.manager.get_screen("perenos").ids.scrollid.add_widget(layout)
            else:
                for i in range(len(jszapis["result"])):
                    for j in range(len(jszapis["result"][i]['complexResource'])):
                        if 'room' in jszapis["result"][i]['complexResource'][j]:
                            choose = MDCard(size_hint=(1, None), height=280, md_bg_color = (0,0,0,0))
                            layout = RelativeLayout()
                            layout.add_widget(Image(source= 'Assets/omsloged/vrachchoosebutton.png', height = 185, width = 185))
                            if 'Офтальмолог' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/eyes.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))
                            elif 'Оториноларинголог' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/ear.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))
                            elif 'Стоматолог' in jszapis['result'][i]["name"].replace("_", " ") or 'зуб' in jsspec['result'][i]["name"].replace("_", " "):
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/tooth.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))
                            elif 'Гастроэнтеролог' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/gastro.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))
                            elif 'справ' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/document.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))
                            elif 'ОРВИ' in jszapis['result'][i]["name"].replace("_", " "):
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/covid19.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))
                            else:
                                layout.add_widget(Image(source= 'Assets/omsloged/docicons/docdefault.png', height = 185, width = 185, pos_hint={'center_x':.1 , 'center_y':.49}))

                            name = MDLabel(
                                text=jszapis['result'][i]["name"].replace('_', " "),
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            name.font_size = 30
                            name.font_name =  'Assets/fonts/roboto.ttf'
                            name.pos_hint = {'center_x': .7, 'center_y': .65}
                            time = datetime.datetime.fromisoformat(
                                jszapis["result"][i]['complexResource'][j]['room']['availabilityDate'])
                            avail = MDLabel(
                                text=f'{time.strftime("С %d %b, %a")}',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            avail.font_name =  'Assets/fonts/roboto.ttf'
                            avail.font_size = 30
                            avail.pos_hint = {'center_x': 1.3, 'center_y': .23}
                            address = MDLabel(
                                text=jszapis["result"][i]['complexResource'][j]['room']['lpuShortName'],
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            address.font_size = 30
                            address.font_name =  'Assets/fonts/roboto.ttf'
                            address.pos_hint = {'center_x': .7, 'center_y': .5}
                            fulladdress = MDLabel(
                                text=jszapis["result"][i]['complexResource'][j]['room']['defaultAddress'],
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('#D4F5EC'),
                            )
                            fulladdress.font_size = 30
                            fulladdress.font_name =  'Assets/fonts/roboto.ttf'
                            fulladdress.pos_hint = {'center_x': .7, 'center_y': .35}
                            layout.add_widget(fulladdress)
                            layout.add_widget(address)
                            layout.add_widget(avail)
                            layout.add_widget(name)
                            choose.resID = jszapis["result"][i]['complexResource'][j]['id']
                            choose.availRES = jszapis["result"][i]['id']
                            choose.bind(on_release=self.showdateandtimenew)
                            choose.add_widget(layout)
                            self.manager.get_screen("perenos").ids.scrollid.add_widget(choose)
            self.manager.current = 'perenos'
        except Exception as ex:
            print(ex)
            self.manager.current = 'omserrorunk'

    def showdateandtimenew(self, instance):
        try:
            self.resID = instance.availRES
            self.complID = instance.resID
            zapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo', json={"jsonrpc": "2.0", "id": self.userid, "method": "getDoctorsInfo",
                                                  "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                             "specialityId": self.specID}})
            jszapis = zapis.json()
            proczapis = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo', json={"jsonrpc": "2.0", "id": "7g9bgvEa8VkCd6A2XHJ7p",
                                                      "method": "getAvailableResourceScheduleInfo",
                                                      "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                                 "availableResourceId": instance.availRES,
                                                                 "complexResourceId": instance.resID,
                                                                 "specialityId": self.specID}})
            jsproczapis = proczapis.json()
            for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
                time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
                title=f'{time.strftime("%d %a")}'
                for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                    timeF = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                    times = MyToggleButtonNew(
                        text=timeF.strftime("%H:%M"),
                        theme_text_color='Custom',
                        text_color='white',
                        md_bg_color='grey',
                        group="x"
                    )
                    times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['endTime']
                    times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime']
            self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
            self.manager.current = 'timetable'
        except:
            self.manager.current = 'omserrorunk'
    def priem(self):
        self.manager.current = 'priem'
class OMSAlertScreen(Screen):
    pass