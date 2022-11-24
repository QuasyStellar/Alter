import re
import sys
import time
import datetime
import locale

from kivy.uix.image import Image

locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
import threading
from kivy.clock import Clock, mainthread
from fake_useragent import UserAgent
from html2image import Html2Image
from cairosvg import svg2png
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
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
from kivymd.uix.card import MDCard

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RoundedRectangularElevationBehavior,
)

# Window.fullscreen = True
Window.size = (1920, 1080)
# Window.maximize()


Builder.load_string("""
#: import Factory kivy.factory.Factory
<ENTERScreen>:
    name: 'enter'
    email: email_input
    password: text_field
    Image:
        source: 'assets/firstscreen/bg.png'
        allow_stretch: True
        keep_ratio: False
    RelativeLayout:
        MDCard:
            orientation: "vertical"
            pos_hint: {'center_x': 0.5, 'center_y': .55}
            size_hint: .25, .45
            radius:[30]
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDTextField:
                    id: email_input
                    hint_text: "Логин"
                    mode: "fill"
                    font_size: dp(45)
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(45)
                    helper_text_mode: "persistent"
                    size_hint: 1, .20
                    pos_hint: {'center_x': .5, 'center_y': .50}
                    mode: "fill"
                    icon_left: "key-variant"
                MDTextButton:
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: dp(30)
                    size_hint: 1, .25
                    pos_hint: {'center_x': .49, 'center_y': .20}
                    bold: True
                    ripple_color: 0,0,1,1
                    on_press: root.check()
                    Image:
                        source: 'assets/firstscreen/emias.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 450, 250
        MDLabel:
            text: "[color=#ffffff]ИЛИ[/color]"
            bold: True
            markup: True
            font_size: dp(40)
            font_name: 'roboto'
            pos_hint: {'center_x': .5, 'center_y': .29}
            halign: 'center'
        MDCard:
            orientation: "vertical"
            radius:[30]
            pos_hint: {'center_x': 0.5, 'center_y': .15}
            size_hint: .25, .20
            MDRelativeLayout:
                orientation: 'horizontal'
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .30}
                    font_size: dp(25)
                    on_release: root.mos()
                    Image:
                        source: 'assets/firstscreen/mos.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        allow_stretch: True
                        size: 450, 100
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .70}
                    font_size: dp(25)
                    on_release: root.oms()
                    Image:
                        source: 'assets/firstscreen/oms.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        allow_stretch: True
                        size: 450, 100
<OMSScreen>:
    bdate: bdate
    policy: policy
    name: 'oms'
    Image:
        source: 'assets/omsscreen/omsbg.png'
        allow_stretch: True
        keep_ratio: False
    MDFillRoundFlatButton:
        text: '< Назад'
        markup: True
        pos_hint: {'center_x': .626, 'center_y': .2}
        font_name: 'roboto'
        font_size: dp(40)
        size_hint: .25,.1
        md_bg_color: 0/255, 106/255, 240/255, .4
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            pos_hint: {'center_x': .626, 'center_y': .5}
            size_hint: .25, .45
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
                    font_size: dp(40)
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
                    font_size: dp(40)
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
        source: 'assets/mosscreen/mosbg.png'
        allow_stretch: True
        keep_ratio: False
    MDFillRoundFlatButton:
        text: '< Назад'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .2}
        font_name: 'roboto'
        font_size: dp(40)
        size_hint: .25,.1
        md_bg_color: 255/255, 255/255, 255/255, .3
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            pos_hint: {'center_x': 0.6, 'center_y': .5}
            size_hint: .25, .45
            radius:[30]
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDTextField:
                    id: email_input
                    hint_text: "Логин"
                    mode: "fill"
                    font_size: dp(40)
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .22
                    helper_text_mode: "persistent"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(40)
                    helper_text_mode: "persistent"
                    size_hint: 1, .22
                    pos_hint: {'center_x': .5, 'center_y': .50}
                    mode: "fill"
                    icon_left: "key-variant"
                MDTextButton:
                    size_hint: 1, .2
                    halign: 'center'
                    pos_hint: {'center_x': .499, 'center_y': .2}
                    font_size: dp(25)
                    on_release: root.check()
                    Image:
                        source: 'assets/mosscreen/mosbutton.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        allow_stretch: True
                        size: self.parent.size
<OMSLoged>:
    name: 'loged'
    Image:
        source: 'assets/omsloged/mainmenubgoms.png'
        allow_stretch: True
        keep_ratio: False
    MDTextButton:
        size_hint: .2, .15
        halign: 'center'
        pos_hint: {'center_x': .89, 'center_y': .1}
        font_size: dp(25)
        on_release: root.exits()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    MDTextButton:
        size_hint: .2, .2
        halign: 'center'
        pos_hint: {'center_x': .89, 'center_y': .65}
        font_size: dp(25)
        on_release: root.full_dialog()
        Image:
            source: 'assets/omsloged/enterfull.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 400, 200
    MDLabel:
        id: authname
        text:'[color=#ffffff]7700 0000 0000 0000[/color]'
        markup: True
        size_hint: .2, .15
        halign: 'center'
        pos_hint: {'center_x': .89, 'center_y': .8}
        font_size: dp(35) 
    MDCard:
        orientation: "vertical"
        pos_hint: {'center_x': .5, 'center_y': .7}
        size_hint: .339, .3
        md_bg_color: 1,1,1,0
        radius: [30]
        RelativeLayout:
            Image:
                source: 'assets/omsloged/emiasmainbutton.png'
                allow_stretch: True
                size: self.parent.size
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Мои записи[/color]'
                markup: True
                pos_hint: {'center_x': .25, 'center_y': .5}
                font_name: 'roboto'
                font_size: dp(32)
                size_hint: .45,.23
                md_bg_color: 1,1,1,1
                on_release: root.zapisi()
                bold: True
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Новая запись[/color]'
                markup: True
                pos_hint: {'center_x': .25, 'center_y': .2}
                font_name: 'roboto'
                font_size: dp(32)
                size_hint: .45,.23
                md_bg_color: 1,1,1,1
                on_release: root.newzapis()
                bold: True
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Направления[/color]'
                markup: True
                pos_hint: {'center_x': .72, 'center_y': .5}
                font_name: 'roboto'
                font_size: dp(32)
                size_hint: .45,.23
                md_bg_color: 1,1,1,1
                on_release: root.prosmotrnapr()
                bold: True
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Прикрепления[/color]'
                markup: True
                pos_hint: {'center_x': .72, 'center_y': .2}
                font_name: 'roboto'
                font_size: dp(32)
                size_hint: .45,.23
                md_bg_color: 1,1,1,1
                on_release: root.prikreplenia()
                bold: True
    MDTextButton:
        orientation: "vertical"
        pos_hint: {'center_x': .5, 'center_y': .3}
        size_hint: .339, .3
        radius: [30]
        on_release: root.exits()
        Image:
            source: 'assets/omsloged/priemmainbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            size: self.parent.size
    MDLabel:
        id: time
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .7}
        font_size: dp(90)
        font_name: 'roboto'
    MDLabel:
        id: days
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .2, 'center_y': .6}
        font_size: dp(90)
        font_name: 'roboto'
        halign: 'center'
    MDLabel:
        id: months
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .5}
        font_size: dp(90)
        font_name: 'roboto'
    MDLabel:
        id: years
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .4}
        font_size: dp(90)
        font_name: 'roboto'
    MDLabel:
        id: week
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .6}
        font_size: dp(90)
        font_name: 'roboto'
<MOSLoged>:
    name: 'mosloged'
    Image:
        source: 'assets/mosloged/mainmenubgmos.png'
        allow_stretch: True
        keep_ratio: False
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release: root.exits()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    MDLabel:
        id: authname
        text:''
        markup: True
        theme_text_color: 'Custom'
        text_color: 'white'
        size_hint: .2, .15
        halign: 'center'
        pos_hint: {'center_x': .909, 'center_y': .78}
        font_size: dp(35) 
        font_name: 'roboto'
    MDLabel:
        id: sures
        text:''
        markup: True
        theme_text_color: 'Custom'
        text_color: 'white'
        size_hint: .2, .15
        halign: 'center'
        pos_hint: {'center_x': .909, 'center_y': .74}
        font_size: dp(35) 
        font_name: 'roboto'
    MDLabel:
        id: ages
        text:''
        markup: True
        size_hint: .2, .15
        halign: 'center'
        theme_text_color: 'Custom'
        text_color: 'white'
        pos_hint: {'center_x': .909, 'center_y': .70}
        font_size: dp(35) 
        font_name: 'roboto'
    MDCard:
        orientation: "vertical"
        pos_hint: {'center_x': .5, 'center_y': .8}
        size_hint: .27, .26
        radius: [30]
        md_bg_color: 0,0,0,0
        RelativeLayout:
            Image:
                source: 'assets/mosloged/emiasbutton.png'
                size: self.parent.size
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Мои записи[/color]'
                markup: True
                pos_hint: {'center_x': .27, 'center_y': .5}
                font_name: 'roboto'
                font_size: dp(25)
                size_hint: .4,.23
                md_bg_color: 1,1,1,1
                on_release: root.manager.get_screen('loged').zapisi()
                bold: True
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Новая запись[/color]'
                markup: True
                pos_hint: {'center_x': .27, 'center_y': .2}
                font_name: 'roboto'
                font_size: dp(25)
                size_hint: .4,.23
                md_bg_color: 1,1,1,1
                on_release: root.manager.get_screen('loged').newzapis()
                bold: True
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Направления[/color]'
                markup: True
                pos_hint: {'center_x': .72, 'center_y': .5}
                font_name: 'roboto'
                font_size: dp(25)
                size_hint: .4,.23
                md_bg_color: 1,1,1,1
                on_release: root.manager.get_screen('loged').prosmotrnapr()
                bold: True
            MDFillRoundFlatButton:
                text: '[color=#1959d1]Прикрепления[/color]'
                markup: True
                pos_hint: {'center_x': .72, 'center_y': .2}
                font_name: 'roboto'
                font_size: dp(25)
                size_hint: .4,.23
                md_bg_color: 1,1,1,1
                on_release: root.manager.get_screen('loged').prikreplenia()
                bold: True
    MDTextButton:
        orientation: "vertical"
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: .27, .26
        radius: [30]
        on_release: root.manager.current = "lkcard"
        Image:
            source: 'assets/mosloged/lkcardbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            size: self.parent.size
    MDTextButton:
        orientation: "vertical"
        pos_hint: {'center_x': .5, 'center_y': .2}
        size_hint: .27, .26
        radius: [30]
        on_release: root.exits()
        Image:
            source: 'assets/mosloged/priemmosbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            size: self.parent.size
    MDTextButton:
        orientation: "vertical"
        pos_hint: {'center_x': .715, 'center_y': .5}
        size_hint: .12, .25
        radius: [30]
        on_release: root.exits()
        Image:
            source: 'assets/mosloged/cardanalizbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            size: self.parent.size
    MDLabel:
        id: time
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .7}
        font_size: dp(90)
        font_name: 'roboto'
    MDLabel:
        id: days
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .2, 'center_y': .6}
        font_size: dp(90)
        font_name: 'roboto'
        halign: 'center'
    MDLabel:
        id: months
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .5}
        font_size: dp(90)
        font_name: 'roboto'
    MDLabel:
        id: years
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .4}
        font_size: dp(90)
        font_name: 'roboto'
    MDLabel:
        id: week
        bold: True
        theme_text_color: 'Custom'
        text_color: 'white'
        markup: True
        pos_hint: {'center_x': .6, 'center_y': .6}
        font_size: dp(90)
        font_name: 'roboto'
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
<Itemfactor>
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
        pos_hint: {'center_x': .05, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif2
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif3.focus = True
        pos_hint: {'center_x': .23, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif3
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif4.focus = True
        pos_hint: {'center_x': .41, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif4
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif5.focus = True
        pos_hint: {'center_x': .59, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif5
        helper_text_mode: "persistent"
        font_name: 'roboto'
        max_text_length: 1
        on_text: verif6.focus = True
        size_hint: .1, .5
        pos_hint: {'center_x': .77, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif6
        helper_text_mode: "persistent"
        font_name: 'roboto'
        max_text_length: 1
        size_hint: .1, .5
        pos_hint: {'center_x': .95, 'center_y': .65}
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
<Zapisi>:
    name: 'zapisi'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.get_screen('loged').screenback()
            root.ids.scrollid.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    ScrollView:
        size_hint: .6, .9
        md_bg_color: 1,1,1,0
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            scroll_distance: 30
            cols:1
            spacing:10 
            size_hint_y: None
            height: self.minimum_height
            id: scrollid
<Full>
    id: fulldialog
    orientation: "horizontal"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    MDLabel:
        bold: True
        theme_text_color: 'Custom'
        text_color: 'grey'
        markup: True
        pos_hint: {'center_x': .5, 'center_y': .5}
        font_size: dp(20)
        font_name: 'roboto'
        text: "Чтобы войти в полную версию необходимо авторизоваться через mos.ru. Текущая авторизация будет прервана и вы будете перенаправлены на страницу входа через mos.ru"
<Perenos>:
    name: 'perenos'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.current = 'zapisi'
            root.ids.scrollid.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    ScrollView:
        size_hint: .6, .9
        md_bg_color: 1,1,1,0
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            scroll_distance: 30
            cols:1
            spacing:10 
            size_hint_y: None
            height: self.minimum_height
            id: scrollid
<Showdate>:
    name: 'timetable'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release: root.back()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    MDCard:
        orientation: "vertical"
        pos_hint: {'center_x': .47, 'center_y': .55}
        size_hint: .7, .7
        radius: [30]
        md_bg_color: 1,1,1,1
        RelativeLayout:
            id: lay 
<Prikreplenia>:
    name: 'prik'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.get_screen('loged').screenback()
            root.ids.lay.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    MDCard:
        orientation: "vertical"
        pos_hint: {'center_x': .47, 'center_y': .55}
        size_hint: .7, .7
        radius: [30]
        md_bg_color: 1,1,1,1
        id: lay
<Napravlenia>:
    name: 'napr'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.get_screen('loged').screenback()
            root.ids.scrollid.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    ScrollView:
        size_hint: .6, .9
        md_bg_color: 1,1,1,0
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            scroll_distance: 30
            cols:1
            spacing:10 
            size_hint_y: None
            height: self.minimum_height
            id: scrollid
<LKCard>:
    name: 'lkcard'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.current = 'mosloged'
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    MDCard:
        size_hint: .6, .8
        md_bg_color: 170/255,170/255,170/255,1
        pos_hint: {'center_x': .5, 'center_y': .5}
        radius: [30]
        RelativeLayout:
            MDFillRoundFlatButton:
                id: 1
                text: "мои тесты на covid-19"
                size_hint: .35, .13
                pos_hint: {'center_x': .35, 'center_y': .8}
                font_size: dp(30)
                on_release: root.view(1)
            MDFillRoundFlatButton:
                id: 2
                text: "мои прививки"
                size_hint: .35, .13
                pos_hint: {'center_x': .70, 'center_y': .8}
                font_size: dp(30)
                on_release: root.manager.current = 'priv'
            MDFillRoundFlatButton:
                id: 3
                text: "мои приемы в поликлинике"
                size_hint: .35, .13
                pos_hint: {'center_x': .35, 'center_y': .65}
                font_size: dp(30)
                on_release: root.view(3)
            MDFillRoundFlatButton:
                id: 4
                text: "мои анализы"
                size_hint: .35, .13
                pos_hint: {'center_x': .70, 'center_y': .65}
                font_size: dp(30)
                on_release: root.view(4)
            MDFillRoundFlatButton:
                id: 5
                text: "мои исследования"
                size_hint: .35, .13
                pos_hint: {'center_x': .35, 'center_y': .5}
                font_size: dp(30)
                on_release: root.view(5)
            MDFillRoundFlatButton:
                id: 6
                text: "мои больничные"
                size_hint: .35, .13
                pos_hint: {'center_x': .70, 'center_y': .5}
                font_size: dp(30)
                on_release: root.view(6)
            MDFillRoundFlatButton:
                id: 7
                text: "мои справки и мед. заключения"
                size_hint: .35, .13
                pos_hint: {'center_x': .35, 'center_y': .35}
                font_size: dp(30)
                on_release: root.view(7)
            MDFillRoundFlatButton:
                id: 8
                text: "мои выписки из стационара"
                size_hint: .35, .13
                pos_hint: {'center_x': .70, 'center_y': .35}
                font_size: dp(30)
                on_release: root.view(8)
            MDFillRoundFlatButton:
                id: 9
                text: "мои рецепты"
                size_hint: .35, .13
                pos_hint: {'center_x': .35, 'center_y': .2}
                font_size: dp(30)
                on_release: root.view(9)
            MDFillRoundFlatButton:
                id: 10
                text: "скорая помощь"
                size_hint: .35, .13
                pos_hint: {'center_x': .70, 'center_y': .2}
                font_size: dp(30)
                on_release: root.view(10)
<History>:
    name: 'history'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.current = 'lkcard'
            root.ids.scrollid.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    ScrollView:
        size_hint: .6, .9
        md_bg_color: 1,1,1,0
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            scroll_distance: 30
            cols:1
            spacing:10 
            size_hint_y: None
            height: self.minimum_height
            id: scrollid
<AnamnesView>
    name: 'anamn'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.current = 'history'
            root.ids.scrollid.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    ScrollView:
        size_hint: .6, .9
        md_bg_color: 1,1,1,0
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            scroll_distance: 30
            cols:1
            spacing:10 
            size_hint_y: None
            height: self.minimum_height
            id: scrollid
<Privivki>:
    name: 'priv'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.current = 'lkcard'
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    MDCard:
        size_hint: .8, .8
        md_bg_color: 170/255,170/255,170/255,1
        pos_hint: {'center_x': .5, 'center_y': .5}
        radius: [30]
        RelativeLayout:
            MDFillRoundFlatButton:
                id: 2
                text: "Профилактические прививки"
                size_hint: .8, .3
                pos_hint: {'center_x': .5, 'center_y': .75}
                font_size: dp(30)
                on_release: root.prof()
            MDFillRoundFlatButton:
                id: 2
                text: "Иммунодиагностические прививки"
                size_hint: .8, .3
                pos_hint: {'center_x': .5, 'center_y': .25}
                font_size: dp(30)
                on_release: root.immuno()
<PrivivkiView>
    name: 'privview'
    MDTextButton:
        size_hint: .18, .15
        halign: 'center'
        pos_hint: {'center_x': .911, 'center_y': .1}
        font_size: dp(25)
        on_release:
            root.manager.current = 'priv'
            root.ids.scrollid.clear_widgets()
        Image:
            source: 'assets/exitbutton.png'
            center_x: self.parent.center_x
            center_y: self.parent.center_y
            allow_stretch: True
            size: 300, 350
    ScrollView:
        size_hint: .6, .9
        md_bg_color: 1,1,1,0
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            scroll_distance: 30
            cols:1
            spacing:10 
            size_hint_y: None
            height: self.minimum_height
            id: scrollid
"""
                    )


