import sys
import locale
locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivy.clock import Clock
import threading
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker
import requests

class OMSScreen(Screen):
    dialog = None
    dialog1 = None
    dialogs = None
    timeclocks = None
    @mainthread
    def error(self):
        self.manager.current = "oms"
        self.show_alert_dialog()
    @mainthread
    def error1(self):
        self.manager.current = "oms"
        self.show_alert_dialog1()
    @mainthread
    def succ(self, policy, bdate):
        self.manager.current = "loged"
        policnum = f"[color=#ffffff]{policy[0:4] + ' **** **** ' + policy[12:16]}[/color]"
        self.manager.get_screen("loged").ids.authname.text = policnum
        self.manager.get_screen("loged").oms = policy
        self.manager.get_screen('loged').bdates = bdate
        self.manager.get_screen('loged').types = 'oms'
    def back(self):
        self.manager.current = "enter"
        self.bdate.helper_text = ""
        self.policy.helper_text = ""
        self.policy.text = ""
        self.bdate.text = ""

    def datepicker(self):
        self.date = AKDatePicker(callback=self.callback)
        self.date.open()

    def callback(self, date):
        try:
            year = str(date.year)
            if len(str(date.day)) > 1:
                day = str(date.day)
            else:
                day = "0" + str(date.day)
            if len(str(date.month)) > 1:
                month = str(date.month)
            else:
                month = "0" + str(date.month)
            self.bdate.text = year + "." + month + "." + day
        except:
            None

    def omsfunc(self, policy, bdate):
        t = threading.Thread(
            target=self.open_omslogin, args=[policy, bdate], daemon=True
        )
        t.start()

    def open_omslogin(self, policy, bdate):
        try:
            assignment = requests.post(
                'https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                json={
                    "jsonrpc": "2.0",
                    "id": "ULHOof43sz6OfDTK4KRf1",
                    "method": "getAssignmentsInfo",
                    "params": {"omsNumber": policy, "birthDate": bdate},
                }
            )
            jsass = assignment.json()
            specialities = requests.post(
                'https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo',
                json={
                    "jsonrpc": "2.0",
                    "id": "ULHOof43sz6OfDTK4KRf1",
                    "method": "getSpecialitiesInfo",
                    "params": {"omsNumber": policy, "birthDate": bdate},
                },
            )
            jsspec = specialities.json()
            if "error" in jsass or "error" in jsspec:
                self.error()
            else:
                self.succ(policy, bdate)
        except Exception as ex:
            self.error1()
            print(ex)
        sys.exit()

    def omslogin(self):
        if len(self.policy.text) < 16 or len(self.policy.text) > 16:
            self.policy.helper_text = "Некорректный полис"
            self.policy.helper_text_color_normal = "red"
            self.policy.helper_text_color_focus = "red"
        elif self.bdate.text != "":
            if self.timeclocks == None:
                self.timeclocks = Clock.schedule_interval(self.manager.get_screen('loged').update, 2)
            bdate = self.bdate.text.replace(".", "-")
            oms = self.policy.text
            self.omsfunc(self.policy.text, bdate)
            self.bdate.helper_text = ""
            self.bdate.helper_text_color_normal = "white"
            self.bdate.helper_text_color_focus = "white"
            self.policy.helper_text_color_normal = "white"
            self.policy.helper_text = ""
            self.bdate.text = ''
            self.policy.text = ''
            self.policy.helper_text_color_focus = "white"
            self.manager.current = "loadoms"


        else:
            self.bdate.helper_text = "Введите дату"
            self.bdate.helper_text_color_normal = "red"
            self.bdate.helper_text_color_focus = "red"
            self.policy.helper_text_color_normal = "white"
            self.policy.helper_text = ""
            self.policy.helper_text_color_focus = "white"

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                text="[color=ffffff]Пациен не найден[/color]",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                        on_release=lambda _: self.dialog.dismiss(),
                    )
                ],
            )
        self.dialog.open()

    def show_alert_dialog1(self):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                text="[color=ffffff]Произошла внутренняя ошибка повторите еще раз[/color]",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                        on_release=lambda _: self.dialog1.dismiss(),
                    )
                ],
            )
        self.dialog1.open()

    def show_alert_dialog_info(self):
        if not self.dialogs:
            self.dialogs = MDDialog(
                text="[color=ffffff]При входе по полису ОМС не доступно: первичный осмотр с использованием AI, анализ медкарты. Доступно: Запись по направлению, запись к врачу, перенос. Чтобы воспользоваться полной версией, войдите через mos.ru[/color]",
                md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        md_bg_color=(0 / 255, 106 / 255, 240 / 255, 0.4),
                        on_release=lambda _: self.dialogs.dismiss(),
                    )
                ],
            )
        self.dialogs.open()

    pass