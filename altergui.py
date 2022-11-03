import re
import sys
import time
from kivy.properties import DictProperty
from kivy.clock import Clock
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
from kivymd.uix.list import OneLineListItem
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options


from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RoundedRectangularElevationBehavior,
)

# Window.fullscreen = True
Window.size = (1920, 1080)
# Window.maximize()


KV = """
ScreenManager:
    ENTERScreen:
    OMSScreen:
    ZapisScreen:
    MOSScreen:
    OMSLoged:
    MOSLoged:
    Loading:
    Loadingoms:
    Vrach:
    TimeScreen:
<ENTERScreen>:
    name: 'enter'
    email: email_input
    password: text_field
    Image:
        source: 'bg.png'
        allow_stretch: True
        keep_ratio: False
    RelativeLayout:
        MDCard:
            orientation: "vertical"
            pos_hint: {'center_x': 0.5, 'center_y': .57}
            size_hint: .2, .4
            radius:[30]
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDLabel:
                    text: "[color=#ffffff]ВОЙТИ ЧЕРЕЗ EMIAS:[/color]"
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
        MDLabel:
            text: "[color=#ffffff]ИЛИ[/color]"
            bold: True
            markup: True
            font_size: dp(28)
            font_name: 'roboto'
            pos_hint: {'center_x': .5, 'center_y': .33}
            halign: 'center'
        MDCard:
            orientation: "vertical"
            radius:[30]
            pos_hint: {'center_x': 0.5, 'center_y': .19}
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
    Image:
        source: 'omsbg.png'
        allow_stretch: True
        keep_ratio: False
    MDFillRoundFlatButton:
        text: '< Назад'
        markup: True
        pos_hint: {'center_x': .626, 'center_y': .2}
        font_name: 'roboto'
        font_size: dp(40)
        size_hint: .2,.1
        md_bg_color: 0/255, 106/255, 240/255, .4
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            pos_hint: {'center_x': .626, 'center_y': .5}
            size_hint: .2, .4
            radius:[30]
            md_bg_color: 0/255, 106/255, 240/255, .4
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDTextField:
                    id: policy
                    hint_text: "Номер полиса"
                    mode: "fill"
                    fill_color_normal: 0/255, 106/255, 240/255, .4
                    max_text_length: 16
                    hint_text_color_normal: "white"
                    helper_text_color_normal: "white"
                    helper_text_color_focus: 'white'
                    icon_left_color_normal: 'white'
                    max_length_text_color: 'white'
                    helper_text: 'Например 7700 0000 0000 0000'
                    min_text_length: 16
                    text_color_normal: "white"
                    font_size: dp(30)
                    input_filter: 'int'
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    md_bg_color: 0/255, 106/255, 240/255, .4
                    icon_left: "account-details"
                MDTextField:
                    id: bdate
                    hint_text: "Выберите дату рождения"
                    fill_color_normal: 0/255, 106/255, 240/255, .4
                    hint_text_color_normal: "white"
                    helper_text_color_normal: "white"
                    text_color_normal: "white"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    readonly: True
                    icon_left: "calendar"
                MDIcon:
                    icon: "calendar"
                    pos_hint: {'center_x': .079, 'center_y': .5}
                    color: 'white'
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, .20
                    font_size: dp(25)
                    on_release: root.datepicker()
                MDFillRoundFlatButton:
                    text: "Войти"
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: 45
                    size_hint: .8, .1
                    md_bg_color: 0/255, 106/255, 240/255, .4
                    pos_hint: {'center_x': .5, 'center_y': .25}
                    bold: True
                    on_release: root.omslogin()
                MDLabel:
                    text: "[color=#ffffff]Авторизируясь по полису[/color]"
                    bold: True
                    font_size: 15
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .51, 'center_y': .10}
                MDLabel:
                    text: "[color=#ffffff]будет доступен не полный функционал[/color]"
                    bold: True
                    font_size: 15
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .51, 'center_y': .06}
                MDIconButton:
                    icon: "help"
                    pos_hint: {'center_x': .9, 'center_y': .075}
                    md_bg_color: 0/255, 106/255, 240/255, .4
                    theme_icon_color: "Custom"
                    icon_color: 1,1,1,1
                    on_release: root.show_alert_dialog_info()
        
<MOSScreen>:
    name: 'mos'
    email: email_input
    password: text_field
    Image:
        source: 'mosbg.png'
        allow_stretch: True
        keep_ratio: False
    MDFillRoundFlatButton:
        text: '< Назад'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .2}
        font_name: 'roboto'
        font_size: dp(40)
        size_hint: .2,.1
        md_bg_color: 255/255, 255/255, 255/255, .3
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            pos_hint: {'center_x': 0.6, 'center_y': .5}
            size_hint: .2, .37
            radius:[30]
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
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
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .2}
                    font_size: dp(25)
                    on_release: root.check()
                    Image:
                        source: 'mos.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 358, 60

<OMSLoged>:
    name: 'loged'
    MDCard:
        orientation: "vertical"
        pos_hint: {'center_x': .88, 'center_y': .85}
        size_hint: .2, .18
        ripple_behaviour: True
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                id: authname
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .5, 'center_y': .81}
                font_size: dp(30)
                size_hint:.97, .3
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
                pos_hint: {'center_x': .5, 'center_y': .19}
                font_size: dp(30)
                right_icon: "delete"
                size_hint:.97, .3
                md_bg_color: 0/255, 106/255, 240/255
                on_release: root.exits()
                ripple_color: 1, 1, 1, 1
                bold: True
            MDFillRoundFlatButton:
                id: full
                text: "Войти в полную версию"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .5, 'center_y': .50}
                size_hint: .97, .3
                font_size: dp(27)
                md_bg_color: 0/255, 106/255, 240/255
                on_release: root.manager.current = "mos"
                ripple_color: 1, 1, 1, 1
                bold: True
    MDCard:
        orientation: "vertical"
        pos_hint: {'center_x': .30, 'center_y': .75}
        size_hint: .2, .3
        ripple_behaviour: True
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Запись к врачу"
                font_name: 'roboto'
                on_release: root.vrach()
                pos_hint: {'center_x': .25, 'center_y': .40}
            MDFillRoundFlatButton:
                text: "Просмотр записей"
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
            MDFillRoundFlatButton:
                text: "Просмотр направлений"
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
            MDFillRoundFlatButton:
                text: "Прикрепления"
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
<MOSLoged>:
    name: 'mosloged'
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .925, 'center_y': .84}
        size_hint: .14, .3
        ripple_behaviour: True
        MDLabel:
            id: authname
            text: 'Имя'
            bold: True
            markup: True
            font_size: dp(30)
            font_name: 'roboto'
            halign: 'center'
        MDLabel:
            id: curuser
            text: 'Фамилия'
            bold: True
            markup: True
            multiline: True
            font_size: dp(30)
            font_name: 'roboto'
            halign: 'center'
        MDLabel:
            id: males
            text: 'Пол: '
            bold: True
            markup: True
            font_size: dp(30)
            font_name: 'roboto'
            halign: 'center'
        MDLabel:
            id: ages
            text: 'Возраст'
            bold: True
            markup: True
            font_size: dp(30)
            font_name: 'roboto'
            halign: 'center'
        MDFillRoundFlatIconButton:
            text: "Выйти"
            bold: True
            icon: "delete"
            markup: True
            icon_color: 1, 0,0,1
            font_name: 'roboto'
            font_size: dp(30)
            right_icon: "delete"
            md_bg_color: 0/255, 106/255, 240/255
            on_release: root.exits()
            ripple_color: 1, 1, 1, 1
            bold: True

    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .30, 'center_y': .75}
        size_hint: .2, .3
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
        pos_hint: {'center_x': .60, 'center_y': .75}
        size_hint: .2, .3
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
        pos_hint: {'center_x': .30, 'center_y': .30}
        size_hint: .2, .3
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
        pos_hint: {'center_x': .60, 'center_y': .30}
        size_hint: .2, .3
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
        
<Loading>:
    name: "load"
    canvas.before:
        Color:
            rgba: 176/255,0,0, 1
        Rectangle:
            pos: self.pos
            size: self.size
    MDSpinner:
        size_hint: None, None
        size: dp(60), dp(60)
        color: 1,1,1,1
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: True 
<Loadingoms>:
    name: "loadoms"
    canvas.before:
        Color:
            rgba: 0/255, 106/255, 240/255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    MDSpinner:
        size_hint: None, None
        size: dp(60), dp(60)
        color: 1,1,1,1
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: True 

<Item>
    id: mobiledialog
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
        pos_hint: {'center_x': .10, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif2
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif3.focus = True
        pos_hint: {'center_x': .28, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif3
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif4.focus = True
        pos_hint: {'center_x': .46, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif4
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif5.focus = True
        pos_hint: {'center_x': .64, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif5
        helper_text_mode: "persistent"
        font_name: 'roboto'
        max_text_length: 1
        size_hint: .1, .5
        pos_hint: {'center_x': .82, 'center_y': .65}
        mode: "fill"

<Itemerrors>
    id: mobiledialog
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
        pos_hint: {'center_x': .10, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif2
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif3.focus = True
        pos_hint: {'center_x': .28, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif3
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif4.focus = True
        pos_hint: {'center_x': .46, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif4
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif5.focus = True
        pos_hint: {'center_x': .64, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif5
        helper_text_mode: "persistent"
        font_name: 'roboto'
        max_text_length: 1
        size_hint: .1, .5
        pos_hint: {'center_x': .82, 'center_y': .65}
        mode: "fill"
<Itemwait>
    id: mobiledialog
    orientation: "horizontal"
    spacing: "12dp"
    size_hint_y: None
    height: "200dp"
    MDIcon:
        id: icons
        icon: 'alert-circle'
        font_size: 100
        pos_hint: {'center_x': .5, 'center_y': .7}
    MDLabel:
        id: timers
        text: '60'
        halign: 'center'
        font_name: 'roboto'
        font_size: dp(26)
        pos_hint: {'center_x': .85, 'center_y': .14}
    MDLabel:
        id: succ
        text: ''
        halign: 'center'
        font_name: 'roboto'
        font_size: dp(26)
        pos_hint: {'center_x': .5, 'center_y': .35}
    MDLabel:
        id: succ1
        text: ''
        halign: 'center'
        font_name: 'roboto'
        font_size: dp(26)
        pos_hint: {'center_x': .5, 'center_y': .09}
    MDLabel:
        id: labels
        text: 'Доступ разблокируется через'
        halign: 'center'
        font_name: 'roboto'
        font_size: dp(25)
        pos_hint: {'center_x': .4, 'center_y': .14}
<ZapisScreen>:
    name: 'zapis'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            id: scrollid

<Vrach>:
    name: 'vrachvibor'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            id: scrollid
<TimeScreen>:
    name: 'timevibor'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            id: scrollid
"""
class ZapisScreen(Screen):
    pass

