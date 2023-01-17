import datetime
from MyComponents.mycomponents import Tab, MyToggleButton, MyToggleButtonNew, Item, Itemerrors, Itemfactor, Itemwait, Full
from kivymd.uix.label import MDLabel
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
    dialog = None
    dialogsucc = None
    dialogsuccper = None
    error = None
    news = None
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

    def errord(self):
        if not self.error:
            self.error = MDDialog(
                title="Произошла непредвиденная ошибка повторите еще раз",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.error.dismiss(),
                    )
                ],
            )
        self.error.open()

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

    def full_dialog(self):
        def enterfull(*args):
            self.manager.current = "mos"

        if not self.dialog:
            self.dialog = MDDialog(
                type='custom',
                content_cls=Full(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Принять",
                        md_bg_color="0000ff",
                        on_press=lambda _: self.dialog.dismiss(),
                        on_release=enterfull
                    ),
                    MDFillRoundFlatButton(
                        text="Отмена",
                        md_bg_color="ff0000",
                        on_release=lambda _: self.dialog.dismiss(),
                    )
                ],
            )
        self.dialog.open()

    def exits(self):
        self.manager.current = 'enter'

    def prikreplenia(self):
        inf = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getPatientInfo3', json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE", "method": "getPatientInfo3",
                                        "params": {"omsNumber": self.oms, "birthDate": self.bdates, "typeAttach": [0, 1, 2],
                                                   "onlyMoscowPolicy": False}})
        jsinf = inf.json()
        for i in range(len(jsinf['result']['attachments']['attachment'])):
            rlayout = RelativeLayout()
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            name = MDLabel(
                text=jsinf['result']['attachments']['attachment'][i]['lpu']['name']
            )
            name.font_size = 45
            name.pos_hint = {'center_x': .55, 'center_y': .8}
            rlayout.add_widget(name)
            address = MDLabel(
                text=jsinf['result']['attachments']['attachment'][i]['lpu']['address']
            )
            address.font_size = 35
            address.pos_hint = {'center_x': .55, 'center_y': .6}
            rlayout.add_widget(address)
            time = datetime.datetime.fromisoformat(jsinf['result']['attachments']['attachment'][i]['createDate'])
            create = MDLabel(
                text=f'{time.strftime("Прикреплено от %d %B %Y")}',
            )
            create.font_size = 35
            create.pos_hint = {'center_x': .55, 'center_y': .4}
            rlayout.add_widget(create)
            card.add_widget(rlayout)
            self.manager.get_screen('prik').ids.lay.add_widget(card)
        self.manager.current = 'prik'

    def zapisi(self):
        prosmotr = requests.post("https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient", json={"jsonrpc": "2.0", "id": "tnSZKjovHE_X2b-JYQ0PB",
                                                "method": "getAppointmentReceptionsByPatient",
                                                "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
        jsps = prosmotr.json()
        if len(jsps["result"]) == 0:
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            label = MDLabel(
                text='Записей нет',
                theme_text_color='Custom',
                text_color='white',
                halign='center'
            )
            label.font_size = 60
            label.pos_hint = {'center_x': .5, 'center_y': .5}
            layout.add_widget(label)
            card.add_widget(layout)
            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
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
        self.manager.current = 'zapisi'

    def otmenas(self, instance):
        otmenas = requests.post("https://emias.info/api/emc/appointment-eip/v1/?cancelAppointment",
                                json={"jsonrpc": "2.0", "id": "lXe4h6pwr3IF-xCqBnESK", "method": "cancelAppointment",
                                      "params": {"omsNumber": self.oms, "birthDate": self.bdates,
                                                 "appointmentId": instance.zapisid}})
        self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
        self.succ()
        self.manager.get_screen('loged').zapisi()

    def perenoss(self, instance):
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

    def showdateandtime(self, instance):
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

    def appointment(self):
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
            self.errord()

    def perenesti(self):
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
            self.errord()

    def prosmotrnapr(self):
        prosmotrnaprs = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getReferralsInfo', json={"jsonrpc": "2.0", "id": "6Ov41JqE7a1bQ3i98ofeF",
                                                 "method": "getReferralsInfo",
                                                 "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
        jsnp = prosmotrnaprs.json()
        if len(jsnp["result"]) == 0:
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            label = MDLabel(
                text='Направлений нет',
                halign='center',
                theme_text_color='Custom',
                text_color='white',
            )
            label.font_size = 40
            label.pos_hint = {'center_x': .5, 'center_y': .5}
            layout.add_widget(label)
            card.add_widget(layout)
            self.manager.get_screen("napr").ids.scrollid.add_widget(card)
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

    def newzapis(self):
        specialities = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo', json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                                "method": "getSpecialitiesInfo",
                                                "params": {"omsNumber": self.oms, "birthDate": self.bdates}})
        jsspec = specialities.json()
        for i in range(len(jsspec["result"])):
            card = MDCard(orientation='vertical', size_hint=(1, None), height=150,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            name = MDLabel(
                text=jsspec['result'][i]["name"].replace("_", " "),
                theme_text_color='Custom',
                text_color='white'
            )
            name.font_size = 35
            name.pos_hint = {'center_x': .55, 'center_y': .8}
            choose = MDFillRoundFlatButton(
                text="Выбрать",
                theme_text_color='Custom',
                text_color='white',
            )
            choose.bind(on_release=self.new)
            choose.zapisid = i
            choose.pos_hint = {'center_x': .85, 'center_y': .5}
            choose.font_size = 40
            layout.add_widget(choose)
            layout.add_widget(name)
            card.add_widget(layout)
            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
        self.manager.current = 'zapisi'

    def new(self, instance):
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
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                          md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            label = MDLabel(
                text='Запись не доступна',
                halign='center',
                theme_text_color='Custom',
                text_color='white',
            )
            label.font_size = 40
            label.pos_hint = {'center_x': .5, 'center_y': .5}
            layout.add_widget(label)
            card.add_widget(layout)
            self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
        else:
            for i in range(len(jszapis["result"])):
                for j in range(len(jszapis["result"][i]['complexResource'])):
                    if 'room' in jszapis["result"][i]['complexResource'][j]:
                        card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                                      md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                        layout = RelativeLayout()
                        name = MDLabel(
                            text=jszapis['result'][i]["name"].replace('_', " "),
                            theme_text_color='Custom',
                            text_color='white'
                        )
                        name.font_size = 45
                        name.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(name)
                        time = datetime.datetime.fromisoformat(
                            jszapis["result"][i]['complexResource'][j]['room']['availabilityDate'])
                        avail = MDLabel(
                            text=f'{time.strftime("С %d %b, %a")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        avail.font_size = 35
                        avail.pos_hint = {'center_x': .55, 'center_y': .6}
                        layout.add_widget(avail)
                        address = MDLabel(
                            text=jszapis["result"][i]['complexResource'][j]['room']['lpuShortName'],
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        address.font_size = 30
                        address.pos_hint = {'center_x': .55, 'center_y': .4}
                        fulladdress = MDLabel(
                            text=jszapis["result"][i]['complexResource'][j]['room']['defaultAddress'],
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
                        perenos.resID = jszapis["result"][i]['complexResource'][j]['id']
                        perenos.availRES = jszapis["result"][i]['id']
                        perenos.bind(on_release=self.showdateandtimenew)
                        perenos.pos_hint = {'center_x': .85, 'center_y': .2}
                        perenos.font_size = 40
                        layout.add_widget(perenos)
                        card.add_widget(layout)
                        self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
        self.manager.current = 'perenos'

    def showdateandtimenew(self, instance):
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
        tabs = MDTabs(
            radius=[30, 30, 0, 0],
            allow_stretch=True,
            tab_hint_x=True,
            tab_bar_height='80'
        )
        for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
            time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
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
            for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                timeF = datetime.datetime.fromisoformat(
                    jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                times = MyToggleButtonNew(
                    text=timeF.strftime("%H:%M"),
                    theme_text_color='Custom',
                    text_color='white',
                    md_bg_color='grey',
                    group="x"
                )
                times.font_size = 60
                times.size_hint_y = None
                times.endTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['endTime']
                times.startTime = jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime']
                layout.add_widget(times)
            layout.height = layout.minimum_height
            scrolllayout.add_widget(layout)
            tab.add_widget(scrolllayout)
            tabs.add_widget(tab)
        self.manager.get_screen('timetable').ids.lay.add_widget(tabs)
        self.manager.current = 'timetable'
    def priem(self):
        self.manager.current = 'priem'
class OMSAlertScreen(Screen):
    pass