class Itemfactor(RelativeLayout):
    pass


class Item(RelativeLayout):
    pass


class Full(RelativeLayout):
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
                self.timeclocks = Clock.schedule_interval(self.manager.get_screen('loged').update, 1)
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


class MOSScreen(Screen):
    dialogerror = None
    mobiles = None
    mobileerror = None
    waiterror = None
    factor = None
    timeclock = None
    def emias2(self, driver, Twofactorverifcode):
        t = threading.Thread(
            target=self.emiasfac, args=[driver, Twofactorverifcode], daemon = True
        )
        if not t.is_alive():
            t.start()
    def emiasthread(self, driver, verifcode):
        t = threading.Thread(
            target=self.emias, args=[driver, verifcode], daemon=True
        )
        if not t.is_alive():
            t.start()
    def emiasfac(self, driver, Twofactorverifcode):
        Twofactor = driver.find_element(By.NAME, "sms-code")
        Twofactor.send_keys(Twofactorverifcode)
        verif_button = driver.find_element(By.ID, "verifyBtn").click()
        time.sleep(5)
        agree = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agree")))
        login_button = driver.find_element(By.ID, "agree").click()
        if driver.current_url == "https://lk.emias.mos.ru/":
            self.em2fac(driver)
        else:
            self.fac2(driver)
    def emias(self, driver, verifcode):
        def refferals(*args):
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
            oms = jsdata["profile"]["policyNum"]
            bdates = jsdata["profile"]["birthDate"]
            s = requests.Session()
            for cookie in driver.get_cookies():
                c = {cookie["name"]: cookie["value"]}
                s.cookies.update(c)
            self.succ(names, sure, age, idus, authtoken, oms, bdates, s)
            driver.quit()
        usercode = driver.find_element(By.ID, "otp_input")
        usercode.send_keys(verifcode)
        time.sleep(5)
        if driver.current_url == "https://lk.emias.mos.ru/":
            self.error(driver)

        else:
            refferals()

    @mainthread
    def fac2(self, driver):
        self.Twofactordialog(driver)
        self.manager.current = 'mos'
    @mainthread
    def err(self):
        self.error_dialog()
        self.manager.current = "mos"
    @mainthread
    def succ(self, names, sure, age, idus, authtoken, oms, bdates, s):
        self.manager.current = "mosloged"
        self.manager.get_screen("mosloged").ids.authname.text = names
        self.manager.get_screen("mosloged").ids.sures.text = sure
        self.manager.get_screen("mosloged").ids.ages.text = age
        self.manager.get_screen("lkcard").idus = idus
        self.manager.get_screen("lkcard").authtoken = authtoken
        self.manager.get_screen("priv").idus = idus
        self.manager.get_screen("priv").authtoken = authtoken
        self.manager.get_screen("lkcard").s = s
        self.manager.get_screen("priv").s = s
        self.manager.get_screen("loged").oms = oms
        self.manager.get_screen('loged').bdates = bdates
        self.manager.get_screen('loged').types = 'mos'
    @mainthread
    def em2fac(self, driver):
        self.mobile(driver)
        self.manager.current = "mos"
    @mainthread
    def error(self, driver):
        self.mobileerrors(driver)
        self.manager.current = "mos"
    @mainthread
    def block(self):
        self.waiterrors()
        self.manager.current = "mos"
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

    def Twofactordialog(self, driver):
        def use_input(obj):
            if (
                    self.factor.content_cls.ids.verif1.text == ""
                    or self.factor.content_cls.ids.verif2.text == ""
                    or self.factor.content_cls.ids.verif3.text == ""
                    or self.factor.content_cls.ids.verif4.text == ""
                    or self.factor.content_cls.ids.verif5.text == ""
                    or self.factor.content_cls.ids.verif6.text == ""
                    or len(
                self.factor.content_cls.ids.verif1.text
                + self.factor.content_cls.ids.verif2.text
                + self.factor.content_cls.ids.verif3.text
                + self.factor.content_cls.ids.verif4.text
                + self.factor.content_cls.ids.verif5.text
                + self.factor.content_cls.ids.verif6.text
            )
                    > 6
            ):
                None
            else:
                Twofactorverifcode = (
                        self.factor.content_cls.ids.verif1.text
                        + self.factor.content_cls.ids.verif2.text
                        + self.factor.content_cls.ids.verif3.text
                        + self.factor.content_cls.ids.verif4.text
                        + self.factor.content_cls.ids.verif5.text
                        + self.factor.content_cls.ids.verif6.text
                )
                self.factor.content_cls.ids.verif1.text = ""
                self.factor.content_cls.ids.verif2.text = ""
                self.factor.content_cls.ids.verif3.text = ""
                self.factor.content_cls.ids.verif4.text = ""
                self.factor.content_cls.ids.verif5.text = ""
                self.factor.content_cls.ids.verif6.text = ""
                self.manager.current = "load"
                self.emias2(driver, Twofactorverifcode)
                self.factor.dismiss()

        if not self.factor:
            self.factor = MDDialog(
                title="Введите СМС КОД",
                type="custom",
                auto_dismiss=False,
                content_cls=Itemfactor(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Ввести", md_bg_color="ff0000", on_release=use_input
                    )
                ],
            )
        self.factor.open()

    def mobile(self, driver):
        def use_input(obj):
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
                self.emiasthread(driver, verifcode)
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

    def mobileerrors(self, driver):
        def use_input(obj):
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
                self.emiasthread(driver, verifcode)
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
            Clock.unschedule(asyncs)
            self.waiterror.dismiss()
            counts = 59
            self.waiterror.content_cls.ids.timers.text = "59"
            self.waiterror.content_cls.ids.succ.text = ""
            self.waiterror.content_cls.ids.succ1.text = ""
            self.waiterror.content_cls.ids.icons.icon = "alert-circle"
            self.waiterror.content_cls.ids.labels.text = "Доступ разблокируется через"

        def timer(*args):
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
        def emias(*args):
            elements = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "otp_input"))
            )
            self.em2fac(driver)
        def nextstep(*args):
            try:
                Twofactor = driver.find_element(By.NAME, "sms-code")
                self.fac2(driver)
            except:
                emias()
        try:
            useragent = UserAgent()
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", useragent.random)
            firefox_options = Options()
            #firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(
                executable_path="C:\\Users\\PCWORK\\Desktop\\alter\\AlterGUI\\geckodriver.exe",
                options=firefox_options,
                firefox_profile=profile
            )
            driver.get(
                "https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth"
            )
            element = WebDriverWait(driver, 1200).until(
                EC.element_to_be_clickable((By.ID, "login"))
            )
            loginmos = driver.find_element(By.NAME, "login")
            loginmos.send_keys(login)
            passwordmos = driver.find_element(By.NAME, "password")
            passwordmos.send_keys(password)
            login_button = driver.find_element(
                By.ID,"bind").click()
            try:
                error = driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a",
                ).text
                self.err()
                driver.quit()
                sys.exit()
            except:
                nextstep()
        except:
            self.err()
            driver.quit()
            sys.exit()
    def check(self):
        if self.email.text != "":
            if len(self.password.text) >= 8:
                login = self.email.text
                password = self.password.text
                self.password.text = ''
                self.email.text = ''
                self.password.helper_text = ""
                self.password.helper_text_color_normal = "white"
                self.password.helper_text_color_focus = "white"
                self.email.helper_text = ""
                self.email.helper_text_color_normal = "white"
                self.email.helper_text_color_focus = "white"
                self.mosfunc(login, password)
                self.manager.current = "load"
                if self.timeclock == None:
                    self.timeclock = Clock.schedule_interval(self.manager.get_screen('mosloged').update, 1)
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = "red"
                self.password.helper_text_color_focus = "red"
                self.email.helper_text = ""
                self.email.helper_text_color_normal = "white"
                self.email.helper_text_color_focus = "white"
        else:
            self.email.helper_text = "Введите телефон, электронную почту или СНИЛС "
            self.email.helper_text_color_normal = "red"
            self.email.helper_text_color_focus = "red"


