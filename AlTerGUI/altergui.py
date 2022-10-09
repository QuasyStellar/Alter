import re
import time
import threading
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker
from kivymd.utils import asynckivy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RoundedRectangularElevationBehavior,
)


#Window.fullscreen = True
Window.size = (1920, 1080)
#Window.maximize()


KV = '''
#: import Thread threading.Thread
ScreenManager:
    ENTERScreen:
    OMSScreen:
    MOSScreen:
    OMSLoged:
<ENTERScreen>:
    name: 'enter'
    email: email_input
    password: text_field
    Image:
        source: 'bg.png'
        allow_stretch: True
        keep_ratio: False


    RelativeLayout:
        Image:
            source: 'alter.png'
            pos_hint: {'center_x': 0.5, 'center_y': .9}

        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .65}
            size_hint: .2, .4
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDLabel:
                    text: "Войти через [color=1560db]EMIAS[/color]:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: email_input
                    hint_text: "Логин"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(30)
                    helper_text_mode: "persistent"
                    size_hint: 1, .20
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .50}
                    mode: "fill"

                    icon_left: "key-variant"
                MDTextButton:
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: dp(30)
                    size_hint: .8, .17
                    pos_hint: {'center_x': .5, 'center_y': .20}
                    bold: True
                    on_press: root.check()
                    Image:
                        source: 'emias.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 362, 65
        MDSeparator:
            pos_hint: {'center_x': .435, 'center_y': .415}
            size_hint_x: .1
            color: 128/255, 128/255, 128/255
        MDLabel:
            text: "[color=#808080]ИЛИ[/color]"
            bold: True
            markup: True
            font_name: 'roboto'
            pos_hint: {'center_x': .5, 'center_y': .415}
            halign: 'center'
        MDSeparator:
            pos_hint: {'center_x': .565, 'center_y': .415}
            size_hint_x: .1
            color: 128/255, 128/255, 128/255

        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .27}
            size_hint: .2, .20
            MDRelativeLayout:
                orientation: 'horizontal'
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .30}
                    font_size: dp(25)
                    on_release: root.mos()
                    Image:
                        source: 'mos.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 358, 60
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .70}
                    font_size: dp(25)
                    on_release: root.oms()
                    Image:
                        source: 'oms.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 362, 65
                    
                
                    
    
<OMSScreen>:
    bdate: bdate
    policy: policy
    name: 'oms'
    MDFillRoundFlatButton:
        text: "На экран авторизации"
        pos_hint: {'center_x': .1, 'center_y': .92}
        font_name: 'roboto'
        font_size: dp(30)
        size_hint_y: .1
        md_bg_color: 0/255, 106/255, 240/255
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .65}
            size_hint: .2, .4
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDLabel:
                    text: "Вход по полису ОМС:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: policy
                    hint_text: "Номер полиса"
                    mode: "fill"
                    max_text_length: 16
                    min_text_length: 16
                    font_size: dp(30)
                    input_filter: 'int'
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "Например, 7100 0000 0000 0000"
                    icon_left: "account-details"
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, .20
                    font_size: dp(25)
                    on_release: root.datepicker()
                MDTextField:
                    id: bdate
                    hint_text: "Дата Рождения"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, .20
                    disabled: True
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    readonly: True
                    icon_left: "account-details"


                MDFillRoundFlatButton:
                    text: "Войти"
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: 45
                    size_hint: .8, .1
                    md_bg_color: 0/255, 106/255, 240/255
                    pos_hint: {'center_x': .5, 'center_y': .25}
                    bold: True
                    on_release: Thread(target = root.omslogin()).start()
                MDLabel:
                    text: "[color=#808080]Авторизируясь по полису[/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .10}
                MDLabel:
                    text: "[color=#808080]будет доступен не полный функционал:[/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .06}
                MDIconButton:
                    icon: "help"
                    pos_hint: {'center_x': .87, 'center_y': .075}
                    md_bg_color: 0/255, 106/255, 240/255
                    theme_icon_color: "Custom"
                    icon_color: 1,1,1,1
                    on_release: root.show_alert_dialog_info()
        
<MOSScreen>:
    name: 'mos'
    bdatemos: bdatemos
    policy: policy
    email: email_input
    password: text_field
    MDFillRoundFlatButton:
        text: "На экран авторизации"
        pos_hint: {'center_x': .1, 'center_y': .92}
        font_name: 'roboto'
        font_size: dp(30)
        size_hint_y: .1
        md_bg_color: 0/255, 106/255, 240/255
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .50}
            size_hint: .2, .7
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDTextField:
                    id: policy
                    hint_text: "Номер полиса(необязательно)"
                    mode: "fill"
                    max_text_length: 16
                    font_size: dp(30)
                    input_filter: 'int'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "Например, 7100 0000 0000 0000"
                    icon_left: "account-details"
                MDTextButton:
                    size_hint: 1, .1
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .35}
                    font_size: dp(25)
                    on_release: root.datepicker()
                MDTextField:
                    id: bdatemos
                    hint_text: "Дата Рождения(необязательно)"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .35}
                    disabled: True
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    readonly: True
                    icon_left: "account-details"
                MDLabel:
                    text: "[color=#808080]Без полиса и даты рождения [/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .10}

                MDLabel:
                    text: "[color=#808080]будет доступен не весь функционал:[/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .07}

                MDLabel:
                    text: "Войти через MOS.RU:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: email_input
                    hint_text: "Телефон, электронная почта или СНИЛС"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .8}

                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(30)
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .65}
                    mode: "fill"

                    icon_left: "key-variant"
                MDTextButton:
                    size_hint: .8, .17
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .20}
                    font_size: dp(25)
                    on_release: root.mobile()
                    Image:
                        source: 'mos.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 358, 60
                MDIconButton:
                    icon: "help"
                    pos_hint: {'center_x': .85, 'center_y': .088}
                    md_bg_color: 0/255, 106/255, 240/255
                    theme_icon_color: "Custom"
                    icon_color: 1,1,1,1
                    on_release: root.show_alert_dialog()
        
<OMSLoged>:
    name: 'loged'
    MDFillRoundFlatButton:
        id: curuser
        bold: True
        markup: True
        icon_color: 1, 0,0,1
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .92}
        font_size: dp(30)
        size_hint: .2,.05
        ripple_scale: 0
        right_icon: "delete"
        md_bg_color: 0/255, 106/255, 240/255
        bold: True
    MDFillRoundFlatIconButton:
        text: "Выйти"
        bold: True
        icon: "delete"
        markup: True
        icon_color: 1, 0,0,1
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .80}
        font_size: dp(30)
        size_hint: .2,.05
        right_icon: "delete"
        md_bg_color: 0/255, 106/255, 240/255
        on_release: root.exits()
        ripple_color: 1, 1, 1, 1
        bold: True
    MDFillRoundFlatButton:
        text: "Войти в полную версию"
        bold: True
        markup: True
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .86}
        font_size: dp(30)
        size_hint: .2,.05
        md_bg_color: 0/255, 106/255, 240/255
        on_release: root.moslogin()
        ripple_color: 1, 1, 1, 1
        bold: True
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .35, 'center_y': .65}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("ЖАЛОБА")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Запись к врачу"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .35, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]Запись[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Просмотр записей[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Перенос записей[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Рецепты[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
                halign: 'center'
            

    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .65, 'center_y': .65}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("Запись")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Справки"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]COVID - 19[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Освобождение от[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .70, 'center_y': .42}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]посещения учреждений[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .70, 'center_y': .35}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Медосмотр[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Перенесенное заболевание[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .70, 'center_y': .20}
                halign: 'center'
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .35, 'center_y': .30}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("ЖАЛОБА")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Первичный прием"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .40, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]Простуда[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Болезни кожи AI[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Болезни горла AI[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Давление/Пульс/ЭКГ AI[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
                halign: 'center'
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .65, 'center_y': .30}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("Запись")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Медкарта"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .35, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]История визитов[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Результаты исследований[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Результаты анализова[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Поиск отклонений[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
                halign: 'center'
        
<Item>
    orientation: "horizontal"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    MDTextField:
        id: verif1
        helper_text_mode: "persistent"
        font_name: 'roboto'
        on_text: verif2.focus = True
        size_hint: .1, .5
        max_text_length: 1
        pos_hint: {'center_x': .15, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif2
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif3.focus = True
        pos_hint: {'center_x': .30, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif3
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif4.focus = True
        pos_hint: {'center_x': .45, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif4
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif5.focus = True
        pos_hint: {'center_x': .60, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif5
        helper_text_mode: "persistent"
        font_name: 'roboto'
        max_text_length: 1
        on_text: verif6.focus = True
        size_hint: .1, .5
        pos_hint: {'center_x': .75, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif6
        size_hint: .1, .5
        max_text_length: 1
        helper_text_mode: "persistent"
        font_name: 'roboto'
        pos_hint: {'center_x': .90, 'center_y': .65}
        mode: "fill"


        
'''

