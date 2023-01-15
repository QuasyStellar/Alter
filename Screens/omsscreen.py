import sys
import locale
locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivy.clock import Clock
import threading
from kivy.clock import Clock, mainthread
from kivymd.uix.screen import MDScreen as Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.effects.fadingedge.fadingedge import FadingEdgeEffect
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker
from kivy.utils import get_color_from_hex
import requests

class FadeScrollView(FadingEdgeEffect, ScrollView):
    pass

class OneLineListItemAligned(OneLineListItem):
    def __init__(self, halign, **kwargs):
        super(OneLineListItemAligned, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = halign

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
        self.manager.get_screen('priem').cur = 'omsloged'
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
    def validation(self):
        if self.ids.policy.text != '':
            if len(self.ids.policy.text) != 16:
                self.ids.policy.fill_color_normal = get_color_from_hex("B5474D")
            else:
                self.ids.policy.fill_color_normal = get_color_from_hex("#32494B")
        else:
            self.ids.policy.fill_color_normal = 53/255,73/255,75/255,0
    def cou(self):
        self.ids.counts.text = f'{len(self.ids.policy.text)}/16'
        if 16>len(self.ids.policy.text) or len(self.ids.policy.text)>16:
            self.ids.counts.text_color = 'red'
        else:
            self.ids.counts.text_color = 'white'
    def days(self, instance):
        self.day = str(instance.date).zfill(2)
    def months(self, instance):
        print(instance.month)
        if instance.month == 'Январь':
            self.month = '01'
        if instance.month == 'Февраль':
            self.month = '02'
        if instance.month == 'Март':
            self.month = '03'
        if instance.month == 'Апрель':
            self.month = '04'
        if instance.month == 'Май':
            self.month = '05'
        if instance.month == 'Июнь':
            self.month = '06'
        if instance.month == 'Июль':
            self.month = '07'
        if instance.month == 'Август':
            self.month = '08'
        if instance.month == 'Сентябрь':
            self.month = '09'
        if instance.month == 'Октябрь':
            self.month = '10'
        if instance.month == 'Ноябрь':
            self.month = '11'
        if instance.month == 'Декабрь':
            self.month = '12'


    def years(self, instance):
        self.year = instance.year
    pass