# Страница после авторизации
class MOSLoged(Screen):
    def update(self, *args):
        today = datetime.datetime.now()
        dt = datetime.datetime.today()
        days = str(datetime.datetime.strftime(today, '%d'))
        months = str(datetime.datetime.strftime(today, '%B'))
        years = str(datetime.datetime.strftime(today, '%Y'))
        time = str(datetime.datetime.now().strftime("%H:%M"))
        week = datetime.datetime.weekday(today)
        if week == 0:
            week = 'ПН'
        elif week == 1:
            week = 'ВТ'
        elif week == 2:
            week = 'СР'
        elif week == 3:
            week = 'ЧТ'
        elif week == 4:
            week = 'ПТ'
        elif week == 5:
            week = 'СБ'
        elif week == 6:
            week = 'ВС'
        self.ids.days.text = days
        self.ids.months.text = months
        self.ids.years.text = years
        self.ids.time.text = time
        self.ids.week.text = week

    def exits(self):
        self.manager.current = "enter"

    pass


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

    def update(self, *args):
        today = datetime.datetime.now()
        dt = datetime.datetime.today()
        days = str(datetime.datetime.strftime(today, '%d'))
        months = str(datetime.datetime.strftime(today, '%B'))
        years = str(datetime.datetime.strftime(today, '%Y'))
        time = str(datetime.datetime.now().strftime("%H:%M"))
        week = datetime.datetime.weekday(today)
        if week == 0:
            week = 'ПН'
        elif week == 1:
            week = 'ВТ'
        elif week == 2:
            week = 'СР'
        elif week == 3:
            week = 'ЧТ'
        elif week == 4:
            week = 'ПТ'
        elif week == 5:
            week = 'СБ'
        elif week == 6:
            week = 'ВС'
        self.ids.days.text = days
        self.ids.months.text = months
        self.ids.years.text = years
        self.ids.time.text = time
        self.ids.week.text = week

    def exits(self):
        self.manager.current = 'enter'

    def prikreplenia(self):
        inf = requests.post('https://emias.info/api/emc/appointment-eip/v1/?getPatientInfo3', json={"jsonrpc": "2.0", "id": "RUi98VgEkYYc8PPKR-OdE", "method": "getPatientInfo3",
                                        "params": {"omsNumber": self.oms, "birthDate": self.bdates, "typeAttach": [0, 1, 2],
                                                   "onlyMoscowPolicy": False}})
        jsinf = inf.json()
        layout = RelativeLayout()
        for i in range(len(jsinf['result']['attachments']['attachment'])):
            name = MDLabel(
                text=jsinf['result']['attachments']['attachment'][i]['lpu']['name']
            )
            name.font_size = 45
            name.pos_hint = {'center_x': .55, 'center_y': .8}
            layout.add_widget(name)
            address = MDLabel(
                text=jsinf['result']['attachments']['attachment'][i]['lpu']['address']
            )
            address.font_size = 35
            address.pos_hint = {'center_x': .55, 'center_y': .6}
            layout.add_widget(address)
            time = datetime.datetime.fromisoformat(jsinf['result']['attachments']['attachment'][i]['createDate'])
            create = MDLabel(
                text=f'{time.strftime("Прикреплено от %d %B %Y")}',
            )
            create.font_size = 35
            create.pos_hint = {'center_x': .55, 'center_y': .4}
            layout.add_widget(create)
            self.manager.get_screen('prik').ids.lay.add_widget(layout)
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
                            perenos.bind(on_release=self.showdateandtime)
                            perenos.pos_hint = {'center_x': .85, 'center_y': .2}
                            perenos.font_size = 40
                            layout.add_widget(perenos)
                            card.add_widget(layout)
                            self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
        self.manager.current = 'perenos'

    def showdateandtime(self, instance):
        vrachchoose = instance.vrachnum
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