class Item(RelativeLayout):
    pass



class ENTERScreen(Screen):
    def check(self):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if self.email.text != "" and re.match(pattern, self.email.text) is not None:
            self.email.helper_text_color_normal = 'white'
            self.email.helper_text_color_focus = 'white'
            self.email.helper_text = ""
            if len(self.password.text)>=8:
                self.password.helper_text_color_normal = 'white'
                self.password.helper_text_color_focus = 'white'
                #вход в emias по логину паролю
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = 'red'
                self.password.helper_text_color_focus = 'red'
        else:
            self.email.helper_text = "Введите корректный Email!"
            self.email.helper_text_color_normal = 'red'
            self.email.helper_text_color_focus = 'red'

    def oms(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = 'oms'

    def mos(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = 'mos'


    pass
class OMSScreen(Screen):
    dialog = None
    dialogs = None
    def back(self):
        self.manager.current = 'enter'
    def datepicker(self):
        self.date = AKDatePicker(callback=self.callback, opposite_colors='ffffff')
        self.date.open()
    def callback(self, date):
        global day, month, year
        try:
            year = str(date.year)
            if len(str(date.day))>1:
                day = str(date.day)
            else:
                day = "0"+str(date.day)
            if len(str(date.month))>1:
                month = str(date.month)
            else:
                month = "0"+str(date.month)
            self.bdate.text = day+"."+ month +"."+year
        except:
            None
            
    def omslogin(self):
        async def omslogin():
            if len(self.policy.text)<16 or len(self.policy.text)>16:
                self.policy.helper_text = "Некорректный полис"
                self.policy.helper_text_color_normal = 'red'
                self.policy.helper_text_color_focus = 'red'
            elif self.bdate.text != "":
                self.policy.helper_text = ""
                try:
                    options = webdriver.ChromeOptions()
                    options.add_argument("headless")
                    driver = webdriver.Chrome(
                        executable_path="chromedriver.exe",
                        options=options
                    )
                    driver.get("https://emias.info/")
                    driver.implicitly_wait(30)
                    police_input = driver.find_element(By.NAME, 'policy')
                    police_input.send_keys(self.policy.text)
                    day_input = driver.find_element(By.NAME, 'day')
                    day_input.send_keys(day) 
                    month_input = driver.find_element(By.NAME, 'month')
                    month_input.send_keys(month) 
                    year_input = driver.find_element(By.NAME, 'year')
                    year_input.send_keys(year)
                    login_button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div/div/div/form/button").click() 
                    element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/header/div/div[2]/div[2]/div/button/div/div'))
                    page = WebDriverWait(driver, 10).until(element_present)
                    self.manager.get_screen('oms').ids.policy.text = ""
                    self.manager.get_screen('oms').ids.bdate.text = ""
                    try:
                        check = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div[1]/div[1]/a[1]").click() 
                        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div[2]/div[2]/div/div[2]/div/div[3]'))
                        page = WebDriverWait(driver, 10).until(element_present)
                        error = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div[2]/div[2]/div/div[2]/div/div[3]').text
                        self.show_alert_dialog()
                    except:
                        global curuserid 
                        curuserid = driver.find_element(By.XPATH, '/html/body/div[2]/header/div/div[2]/div[2]/div/button/div/div').text
                        self.manager.get_screen('loged').ids.curuser.text = ("Полис: "+ curuserid)
                        self.manager.current = "loged"


                finally:
                    driver.close()
                    driver.quit()
            else:
                self.bdate.helper_text = "Введите дату"
                self.bdate.helper_text_color_normal = 'red'
                self.bdate.helper_text_color_focus = 'red'
        asynckivy.start(omslogin())
    def exits(self):
        self.manager.current = 'enter'
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Пациент не найден",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()
    
    def show_alert_dialog_info(self):
        if not self.dialogs:
            self.dialogs = MDDialog(
                text="При входе только по ОМС вам будет не доступно: первичный осмотр с использованием AI, анализ медкарты и т.д. Будет доступно: Запись по направлению, запись к врачу, рецепты, перенос. Чтобы воспользоваться полной версией, войдите через mos.ru",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogs.dismiss()
                    )
                ],
            )
        self.dialogs.open()

    pass