class Item(RelativeLayout):
    pass


class Itemwait(RelativeLayout):
    pass


class Itemerrors(RelativeLayout):
    pass


# ГЛАВНЫЙ ЭКРАН
class ENTERScreen(Screen):
    def check(self):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if self.email.text != "" and re.match(pattern, self.email.text) is not None:
            self.email.helper_text_color_normal = "white"
            self.email.helper_text_color_focus = "white"
            self.email.helper_text = ""
            if len(self.password.text) >= 8:
                self.password.helper_text_color_normal = "white"
                self.password.helper_text_color_focus = "white"
                # вход в emias по логину паролю
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = "red"
                self.password.helper_text_color_focus = "red"
        else:
            self.email.helper_text = "Введите корректный Email!"
            self.email.helper_text_color_normal = "red"
            self.email.helper_text_color_focus = "red"

    def oms(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = "oms"

    def mos(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = "mos"

    pass


# ВХОД ПО ОМС
class OMSScreen(Screen):
    dialog = None
    dialog1 = None
    dialogs = None
    global result

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
        global day, month, year
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
            self.bdate.text = day + "." + month + "." + year
        except:
            None

    def omsfunc(self, policy, day, month, year):
        t = threading.Thread(
            target=self.open_omslogin, args=[policy, day, month, year], daemon=True
        )
        t.start()

    def open_omslogin(self, policy, day, month, year):
        try:
            global result, curuserid
            bdate = year + "-" + month + "-" + day
            assignment = requests.post(
                ass,
                json={
                    "jsonrpc": "2.0",
                    "id": "ULHOof43sz6OfDTK4KRf1",
                    "method": "getAssignmentsInfo",
                    "params": {"omsNumber": policy, "birthDate": bdate},
                },
            )
            jsass = assignment.json()
            specialities = requests.post(
                ass,
                json={
                    "jsonrpc": "2.0",
                    "id": "ULHOof43sz6OfDTK4KRf1",
                    "method": "getSpecialitiesInfo",
                    "params": {"omsNumber": policy, "birthDate": bdate},
                },
            )
            jsspec = specialities.json()
            if "error" in jsass or "error" in jsspec:
                result = 0
            else:
                curuserid = policy
                result = 1
        except:
            result = 666

    def omslogin(self):
        def checkglobal(*args):
            global curuserid, result, oms, bdates
            if result == None:
                None
            elif result == 0:
                result = None
                self.manager.current = "oms"
                self.show_alert_dialog()
                Clock.unschedule(clocks)
            elif result == 1:
                self.manager.current = "loged"
                self.manager.get_screen("loged").ids.authname.text = self.policy.text
                oms = self.policy.text
                bdates = year + "-" + month + "-" + day
                Clock.unschedule(clocks)
                result = None
            elif result == 666:
                result = None
                self.manager.current = "oms"
                self.show_alert_dialog1()
                Clock.unschedule(clocks)

        if len(self.policy.text) < 16 or len(self.policy.text) > 16:
            self.policy.helper_text = "Некорректный полис"
            self.policy.helper_text_color_normal = "red"
            self.policy.helper_text_color_focus = "red"
        elif self.bdate.text != "":
            self.omsfunc(self.policy.text, day, month, year)
            self.manager.current = "loadoms"
            self.bdate.helper_text = ""
            self.bdate.helper_text_color_normal = "white"
            self.bdate.helper_text_color_focus = "white"
            self.policy.helper_text_color_normal = "white"
            self.policy.helper_text = ""
            self.policy.helper_text_color_focus = "white"
            clocks = Clock.schedule_interval(checkglobal, 2)

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
                text="[color=ffffff]Произошла внутренняя ошибка повторите еще[/color]",
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


# вход через mos.ru
class MOSScreen(Screen):
    dialogerror = None
    mobiles = None
    mobileerror = None
    waiterror = None

    def back(self):
        self.manager.current = "enter"
        self.password.helper_text = ""
        self.password.helper_text_color_normal = "white"
        self.password.helper_text_color_focus = "white"
        self.email.helper_text = ""
        self.email.helper_text_color_normal = "white"
        self.email.helper_text_color_focus = "white"
        self.password.text = ""
        self.email.text = ""

    def error_dialog(self):
        if not self.dialogerror:
            self.dialogerror = MDDialog(
                text="Введен некорректный логин или пароль. Телефон может быть введен в любом формате, например, +79991234567. СНИЛС должен быть указан в виде последовательности цифр через дефисы или без разделителей. Электронная почта должна содержать символ @. ",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        md_bg_color="ff0000",
                        on_release=lambda _: self.dialogerror.dismiss(),
                    )
                ],
            )
        self.dialogerror.open()

    def mobile(self):
        def use_input(obj):
            global verifcode
            if (
                self.mobiles.content_cls.ids.verif1.text == ""
                or self.mobiles.content_cls.ids.verif2.text == ""
                or self.mobiles.content_cls.ids.verif3.text == ""
                or self.mobiles.content_cls.ids.verif4.text == ""
                or self.mobiles.content_cls.ids.verif5.text == ""
                or len(
                    self.mobiles.content_cls.ids.verif1.text
                    + self.mobiles.content_cls.ids.verif2.text
                    + self.mobiles.content_cls.ids.verif3.text
                    + self.mobiles.content_cls.ids.verif4.text
                    + self.mobiles.content_cls.ids.verif5.text
                )
                > 5
            ):
                None
            else:
                verifcode = (
                    self.mobiles.content_cls.ids.verif1.text
                    + self.mobiles.content_cls.ids.verif2.text
                    + self.mobiles.content_cls.ids.verif3.text
                    + self.mobiles.content_cls.ids.verif4.text
                    + self.mobiles.content_cls.ids.verif5.text
                )
                self.mobiles.content_cls.ids.verif1.text = ""
                self.mobiles.content_cls.ids.verif2.text = ""
                self.mobiles.content_cls.ids.verif3.text = ""
                self.mobiles.content_cls.ids.verif4.text = ""
                self.mobiles.content_cls.ids.verif5.text = ""
                self.manager.current = "load"
                self.mobiles.dismiss()

        if not self.mobiles:
            self.mobiles = MDDialog(
                title="Введите СМС КОД",
                type="custom",
                auto_dismiss=False,
                content_cls=Item(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Ввести", md_bg_color="ff0000", on_release=use_input
                    )
                ],
            )
        self.mobiles.open()

    def mobileerrors(self):
        def use_input(obj):
            global verifcode
            if (
                self.mobileerror.content_cls.ids.verif1.text == ""
                or self.mobileerror.content_cls.ids.verif2.text == ""
                or self.mobileerror.content_cls.ids.verif3.text == ""
                or self.mobileerror.content_cls.ids.verif4.text == ""
                or self.mobileerror.content_cls.ids.verif5.text == ""
                or len(
                    self.mobileerror.content_cls.ids.verif1.text
                    + self.mobileerror.content_cls.ids.verif2.text
                    + self.mobileerror.content_cls.ids.verif3.text
                    + self.mobileerror.content_cls.ids.verif4.text
                    + self.mobileerror.content_cls.ids.verif5.text
                )
                > 5
            ):
                None
            else:
                verifcode = (
                    self.mobileerror.content_cls.ids.verif1.text
                    + self.mobileerror.content_cls.ids.verif2.text
                    + self.mobileerror.content_cls.ids.verif3.text
                    + self.mobileerror.content_cls.ids.verif4.text
                    + self.mobileerror.content_cls.ids.verif5.text
                )
                self.mobileerror.content_cls.ids.verif1.text = ""
                self.mobileerror.content_cls.ids.verif2.text = ""
                self.mobileerror.content_cls.ids.verif3.text = ""
                self.mobileerror.content_cls.ids.verif4.text = ""
                self.mobileerror.content_cls.ids.verif5.text = ""
                self.manager.current = "load"
                self.mobileerror.dismiss()

        if not self.mobileerror:
            self.mobileerror = MDDialog(
                title="   Был введен неверный код",
                type="custom",
                auto_dismiss=False,
                content_cls=Itemerrors(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Ввести", md_bg_color="ff0000", on_release=use_input
                    )
                ],
            )
        self.mobileerror.open()

    def waiterrors(self):
        def use_input(obj):
            global counts
            Clock.unschedule(asyncs)
            self.waiterror.dismiss()
            counts = 59
            self.waiterror.content_cls.ids.timers.text = "59"
            self.waiterror.content_cls.ids.succ.text = ""
            self.waiterror.content_cls.ids.succ1.text = ""
            self.waiterror.content_cls.ids.icons.icon = "alert-circle"
            self.waiterror.content_cls.ids.labels.text = "Доступ разблокируется через"

        def timer(*args):
            global counts, result
            if counts == 0:
                Clock.unschedule(asyncs)
                self.waiterror.content_cls.ids.succ.text = "Доступ разблокирован"
                self.waiterror.content_cls.ids.succ1.text = (
                    "Можете поробовать авторизоваться снова снова"
                )
                self.waiterror.content_cls.ids.icons.icon = "check"
                self.waiterror.content_cls.ids.timers.text = ""
                self.waiterror.content_cls.ids.labels.text = ""
                time.sleep(2)
                counts = 59
            else:
                self.waiterror.content_cls.ids.timers.text = str(counts)
                counts -= 1

        if not self.waiterror:
            self.waiterror = MDDialog(
                title="Превышено кол-во ввода смс-кода, доступ заблокирован",
                type="custom",
                auto_dismiss=False,
                content_cls=Itemwait(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Выход", md_bg_color="ff0000", on_release=use_input
                    )
                ],
            )
        self.waiterror.open()
        asyncs = Clock.schedule_interval(timer, 1)

    def mosfunc(self, login, password):
        t = threading.Thread(
            target=self.open_moslogin, args=[login, password], daemon=True
        )
        if not t.is_alive():
            t.start()

    def open_moslogin(self, login, password):
        global verifcode, result, curuserid, polic, names, sure, male, age, idus, authtoken

        def refferals(*args):
            global verifcode, result, curuserid, polic, names, sure, male, age, idus, authtoken
            userid = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]",
                    )
                )
            )
            names = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]",
            ).text
            male = driver.find_element(By.ID, "profile_select_gender").text
            sure = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[2]",
            ).text
            age = driver.find_element(By.ID, "profile_select_birth_date").text
            idus = driver.execute_script(
                "return window.sessionStorage.getItem('profile/currentProfileId')"
            ).replace('"', "")
            authtoken = driver.execute_script(
                "return window.localStorage.getItem('patient.web.v2.accessToken')"
            ).replace('"', "")
            profdata = driver.execute_script(
                "return window.sessionStorage.getItem('profile/profileData')"
            )
            jsdata = json.loads(profdata)
            polic = jsdata["profile"]["policyNum"]
            bdate = jsdata["profile"]["birthDate"]
            s = requests.Session()
            for cookie in driver.get_cookies():
                c = {cookie["name"]: cookie["value"]}
                s.cookies.update(c)
            result = 1
            driver.quit()

        try:
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(
                executable_path="C:\\Users\\PCWORK\Desktop\\alter\AlterGUI\\geckodriver.exe",
                options=firefox_options,
            )
            driver.get(
                "https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth"
            )
            element = WebDriverWait(driver, 120).until(
                EC.element_to_be_clickable((By.ID, "login"))
            )
            loginmos = driver.find_element(By.NAME, "login")
            loginmos.send_keys(login)
            passwordmos = driver.find_element(By.NAME, "password")
            passwordmos.send_keys(password)
            login_button = driver.find_element(
                By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button"
            ).click()
            try:
                error = driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a",
                ).text
                result = 0
                driver.quit()
            except:
                c = 0
                flag = False
                elements = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "otp_input"))
                )
                usercode = driver.find_element(By.ID, "otp_input")
                result = 2
                while verifcode == None:
                    None
                else:
                    usercode.send_keys(verifcode)
                    time.sleep(5)
                    if driver.current_url == "https://lk.emias.mos.ru/":
                        result = 3
                        verifcode = None
                        while verifcode == None:
                            None
                        else:
                            usercode.send_keys(verifcode)
                            time.sleep(5)
                            if driver.current_url == "https://lk.emias.mos.ru/":
                                result = 3
                                verifcode = None
                                while verifcode == None:
                                    None
                                else:
                                    usercode.send_keys(verifcode)
                                    time.sleep(5)
                                    if driver.current_url == "https://lk.emias.mos.ru/":
                                        result = 4
                                        verifcode = None
                                        driver.quit()
                                    else:
                                        refferals()
                            else:
                                refferals()
                    else:
                        refferals()
        except:
            result = 0
        driver.quit()
        sys.exit()

    def check(self):
        global login, password

        def checkglobal(*args):
            global verifcode, result, curuserid, polic, names, surename, male, age, idus, authtoken
            if result == None:
                None
            elif result == 0:
                self.error_dialog()
                self.manager.current = "mos"
                result = None
                Clock.unschedule(vclocks)
            elif result == 1:
                self.manager.current = "mosloged"
                result = None
                self.manager.get_screen("mosloged").ids.authname.text = names
                self.manager.get_screen("mosloged").ids.curuser.text = " "
                self.manager.get_screen("mosloged").ids.males.text = male
                self.manager.get_screen("mosloged").ids.ages.text = age
                Clock.unschedule(vclocks)
            elif result == 2:
                self.mobile()
                self.manager.current = "mos"
                result = None
            elif result == 3:
                self.mobileerrors()
                result = None
                self.manager.current = "mos"
            elif result == 4:
                self.waiterrors()
                self.manager.current = "mos"
                result = None
                Clock.unschedule(vclocks)

        if self.email.text != "":
            if len(self.password.text) >= 8:
                login = self.email.text
                password = self.password.text
                self.password.helper_text = ""
                self.password.helper_text_color_normal = "white"
                self.password.helper_text_color_focus = "white"
                self.email.helper_text = ""
                self.email.helper_text_color_normal = "white"
                self.email.helper_text_color_focus = "white"
                self.mosfunc(login, password)
                self.manager.current = "load"
                vclocks = Clock.schedule_interval(checkglobal, 2)
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = "red"
                self.password.helper_text_color_focus = "red"
                self.email.helper_text = ""
                self.email.helper_text_color_normal = "white"
                self.email.helper_text_color_focus = "white"
        else:
            self.email.helper_text = "Введите телефон, электронную почта или СНИЛС "
            self.email.helper_text_color_normal = "red"
            self.email.helper_text_color_focus = "red"