class Tab(MDFloatLayout, MDTabsBase):
    pass


class MyToggleButton(MDRaisedButton, MDToggleButton):
    def perenesti(self, *args):
        sm = MDApp.get_running_app().sm
        sm.get_screen('loged').perenesti()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = (29 / 255, 89 / 255, 242 / 255, 1)
        self.background_normal = "grey"

    def on_state(self, widget, value):
        sm = MDApp.get_running_app().sm
        self.btn = MDRaisedButton(text='Записать')
        self.btn.font_size = 30
        self.btn.pos_hint = {'center_x': .65, 'center_y': .1}
        self.btn.size_hint = (.28, .13)
        self.btn.bind(on_release=self.perenesti)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            sm.get_screen('loged').perenosEnd = self.endTime
            sm.get_screen('loged').perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None


class MyToggleButtonNew(MDRaisedButton, MDToggleButton):
    def appointment(self, *args):
        sm = MDApp.get_running_app().sm
        sm.get_screen('loged').appointment()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = (29 / 255, 89 / 255, 242 / 255, 1)
        self.background_normal = "grey"

    def on_state(self, widget, value):
        sm = MDApp.get_running_app().sm
        self.btn = MDRaisedButton(text='Записать')
        self.btn.font_size = 30
        self.btn.pos_hint = {'center_x': .65, 'center_y': .1}
        self.btn.size_hint = (.28, .13)
        self.btn.bind(on_release=self.appointment)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            perenosEnd = self.endTime
            perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None