class MOSScreen(Screen):
    dialogs = None
    dialog = None
    dialogerror = None
    mobiles = None
    def back(self):
        self.manager.current = 'enter'
    def datepicker(self):
        self.date = AKDatePicker(callback=self.callback, opposite_colors='ffffff')
        self.date.open()
    def callback(self, date):
        global day, month, year
        try:
            year = str(date.year)
            if len(str(date.day))>1:
                day = str(date.day)
            else:
                day = "0"+str(date.day)
            if len(str(date.month))>1:
                month = str(date.month)
            else:
                month = "0"+str(date.month)
            self.bdatemos.text = day+"."+ month +"."+year
        except:
            None
    def show_alert_dialog(self):
        if not self.dialogs:
            self.dialogs = MDDialog(
                text="Без полиса и даты рождения вам будет не доступно: запись по направлению, запись к врачу ",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogs.dismiss()
                    )
                ],
            )
        self.dialogs.open()
    
    def error_dialog(self):
        if not self.dialogerror:
            self.dialogerror = MDDialog(
                text="Введен некорректный логин или пароль. Телефон может быть введен в любом формате, например, +79991234567. СНИЛС должен быть указан в виде последовательности цифр через дефисы или без разделителей. Электронная почта должна содержать символ @. ",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogerror.dismiss()
                    )
                ],
            )
        self.dialogerror.open()

    def mobile(self):
        global verifcode
        def use_input(obj):
            if self.mobiles.content_cls.ids.verif1.text =="" or  self.mobiles.content_cls.ids.verif2.text == "" or  self.mobiles.content_cls.ids.verif3.text == "" or self.mobiles.content_cls.ids.verif4.text == "" or self.mobiles.content_cls.ids.verif5.text == "" or self.mobiles.content_cls.ids.verif6.text =="" or len(self.mobiles.content_cls.ids.verif1.text + self.mobiles.content_cls.ids.verif2.text + self.mobiles.content_cls.ids.verif3.text + self.mobiles.content_cls.ids.verif4.text + self.mobiles.content_cls.ids.verif5.text + self.mobiles.content_cls.ids.verif6.text)>6:
                print("Код не введен")
            else:
                verifcode = self.mobiles.content_cls.ids.verif1.text + self.mobiles.content_cls.ids.verif2.text + self.mobiles.content_cls.ids.verif3.text + self.mobiles.content_cls.ids.verif4.text + self.mobiles.content_cls.ids.verif5.text + self.mobiles.content_cls.ids.verif6.text
                self.mobiles.dismiss()
                print(verifcode)

        if not self.mobiles:
            self.mobiles = MDDialog(
                title="Введите СМС КОД",
                type="custom",
                content_cls=Item(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Ввести",
                        on_release=use_input
                        
                    )
                ],
            )
        self.mobiles.open()

    
        


    def check(self):
        global curuserid, verifcode
        if self.email.text != "":
            self.email.helper_text_color_normal = 'white'
            self.email.helper_text_color_focus = 'white'
            self.email.helper_text = ""
            if len(self.password.text)>=8:
                self.password.helper_text_color_normal = 'white'
                self.password.helper_text_color_focus = 'white'
                if self.policy.text=="" and self.bdatemos.text == "":
                    #ВХОД ТОЛЬКО ЧЕРЕЗ MOS.RU
                    options = webdriver.ChromeOptions()
                    #options.add_argument("headless")
                    driver = webdriver.Chrome(
                        executable_path="chromedriver.exe",
                        options=options
                    )
                    driver.get("https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
                    driver.implicitly_wait(30)
                    loginmos = driver.find_element(By.NAME, 'login')
                    loginmos.send_keys(self.email.text)
                    passwordmos = driver.find_element(By.NAME, 'password')
                    passwordmos.send_keys(self.password.text)
                    login_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
                    try:
                        error = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text    
                        self.error_dialog()
                        driver.quit
                    except:
                        self.mobile()
                        while verifcode == None:
                            None
                        else:
                            print("код введен")
                        

                        



                    
                elif self.policy.text!="" or self.bdatemos.text != "":
                    if len(self.policy.text)<16 or len(self.policy.text)>16:
                        self.policy.helper_text = "Некорректный полис"
                        self.policy.helper_text_color_normal = 'red'
                        self.policy.helper_text_color_focus = 'red'
                    elif self.bdatemos.text == "":
                        self.bdatemos.helper_text = "Введите дату"
                        self.bdatemos.helper_text_color_normal = 'red'
                        self.bdatemos.helper_text_color_focus = 'red'
                        self.policy.helper_text = ""
                    else:
                        #ВХОД С ПОЛИСОМ И МОС РУ
                        self.bdatemos.helper_text = ""
                        
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = 'red'
                self.password.helper_text_color_focus = 'red'
        else:
            self.email.helper_text = "Введите телефон, электронная почта или СНИЛС "
            self.email.helper_text_color_normal = 'red'
            self.email.helper_text_color_focus = 'red'


class OMSLoged(Screen):
    def moslogin(self):
        self.manager.current = 'omsmos'
    def exits(self):
        self.manager.get_screen('oms').ids.policy.text = ""
        self.manager.get_screen('oms').ids.bdate.text = ""
        self.manager.current = 'enter'
        global day
        global year
        global month
        day  = None
        year = None
        month = None



    pass



class AlterApp(MDApp):
    def build(self):
        global day
        global year
        global month, verifcode
        day  = None
        year = None
        month = None
        verifcode = None
        sm = ScreenManager()
        sm.add_widget(ENTERScreen(name='enter'))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(MOSScreen(name="mos"))
        sm.add_widget(OMSLoged(name="loged"))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


AlterApp().run()
# 5494499745000410