# Страница после авторизации
class MOSLoged(Screen):
    def exits(self):
        self.manager.current = "enter"
        global day, year, month, verifcode, login, password, result, polic
        day = None
        year = None
        month = None
        verifcode = None
        login = None
        password = None
        result = None
        polic = None

    pass


class OMSLoged(Screen):
    def timechoose(self, docvibor):
        global timechooses, docid, result
        assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsass = assignment.json()
        specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspec = specialities.json()
        userid = jsass["id"]
        specId = jsspec['result'][docid]["code"]
        zapis = requests.post(speclist, json = {"jsonrpc":"2.0","id":userid,"method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"specialityId": specId}})
        jszapis = zapis.json()
        timechooses = []
        docchoose = jszapis['result'][docvibor]["id"]
        for i in range(len(jszapis["result"])):
            if jszapis['result'][i]["id"] == docchoose:
                for j in range(len(jszapis["result"][i]['complexResource'])):
                    if 'room' in jszapis["result"][i]['complexResource'][j]:
                        resid = jszapis["result"][i]['complexResource'][j]['id']
        proczapis = requests.post(datespec, json = {"jsonrpc":"2.0","id":"7g9bgvEa8VkCd6A2XHJ7p","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdates,"availableResourceId":docchoose,"complexResourceId":resid,"specialityId":"11"}})
        jsproczapis = proczapis.json()
        for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
            timechooses.append(jsproczapis["result"]['scheduleOfDay'][i]["date"])
        if len(timechooses) == 0:
            result = 0
        else:
            result = 1
        print(result)
    def showdate(self, instance):
        def checkglobal(*args):
            global result, timechooses
            if result == None:
                None
            elif result ==0:
                Clock.unschedule(zapisclockss)
                result = None
                f_nextButton = MDFillRoundFlatButton(
                        text="Запись к этому доктору не доступна", md_bg_color="blue"
                        )
                self.manager.get_screen("timevibor").ids.scrollid.add_widget(f_nextButton)
            else:
                Clock.unschedule(zapisclockss)
                result = None
                for i in range(len(timechooses)):
                    f_nextButton = MDFillRoundFlatButton(
                            text=timechooses[i], md_bg_color="blue"
                            )
                    f_nextButton.bind(on_press=self.showdate)
                    self.manager.get_screen("timevibor").ids.scrollid.add_widget(f_nextButton)
            print(result)
        global vrachchoose
        docvibor = vrachchoose.index(instance.text)
        t = threading.Thread(
            target=self.timechoose, args=[docvibor], daemon=True
        )
        if not t.is_alive():
            t.start()
        self.manager.current = 'timevibor'
        zapisclockss = Clock.schedule_interval(checkglobal, 2)
    def Press_auth(self,instance):
        def checkglobal(*args):
            global result, doclist, vrachchoose
            if result == None:
                None
            elif result == 2:
                Clock.unschedule(zapisclocks)
                result = None
                f_nextButton = MDFillRoundFlatButton(
                        text="Запись не доступна", md_bg_color="blue"
                        )
                self.manager.get_screen("vrachvibor").ids.scrollid.add_widget(f_nextButton)
            else:
                Clock.unschedule(zapisclocks)
                result = None
                for i in range(len(vrachchoose)):
                    f_nextButton = MDFillRoundFlatButton(
                            text=vrachchoose[i], md_bg_color="blue"
                            )
                    f_nextButton.bind(on_press=self.showdate)
                    self.manager.get_screen("vrachvibor").ids.scrollid.add_widget(f_nextButton)
        global doclist, docid   
        docid = doclist.index(instance.text)
        t = threading.Thread(
            target=self.docchoose, daemon=True
        )
        if not t.is_alive():
            t.start()
        self.manager.current = 'vrachvibor'
        zapisclocks = Clock.schedule_interval(checkglobal, 2)

    def docchoose(self):
        global oms, bdates, doclist, result, vrachchoose, docid
        count = 0
        assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsass = assignment.json()
        specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspec = specialities.json()
        userid = jsass["id"]
        specId = jsspec['result'][docid]["code"]
        zapis = requests.post(speclist, json = {"jsonrpc":"2.0","id":userid,"method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"specialityId": specId}})
        jszapis = zapis.json()
        vrachchoose = []
        for i in range(len(jszapis["result"])):
            for j in range(len(jszapis["result"][i]['complexResource'])):
                if 'room' in jszapis["result"][i]['complexResource'][j]:
                    receptionTypeId = jszapis["result"][i]['receptionType'][0]['code']
                    count+=1
        if count == 0:
            result = 2
        else:
            for i in range(len(jszapis["result"])):
                for j in range(len(jszapis["result"][i]['complexResource'])):
                    if 'room' in jszapis["result"][i]['complexResource'][j]:
                        vrachchoose.append(jszapis['result'][i]["name"])
            result = 1
    def exits(self):
        self.manager.current = "enter"
        global day, year, month, verifcode, login, password, result, polic
        day = None
        year = None
        month = None
        verifcode = None
        login = None
        password = None
        result = None
        polic = None
    def vrach(self):
        def checkglobal(*args):
            global result, doclist
            if result == None:
                None
            else:
                Clock.unschedule(zapisclock)
                result = None
                for i in range(len(doclist)):
                    f_nextButton = MDFillRoundFlatButton(
                            text=doclist[i], md_bg_color="blue"
                            )
                    f_nextButton.bind(on_press=self.Press_auth)
                    self.manager.get_screen("zapis").ids.scrollid.add_widget(f_nextButton)

        t = threading.Thread(
            target=self.vrachs, args=[], daemon=True
        )
        if not t.is_alive():
            t.start()
        self.manager.current = 'zapis'
        zapisclock = Clock.schedule_interval(checkglobal, 2)

    def vrachs(self):
        global oms, bdates, doclist, result
        assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsass = assignment.json()
        specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspec = specialities.json()
        userid = jsass["id"]
        doclist = []
        for i in range(len(jsspec["result"])):
            doclist.append(jsspec['result'][i]["name"])
        result = 1
        
class Loading(Screen):
    pass


class Loadingoms(Screen):
    pass
class Vrach(Screen):
    pass
class TimeScreen(Screen):
    pass
class AlterApp(MDApp):
    def build(self):
        global day, year, month, verifcode, login, docid, password, result, curuserid, polic, names, sure, male, age, idus, authtoken, counts, oms, bdates, ref, ass, spec, doclist,vrachchoose, speclist, datespec, create, cancel, shift, info, timechooses
        day = None
        counts = 59
        year = None
        month = None
        verifcode = None
        login = None
        password = None
        bdates = None
        result = None
        polic = None
        curuserid = None
        names = None
        sure = None
        male = None
        age = None
        idus = None
        authtoken = None
        timechooses = None
        docid = None
        ref = "https://emias.info/api/emc/appointment-eip/v1/?getReferralsInfo"
        ass = "https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo"
        spec = "https://emias.info/api/emc/appointment-eip/v1/?getSpecialitiesInfo"
        doclist = "https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient"
        speclist = "https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo"
        datespec = "https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo"
        create = "https://emias.info/api/emc/appointment-eip/v1/?createAppointment"
        cancel = "https://emias.info/api/emc/appointment-eip/v1/?cancelAppointment"
        shift = "https://emias.info/api/emc/appointment-eip/v1/?shiftAppointment"
        info = "https://emias.info/api/emc/appointment-eip/v1/?getPatientInfo3"
        doclist = None
        vrachchoose = None

        sm = ScreenManager()
        sm.add_widget(ENTERScreen(name="enter"))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(ZapisScreen(name="zapis"))
        sm.add_widget(MOSScreen(name="mos"))
        sm.add_widget(OMSLoged(name="loged"))
        sm.add_widget(MOSLoged(name="mosloged"))
        sm.add_widget(Loading(name="load"))
        sm.add_widget(Vrach(name="vrachvibor"))
        sm.add_widget(TimeScreen(name="timevibor"))
        sm.add_widget(Loadingoms(name="loadoms"))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


AlterApp().run()
#5494499745000410