class Loading(Screen):
    pass


class Loadingoms(Screen):
    pass


class Zapisi(Screen):
    pass


class Showdate(Screen):
    def back(self):
        self.manager.current = 'perenos'
        self.ids.lay.clear_widgets()
        try:
            if self.children[0].text == 'Записать':
                self.remove_widget(self.children[0])
            else:
                None
        except:
            None


class Perenos(Screen):
    pass


class Napravlenia(Screen):
    pass


class Prikreplenia(Screen):
    pass


class LKCard(Screen):
    def show_document(self):
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
        ima.height = self.height  
        lay.height = ima.height
        but.height = 150
        but.width = 200
        but.font_size = 30
        lay.add_widget(ima)
        scrollview.add_widget(lay)
        self.dialog = MDDialog(
            type='custom',
            content_cls=scrollview,
            size_hint_x= .5,
            elevation = 0,
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
        hti = Html2Image()
        html = jspros['documentHtml']
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1000")
        driver = webdriver.Firefox(options=firefox_options)
        driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html))
        driver.quit()
        height = driver.execute_script("return document.body.scrollHeight")
        hti.screenshot(html_str=html, save_as=f"document.png", size=(1000, height))
        self.show_document()


    def historyanamnes(self, instance):
        anamnes = self.s.get(f'https://lk.emias.mos.ru/api/1/documents/inspections?ehrId={self.idus}&shortDateFilter=all_time',
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
                        doctorspec = MDLabel(
                            text=f"{jsanam['documents'][i]['doctorSpecialization']}",
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        doctorspec.font_size = 45
                        doctorspec.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(doctorspec)
                    except:
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
                        title = MDLabel(
                            text=f"{jsanam['documents'][i]['title']}",
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        title.font_size = 45
                        title.pos_hint = {'center_x': .55, 'center_y': .6}
                        layout.add_widget(title)
                    if 'doctorName' in jsanam['documents'][i]:
                        doctorname = MDLabel(
                            text=f"{jsanam['documents'][i]['doctorName']}",
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        doctorname.font_size = 45
                        doctorname.pos_hint = {'center_x': .55, 'center_y': .4}
                        layout.add_widget(doctorname)
                    if 'appointmentDate' in jsanam['documents'][i]:
                        time = datetime.datetime.fromisoformat(jsanam['documents'][i]['appointmentDate'])
                        timelab = MDLabel(
                            text=f'{time.strftime("%a, %d %b %Y")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        timelab.font_size = 35
                        timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
                        layout.add_widget(timelab)
                    if 'organisation' in jsanam['documents'][i]:
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
                card.bind(on_release = self.documentview)
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
            analiz = self.s.get(f'https://lk.emias.mos.ru/api/1/documents/analyzes?ehrId={self.idus}&shortDateFilter=all_time',
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
            ldp = self.s.get(f'https://lk.emias.mos.ru/api/1/documents/research?ehrId={self.idus}&shortDateFilter=all_time',
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
                card.bind(on_release = self.documentview)
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
                prosmotr = self.s.get(f"https://lk.emias.mos.ru/api/3/receipt/details?ehrId={self.idus}&prescriptionNumber={jsrec['receipts'][i]['prescriptionNumber']}",
                    headers={'X-Access-JWT': self.authtoken})
                jspros = prosmotr.json()
                svg_code =  jspros['qrCode']
                svg2png(bytestring=svg_code,output_width=350, output_height=350, write_to='document.png', negate_colors= (1,1,1,1))
                ima = Image(
                    source='document.png',
                    size_hint = (None, None)
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
            print(jsemg)
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

class History(Screen):
    pass


class AnamnesView(Screen):
    pass


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


class PrivivkiView(Screen):
    pass


class AlterApp(MDApp):
    sm = None
    def build(self):
        self.sm = ScreenManager()
        sm = self.sm
        sm.add_widget(ENTERScreen(name="enter"))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(MOSScreen(name="mos"))
        sm.add_widget(OMSLoged(name="loged"))
        sm.add_widget(MOSLoged(name="mosloged"))
        sm.add_widget(Loading(name="load"))
        sm.add_widget(Loadingoms(name="loadoms"))
        sm.add_widget(Zapisi(name='zapisi'))
        sm.add_widget(Perenos(name='perenos'))
        sm.add_widget(Showdate(name=('timetable')))
        sm.add_widget(Prikreplenia(name='prik'))
        sm.add_widget(Napravlenia(name='napr'))
        sm.add_widget(LKCard(name="lkcard"))
        sm.add_widget(History(name='history'))
        sm.add_widget(AnamnesView(name='anamn'))
        sm.add_widget(Privivki(name='priv'))
        sm.add_widget((PrivivkiView(name='privview')))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return sm


if __name__ == '__main__':
    AlterApp().run()
# 5494499745000410 1088989771000020