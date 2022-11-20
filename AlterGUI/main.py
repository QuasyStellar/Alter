import re
import sys
import time
import datetime
import locale
locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
import threading
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
                    font_name: 'roboto'
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(45)
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
                    font_name: 'roboto'
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(40)
                    helper_text_mode: "persistent"
                    size_hint: 1, .22
                    font_name: 'roboto'
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
    MDCard:
        size_hint: .8, .8
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
                on_release: root.view(2)
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
            root.manager.current = 'mosloged'
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
        global result, curuserid
        try:
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
                result = policy
        except:
            result = 666
        sys.exit()


    def omslogin(self):
        global oms
        def checkglobal(*args):
            global result, bdates, types
            if result == None:
                None
            elif result == 0:
                result = None
                self.manager.current = "oms"
                self.show_alert_dialog()
                Clock.unschedule(clocks)
            elif result == 666:
                result = None
                self.manager.current = "oms"
                self.show_alert_dialog1()
                Clock.unschedule(clocks)
            else:
                self.manager.current = "loged"
                policnum = f"[color=#ffffff]{result[0:4]+' **** **** '+ result[12:16]}[/color]"
                self.manager.get_screen("loged").ids.authname.text = policnum
                bdates = year + "-" + month + "-" + day
                Clock.unschedule(clocks)
                result = None
                types = 'oms'

        if len(self.policy.text) < 16 or len(self.policy.text) > 16:
            self.policy.helper_text = "Некорректный полис"
            self.policy.helper_text_color_normal = "red"
            self.policy.helper_text_color_focus = "red"
        elif self.bdate.text != "":
            oms = self.policy.text
            self.omsfunc(self.policy.text, day, month, year)
            self.bdate.helper_text = ""
            self.bdate.helper_text_color_normal = "white"
            self.bdate.helper_text_color_focus = "white"
            self.policy.helper_text_color_normal = "white"
            self.policy.helper_text = ""
            self.bdate.text = ''
            self.policy.text = ''
            self.policy.helper_text_color_focus = "white"
            self.manager.current = "loadoms"
            clocks = Clock.schedule_interval(checkglobal, 2)
            if self.timeclocks == None:
                self.timeclocks = Clock.schedule_interval(self.manager.get_screen('loged').update, 2)

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
    def Twofactordialog(self):
        def use_input(obj):
            global Twofactorverifcode
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
        global verifcode, result, curuserid, polic, names, sure, male, age, idus, authtoken, Twofactorverifcode
        def emias(*args):
            global verifcode, result, curuserid, polic, names, sure, male, age, idus, authtoken, Twofactorverifcode
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
        def refferals(*args):
            global verifcode, result, curuserid, polic, names, sure, age, idus, authtoken, oms, bdates, s
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
            result = 1
            driver.quit()

        try:
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(
                executable_path="C:\\Users\\PCWORK\\Desktop\\alter\\AlterGUI\\geckodriver.exe",
                options=firefox_options,
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
                try:
                    Twofactor = driver.find_element(By.NAME, "sms-code")
                    while driver.current_url != "https://lk.emias.mos.ru/":
                        result = 22
                        while Twofactorverifcode == None:
                            None
                        else:
                            Twofactor.send_keys(Twofactorverifcode)
                            verif_button = driver.find_element(By.ID, "verifyBtn").click()
                            time.sleep(5)
                            try:
                                agree = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "agree")))
                                login_button = driver.find_element(By.ID, "agree").click()
                            except:
                                None
                            Twofactorverifcode = None
                            time.sleep(5)
                    else:
                        emias()
                except:
                    emias()
        except:
            result = 0
            driver.quit()
            sys.exit()

    def check(self):
        global login, password

        def checkglobal(*args):
            global verifcode, result, curuserid, polic, names, sure, male, age, idus, authtoken, types
            if result == None:
                None
            elif result == 22:
                self.Twofactordialog()
                self.manager.current = 'mos'
                result = None
            elif result == 0:
                self.error_dialog()
                self.manager.current = "mos"
                result = None
                Clock.unschedule(vclocks)
            elif result == 1:
                self.manager.current = "mosloged"
                result = None
                self.manager.get_screen("mosloged").ids.authname.text = names
                self.manager.get_screen("mosloged").ids.sures.text = sure
                self.manager.get_screen("mosloged").ids.ages.text = age
                types = 'mos'
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
                vclocks = Clock.schedule_interval(checkglobal, 2)
                if self.timeclock == None:
                    self.timeclock = Clock.schedule_interval(self.manager.get_screen('mosloged').update, 2)
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
        months =  str(datetime.datetime.strftime(today, '%B'))
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
    def screenback(self):
        global types
        if types == 'oms':
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
        months =  str(datetime.datetime.strftime(today, '%B'))
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
        global oms, bdates, result, doclist
        inf = requests.post(info, json = {"jsonrpc":"2.0","id":"RUi98VgEkYYc8PPKR-OdE","method":"getPatientInfo3","params":{"omsNumber":oms,"birthDate":bdates,"typeAttach":[0,1,2], "onlyMoscowPolicy":False}})
        jsinf = inf.json()
        layout = RelativeLayout()
        for i in range(len(jsinf['result']['attachments']['attachment'])):
            name = MDLabel(
                        text=jsinf['result']['attachments']['attachment'][i]['lpu']['name']
                        )
            name.font_size  =  45
            name.pos_hint = {'center_x': .55, 'center_y':.8}
            layout.add_widget(name)
            address = MDLabel(
                text = jsinf['result']['attachments']['attachment'][i]['lpu']['address']
                )
            address.font_size  =  35
            address.pos_hint = {'center_x': .55, 'center_y':.6}
            layout.add_widget(address)
            time = datetime.datetime.fromisoformat( jsinf['result']['attachments']['attachment'][i]['createDate'])
            create = MDLabel(
                text = f'{time.strftime("Прикреплено от %d %B %Y")}',
                )
            create.font_size  = 35
            create.pos_hint = {'center_x': .55, 'center_y':.4}
            layout.add_widget(create)
            self.manager.get_screen('prik').ids.lay.add_widget(layout)
        self.manager.current = 'prik'


    
    def zapisi(self):
        global oms, bdates, result, doclist
        prosmotr = requests.post(doclist, json = {"jsonrpc":"2.0","id":"tnSZKjovHE_X2b-JYQ0PB","method":"getAppointmentReceptionsByPatient","params":{"omsNumber":oms,"birthDate":bdates}})
        jsps = prosmotr.json()
        if len(jsps["result"]) == 0:
            card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
            layout = RelativeLayout()
            label = MDLabel(
                        text = 'Записей нет',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        halign = 'center'
                        )
            label.font_size = 60
            label.pos_hint = {'center_x':.5, 'center_y':.5}
            layout.add_widget(label)
            card.add_widget(layout)
            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
        else:
            for i in range(len(jsps['result'])):
                if 'toDoctor' in jsps["result"][i]:
                    card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                    layout = RelativeLayout()
                    specname = MDLabel(
                        text=f'{jsps["result"][i]["toDoctor"]["specialityName"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white', 
                        )
                    specname.font_size  =  45
                    specname.pos_hint = {'center_x': .55, 'center_y':.8}
                    layout.add_widget(specname)
                    time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                    timelab = MDLabel(
                        text = f'{time.strftime("%a, %d %b в %H:%M")}',
                        theme_text_color= 'Custom',
                        text_color= 'white', 
                        )
                    timelab.font_size  =  35
                    timelab.pos_hint = {'center_x': 1.2, 'center_y':.65}
                    layout.add_widget(timelab)
                    address = MDLabel(
                        text = f'{jsps["result"][i]["nameLpu"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    address.font_size  =  35
                    address.pos_hint = {'center_x': .55, 'center_y':.27}
                    layout.add_widget(address)
                    addressbol = MDLabel(
                        text = f'{jsps["result"][i]["lpuAddress"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    addressbol.font_size  =  35
                    addressbol.pos_hint = {'center_x': .55, 'center_y':.15}
                    layout.add_widget(addressbol)
                    room = MDLabel(
                        text = f'Каб. {jsps["result"][i]["roomNumber"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    room.font_size  = 40
                    room.pos_hint = {'center_x': 1.2, 'center_y':.5}
                    layout.add_widget(room)
                    fio = MDLabel(
                        text = f'{jsps["result"][i]["toDoctor"]["doctorFio"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    fio.font_size  = 30
                    fio.pos_hint = {'center_x': .55, 'center_y':.66}
                    layout.add_widget(fio)
                    otmena = MDIconButton(
                        theme_text_color= 'Custom',
                        text_color= 'red',
                        icon='delete'
                        )
                    otmena.zapisid = jsps["result"][i]["id"]
                    otmena.bind(on_release=self.otmenas)
                    otmena.pos_hint = {'center_x': .95, 'center_y':.2}
                    otmena.icon_size = '60dp'
                    layout.add_widget(otmena)

                    perenos = MDFillRoundFlatButton(
                        text="Перенести",
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    perenos.zapisid = jsps["result"][i]["id"]
                    perenos.bind(on_release=self.perenoss)
                    perenos.pos_hint = {'center_x': .8, 'center_y':.2}
                    perenos.font_size  = 40
                    perenos.zapisid = i
                    layout.add_widget(perenos)
                    card.add_widget(layout)
                    self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
                else:
                    card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                    layout = RelativeLayout()
                    specname = MDLabel(
                        text=jsps["result"][i]["toLdp"]["ldpTypeName"],
                        theme_text_color= 'Custom',
                        text_color= 'white', 
                        )
                    specname.font_size  =  45
                    specname.pos_hint = {'center_x': .55, 'center_y':.8}
                    layout.add_widget(specname)
                    time = datetime.datetime.fromisoformat(jsps["result"][i]["startTime"])
                    timelab = MDLabel(
                        text = f'{time.strftime("%a, %d %b в %H:%M")}',
                        theme_text_color= 'Custom',
                        text_color= 'white', 
                        )
                    timelab.font_size  =  35
                    timelab.pos_hint = {'center_x': 1.2, 'center_y':.65}
                    layout.add_widget(timelab)
                    address = MDLabel(
                        text = f'{jsps["result"][i]["nameLpu"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    address.font_size  =  35
                    address.pos_hint = {'center_x': .55, 'center_y':.27}
                    layout.add_widget(address)
                    addressbol = MDLabel(
                        text = f'{jsps["result"][i]["lpuAddress"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    addressbol.font_size  =  35
                    addressbol.pos_hint = {'center_x': .55, 'center_y':.15}
                    layout.add_widget(addressbol)
                    room = MDLabel(
                        text = f'Каб. {jsps["result"][i]["roomNumber"]}',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    room.font_size  = 40
                    room.pos_hint = {'center_x': 1.2, 'center_y':.5}
                    layout.add_widget(room)
                    otmena = MDIconButton(
                        theme_text_color= 'Custom',
                        text_color= 'red',
                        icon='delete'
                        )
                    otmena.zapisid = jsps["result"][i]["id"]
                    otmena.bind(on_release=self.otmenas)
                    otmena.pos_hint = {'center_x': .95, 'center_y':.2}
                    otmena.icon_size = '60dp'
                    layout.add_widget(otmena)

                    perenos = MDFillRoundFlatButton(
                        text="Перенести",
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        )
                    perenos.bind(on_release=self.perenoss)
                    perenos.pos_hint = {'center_x': .8, 'center_y':.2}
                    perenos.font_size  = 40
                    perenos.zapisid = i
                    layout.add_widget(perenos)
                    card.add_widget(layout)
                    self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
        self.manager.current = 'zapisi'

    def otmenas(self, instance):
        global oms, bdates
        otmenas = requests.post(cancel, json = {"jsonrpc":"2.0","id":"lXe4h6pwr3IF-xCqBnESK","method":"cancelAppointment","params":{"omsNumber":oms,"birthDate":bdates,"appointmentId":instance.zapisid}})
        self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
        self.succ()
        self.manager.get_screen('loged').zapisi()

    def perenoss(self, instance):
        global oms, bdates, doclist, zapisvibor
        c = 0
        spisokzapisei = requests.post(doclist, json = {"jsonrpc":"2.0","id":"H0XYtGjt9CtPQqfGt7NYp","method":"getAppointmentReceptionsByPatient","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspisok = spisokzapisei.json()
        zapisvibor = instance.zapisid
        if 'toDoctor' in jsspisok['result'][zapisvibor]:
            appID = jsspisok["result"][zapisvibor]['id']
            specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
            recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
            spisokvrachei = requests.post(speclist, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"appointmentId":appID,"specialityId":specID}})
            jsvrachi = spisokvrachei.json()
            for i in range(len(jsvrachi["result"])):
                for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            c+=1
            if c == 0:
                card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                layout = RelativeLayout()
                label = MDLabel(
                        text = 'Перенос не доступен',
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        halign = 'center'
                        )
                label.font_size = 40
                label.pos_hint = {'center_x':.5, 'center_y':.5}
                layout.add_widget(label)
                card.add_widget(layout)
                self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
            else:
                for i in range(len(jsvrachi["result"])):
                    for j in range(len(jsvrachi["result"][i]['complexResource'])):
                            if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                                card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                                layout = RelativeLayout()
                                name= MDLabel(
                                    text = jsvrachi["result"][i]['name'].replace("_", " "),
                                    theme_text_color= 'Custom',
                                    text_color= 'white'
                                )
                                name.font_size = 45
                                name.pos_hint = {'center_x': .55, 'center_y': .8}
                                layout.add_widget(name)
                                time = datetime.datetime.fromisoformat(jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                                avail = MDLabel(
                                    text=f'{time.strftime("С %d %b, %a")}',
                                    theme_text_color='Custom',
                                    text_color='white',
                                )
                                avail.font_size = 35
                                avail.pos_hint = {'center_x':.55, 'center_y':.6}
                                layout.add_widget(avail)
                                address = MDLabel(
                                    text= jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
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
                                    theme_text_color= 'Custom',
                                    text_color= 'white',
                                    )
                                perenos.vrachnum = i
                                perenos.bind(on_release=self.showdateandtime)
                                perenos.pos_hint = {'center_x': .85, 'center_y':.2}
                                perenos.font_size  = 40
                                layout.add_widget(perenos)
                                card.add_widget(layout)
                                self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
        else:
            appID = jsspisok["result"][zapisvibor]['id']
            recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
            spisokvrachei = requests.post(speclist, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"appointmentId":appID}})
            jsvrachi = spisokvrachei.json()
            for i in range(len(jsvrachi["result"])):
                for j in range(len(jsvrachi["result"][i]['complexResource'])):
                    if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                        c+=1
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
                            card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                            layout = RelativeLayout()
                            name= MDLabel(
                                text = jsvrachi["result"][i]['name'].replace("_", " "),
                                theme_text_color= 'Custom',
                                text_color= 'white'
                            )
                            name.font_size = 45
                            name.pos_hint = {'center_x': .55, 'center_y': .8}
                            layout.add_widget(name)
                            time = datetime.datetime.fromisoformat(jsvrachi["result"][i]['complexResource'][j]['room']['availabilityDate'])
                            avail = MDLabel(
                                text=f'{time.strftime("С %d %b, %a")}',
                                theme_text_color='Custom',
                                text_color='white',
                            )
                            avail.font_size = 35
                            avail.pos_hint = {'center_x':.55, 'center_y':.6}
                            layout.add_widget(avail)
                            address = MDLabel(
                                text= jsvrachi["result"][i]['complexResource'][j]['room']['lpuShortName'],
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
                                theme_text_color= 'Custom',
                                text_color= 'white',
                                )
                            perenos.vrachnum = i
                            perenos.bind(on_release=self.showdateandtime)
                            perenos.pos_hint = {'center_x': .85, 'center_y':.2}
                            perenos.font_size  = 40
                            layout.add_widget(perenos)
                            card.add_widget(layout)
                            self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
        self.manager.current = 'perenos'

    def showdateandtime(self, instance):
        global oms, bdates, zapisvibor, appID, specID, recpID, resID, complID
        vrachchoose = instance.vrachnum
        spisokzapisei = requests.post(doclist, json = {"jsonrpc":"2.0","id":"H0XYtGjt9CtPQqfGt7NYp","method":"getAppointmentReceptionsByPatient","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspisok = spisokzapisei.json()
        if 'toDoctor' in jsspisok["result"][zapisvibor]:
            appID = jsspisok["result"][zapisvibor]['id']
            specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
            recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
            spisokvrachei = requests.post(speclist, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"appointmentId":appID,"specialityId":specID}})
            jsvrachi = spisokvrachei.json()
            resID = jsvrachi["result"][vrachchoose]["id"]
            for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                    if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                        complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
            dati = requests.post(datespec, json = {"jsonrpc":"2.0","id":"RUi98VgEkYYc8PPKR-OdE","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdates,"availableResourceId":resID,"complexResourceId":complID,"appointmentId":appID,"specialityId":specID}})
            jsdati = dati.json()
            tabs =MDTabs(
                radius= [30, 30, 0,0],
                allow_stretch= True,
                tab_hint_x= True,
                tab_bar_height= '150'
                ) 
            for i in range(len(jsdati["result"]['scheduleOfDay'])):
                time = datetime.datetime.fromisoformat(jsdati["result"]['scheduleOfDay'][i]['date'])
                tab = Tab(
                    title=f'{time.strftime("%d %a")}'
                )
                tab.tab_label.font_size = '50sp'
                scrolllayout = ScrollView(
                    size_hint= (1, .9),
                    md_bg_color=(1,1,1,0)
                    )
                layout = StackLayout()
                layout.size_hint_y = None
                layout.spacing  = 40
                for j in range(len(jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                    timeF = datetime.datetime.fromisoformat(jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                    times = MyToggleButton(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color= 'Custom',
                            text_color= 'white',
                            md_bg_color='grey',
                            group = "x"
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
            appID = jsspisok["result"][zapisvibor]['id']
            recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
            spisokvrachei = requests.post(speclist, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"appointmentId":appID}})
            jsvrachi = spisokvrachei.json()
            resID = jsvrachi["result"][vrachchoose]["id"]
            for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                    if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                        complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
            dati = requests.post(datespec, json = {"jsonrpc":"2.0","id":"RUi98VgEkYYc8PPKR-OdE","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdates,"availableResourceId":resID,"complexResourceId":complID,"appointmentId":appID,"specialityId":specID}})
            jsdati = dati.json()
            tabs =MDTabs(
                radius= [30, 30, 0,0],
                allow_stretch= True,
                tab_hint_x= True,
                tab_bar_height= '150'
                ) 
            for i in range(len(jsdati["result"]['scheduleOfDay'])):
                time = datetime.datetime.fromisoformat(jsdati["result"]['scheduleOfDay'][i]['date'])
                tab = Tab(
                    title=f'{time.strftime("%d %a")}'
                )
                tab.tab_label.font_size = '50sp'
                scrolllayout = ScrollView(
                    size_hint= (1, .9),
                    md_bg_color=(1,1,1,0)
                    )
                layout = StackLayout()
                layout.size_hint_y = None
                layout.spacing  = 40
                for j in range(len(jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                    timeF = datetime.datetime.fromisoformat(jsdati["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                    times = MyToggleButton(
                            text=timeF.strftime("%H:%M"),
                            theme_text_color= 'Custom',
                            text_color= 'white',
                            md_bg_color='grey',
                            group = "x"
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
        global oms, bdates, perenosEnd, perenosStart, appID, specID, recpID, resID, complID
        appocreate = requests.post(create, json ={"jsonrpc":"2.0","id":"AvyJzHk1dm8eNqyg5uzLx","method":"createAppointment","params":{"omsNumber":oms,"birthDate":bdates,"availableResourceId":resID,"complexResourceId":complID,"receptionTypeId":recpID,"startTime":perenosStart,"endTime":perenosEnd}})
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
        global oms, bdates, perenosEnd, perenosStart, appID, recpID, resID, complID
        perenes = requests.post(shift, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"shiftAppointment","params":{"omsNumber":oms,"birthDate":bdates,"appointmentId":appID,"availableResourceId":resID,"complexResourceId":complID,"receptionTypeId":recpID,"startTime":perenosStart,"endTime":perenosEnd}})
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
        global oms, bdates
        prosmotrnaprs = requests.post(ref, json ={"jsonrpc":"2.0","id":"6Ov41JqE7a1bQ3i98ofeF","method":"getReferralsInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsnp = prosmotrnaprs.json()
        if len(jsnp["result"]) == 0:
                card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
                layout = RelativeLayout()
                label = MDLabel(
                    text='Направлений нет',
                    halign='center',
                    theme_text_color= 'Custom',
                    text_color= 'white',
                )
                label.font_size = 40
                label.pos_hint = {'center_x': .5, 'center_y': .5}
                layout.add_widget(label)
                card.add_widget(layout)
                self.manager.get_screen("napr").ids.scrollid.add_widget(card)
        else:
            for i in range(len(jsnp["result"])):
                if 'toDoctor' in jsnp['result'][i]:
                    card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                    layout = RelativeLayout()
                    name= MDLabel(
                        text = jsnp["result"][i]["toDoctor"]["specialityName"].replace("_", " "),
                        theme_text_color= 'Custom',
                        text_color= 'white'
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
                    avail.pos_hint = {'center_x':.55, 'center_y':.6}
                    layout.add_widget(avail)
                    end = MDLabel(
                        text= jsnp["result"][i]["endTime"],
                        theme_text_color='Custom',
                        text_color='white',
                    )
                    end.font_size = 30
                    end.pos_hint = {'center_x': .55, 'center_y': .4}
                    layout.add_widget(end)
                    card.add_widget(layout)
                    self.manager.get_screen("napr").ids.scrollid.add_widget(card)
                else:
                    card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                    layout = RelativeLayout()
                    name= MDLabel(
                        text = jsnp["result"][i]["toLdp"]["ldpTypeName"].replace("_", " "),
                        theme_text_color= 'Custom',
                        text_color= 'white'
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
                    avail.pos_hint = {'center_x':.55, 'center_y':.6}
                    layout.add_widget(avail)
                    end = MDLabel(
                        text= jsnp["result"][i]["endTime"],
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
        global oms, bdates
        specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspec = specialities.json()
        for i in range(len(jsspec["result"])):
            card = MDCard(orientation='vertical', size_hint=(1, None), height = 150, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
            layout = RelativeLayout()
            name= MDLabel(
                text = jsspec['result'][i]["name"].replace("_", " "),
                theme_text_color= 'Custom',
                text_color= 'white'
            )
            name.font_size = 35
            name.pos_hint = {'center_x': .55, 'center_y': .8}
            choose = MDFillRoundFlatButton(
                                text="Выбрать",
                                theme_text_color= 'Custom',
                                text_color= 'white',
                                )
            choose.bind(on_release=self.new)
            choose.zapisid = i
            choose.pos_hint = {'center_x': .85, 'center_y':.5}
            choose.font_size  = 40
            layout.add_widget(choose)
            layout.add_widget(name)
            card.add_widget(layout)
            self.manager.get_screen("zapisi").ids.scrollid.add_widget(card)
        self.manager.current = 'zapisi'
    def new(self, instance):
        global oms, bdates, zapisvibor, userid, specID, recpID
        count = 0
        resid = None
        assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsass = assignment.json()
        userid = jsass["id"]
        specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdates}})
        jsspec = specialities.json()
        specID = jsspec['result'][instance.zapisid]["code"]
        zapis = requests.post(speclist, json = {"jsonrpc":"2.0","id":userid,"method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"specialityId": specID}})
        jszapis = zapis.json()
        for i in range(len(jszapis["result"])):
            for j in range(len(jszapis["result"][i]['complexResource'])):
                if 'room' in jszapis["result"][i]['complexResource'][j]:
                    recpID = jszapis["result"][i]['receptionType'][0]['code']
                    count+=1
        if count == 0:
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                              md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            label = MDLabel(
                text='Запись не доступна',
                halign='center',
                theme_text_color= 'Custom',
                text_color= 'white',
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
                        card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                        layout = RelativeLayout()
                        name= MDLabel(
                            text = jszapis['result'][i]["name"].replace('_', " "),
                            theme_text_color= 'Custom',
                            text_color= 'white'
                        )
                        name.font_size = 45
                        name.pos_hint = {'center_x': .55, 'center_y': .8}
                        layout.add_widget(name)
                        time = datetime.datetime.fromisoformat(jszapis["result"][i]['complexResource'][j]['room']['availabilityDate'])
                        avail = MDLabel(
                            text=f'{time.strftime("С %d %b, %a")}',
                            theme_text_color='Custom',
                            text_color='white',
                        )
                        avail.font_size = 35
                        avail.pos_hint = {'center_x':.55, 'center_y':.6}
                        layout.add_widget(avail)
                        address = MDLabel(
                            text= jszapis["result"][i]['complexResource'][j]['room']['lpuShortName'],
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
                            theme_text_color= 'Custom',
                            text_color= 'white',
                            )
                        perenos.resID = jszapis["result"][i]['complexResource'][j]['id']
                        perenos.availRES = jszapis["result"][i]['id']
                        perenos.bind(on_release=self.showdateandtimenew)
                        perenos.pos_hint = {'center_x': .85, 'center_y':.2}
                        perenos.font_size  = 40
                        layout.add_widget(perenos)
                        card.add_widget(layout)
                        self.manager.get_screen("perenos").ids.scrollid.add_widget(card)
        self.manager.current = 'perenos'

    def showdateandtimenew(self, instance):
        global oms, bdates, userid, specID, resID, complID, resID, complID
        resID = instance.availRES
        complID = instance.resID
        zapis = requests.post(speclist, json = {"jsonrpc":"2.0","id":userid,"method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdates,"specialityId": specID}})
        jszapis = zapis.json()
        proczapis = requests.post(datespec, json = {"jsonrpc":"2.0","id":"7g9bgvEa8VkCd6A2XHJ7p","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdates,"availableResourceId":instance.availRES,"complexResourceId":instance.resID,"specialityId":specID}})
        jsproczapis = proczapis.json()
        tabs =MDTabs(
                radius= [30, 30, 0,0],
                allow_stretch= True,
                tab_hint_x= True,
                tab_bar_height= '80'
                )
        for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
            time = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]["date"])
            tab = Tab(
                title=f'{time.strftime("%d %a")}'
            )
            tab.tab_label.font_size = '50sp'
            scrolllayout = ScrollView(
                size_hint= (1, .9),
                md_bg_color=(1,1,1,0)
                )
            layout = StackLayout()
            layout.size_hint_y = None
            layout.spacing  = 40
            for j in range(len(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'])):
                timeF = datetime.datetime.fromisoformat(jsproczapis["result"]['scheduleOfDay'][i]['scheduleBySlot'][0]['slot'][j]['startTime'])
                times = MyToggleButtonNew(
                        text=timeF.strftime("%H:%M"),
                        theme_text_color= 'Custom',
                        text_color= 'white',
                        md_bg_color='grey',
                        group = "x"
                        )
                times.font_size = 60
                times.size_hint_y= None
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
    global sm
    def perenesti(self, *args):
        sm.get_screen('loged').perenesti()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = (29 / 255, 89 / 255, 242 / 255, 1)
        self.background_normal = "grey"
    def on_state(self, widget, value):
        global perenosEnd, perenosStart
        self.btn = MDRaisedButton(text='Записать')
        self.btn.font_size = 30
        self.btn.pos_hint = {'center_x': .65, 'center_y':.1}
        self.btn.size_hint = (.28, .13)
        self.btn.bind(on_release=self.perenesti)
        if value == 'down':
            sm.get_screen('timetable').add_widget(self.btn)
            perenosEnd = self.endTime
            perenosStart = self.startTime
        else:
            sm.get_screen('timetable').remove_widget(sm.get_screen('timetable').children[0])
            perenosEnd = None
            perenosStart = None
class MyToggleButtonNew(MDRaisedButton, MDToggleButton):
    global oms, bdates, perenosEnd, perenosStart, appID, recpID, resID, complID, sm
    def appointment(self, *args):
        sm.get_screen('loged').appointment()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = (29 / 255, 89 / 255, 242 / 255, 1)
        self.background_normal = "grey"
    def on_state(self, widget, value):
        global perenosEnd, perenosStart
        self.btn = MDRaisedButton(text='Записать')
        self.btn.font_size = 30
        self.btn.pos_hint = {'center_x': .65, 'center_y':.1}
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
    global idus, authtoken, s
    def historyanamnes(self, instance):
        anamnes = s.get(f'https://lk.emias.mos.ru/api/1/documents/inspections?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
        jsanam = anamnes.json()
        for i in range(len(jsanam['documents'])):
            if 'appointmentDate' in jsanam['documents'][i]:
                date = jsanam['documents'][i]['appointmentDate']
                if date[0:4] == instance.year:
                    flag = False
                    try:
                        print(f'({i})',jsanam['documents'][i]['doctorSpecialization'])
                    except:
                        print(f'({i})',jsanam['documents'][i]['title'])
                        flag = True
                    if flag == False:
                        print(jsanam['documents'][i]['title'])
                    if 'doctorName' in jsanam['documents'][i]:
                        print(jsanam['documents'][i]['doctorName'])
                    if 'appointmentDate' in jsanam['documents'][i]:
                        print(jsanam['documents'][i]['appointmentDate'])
                    if 'organisation' in jsanam['documents'][i]:
                        print(jsanam['documents'][i]['organisation'])
    def view(self, id):
        def covidtest(*args):
            covid = s.get(f"https://lk.emias.mos.ru/api/1/documents/covid-analyzes?ehrId={idus}&shortDateFilter=all_time", headers = {'X-Access-JWT': authtoken})
            jscov = covid.json()
            for i in range(len(jscov['documents'])):
                card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                layout = RelativeLayout()
                title = MDLabel(
                    text=f"{jscov['documents'][i]['title']}",
                    theme_text_color= 'Custom',
                    text_color= 'white', 
                    )
                title.font_size  =  45
                title.pos_hint = {'center_x': .55, 'center_y':.8}
                layout.add_widget(title)
                time = datetime.datetime.fromisoformat(jscov['documents'][i]['date'])
                timelab = MDLabel(
                    text = f'{time.strftime("%a, %d %b в %H:%M")}',
                    theme_text_color= 'Custom',
                    text_color= 'white', 
                    )
                timelab.font_size  =  35
                timelab.pos_hint = {'center_x': 1.2, 'center_y':.65}
                layout.add_widget(timelab)
                card.add_widget(layout)
                self.manager.get_screen("history").ids.scrollid.add_widget(card)
            self.manager.current = 'history'

        def myvacine(*args):
            vacin = s.get(f"https://lk.emias.mos.ru/api/3/vaccinations?ehrId={idus}", headers = {'X-Access-JWT': authtoken})
            jsvac = vacin.json()
            vacinchoose = int(input('(0) Профилактические прививки\n(1) Иммунодиагностические тесты\n'))
            if vacinchoose == 0:
                for i in range(len(jsvac['doneList'])):
                    print(f"({i})",jsvac['doneList'][i]['infectionList'][0]['infectionName'])
                    print(jsvac['doneList'][i]['dateVaccination'])
                    print('Возраст: ',jsvac['doneList'][i]['age'])

            else:
                for i in range(len(jsvac['tubList'])):
                    print(f"({i})",jsvac['tubList'][i]['infectionList'][0]['infectionName'])
                    print(jsvac['tubList'][i]['dateVaccination'])
                    print(jsvac['tubList'][i]['tubResultList'][0]['reactionKind'])
                    print('Возраст: ',jsvac['tubList'][i]['age'])
        def myanamnes(*args):
            anamnes = s.get(f'https://lk.emias.mos.ru/api/1/documents/inspections?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jsanam = anamnes.json()
            filt = []
            for i in range(len(jsanam['documents'])):
                if 'appointmentDate' in jsanam['documents'][i]:
                    date = jsanam['documents'][i]['appointmentDate']
                    if date[0:4] not in filt:
                        filt.append(date[0:4])
            for i in filt:
                card = MDCard(orientation='vertical', size_hint=(1, None), height = 300, md_bg_color=(29/255, 89/255, 242/255, 1), radius= [30])
                layout = RelativeLayout()
                timelab = MDLabel(
                    text = f'Записи за {i[0:4]} год.',
                    theme_text_color= 'Custom',
                    text_color= 'white', 
                    halign='center'
                    )
                timelab.font_size  =  60
                timelab.pos_hint = {'center_x': .5, 'center_y':.5}
                layout.add_widget(timelab)
                card.add_widget(layout)
                card.bind(on_release=self.historyanamnes)
                card.year = i[0:4]
                self.manager.get_screen("history").ids.scrollid.add_widget(card)
            self.manager.current = 'history'

        def myanaliz(*args):
            analiz = s.get(f'https://lk.emias.mos.ru/api/1/documents/analyzes?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jsanaliz = analiz.json()
            for i in range(len(jsanaliz['documents'])):
                print(f'({i})',jsanaliz['documents'][i]['title'])
                print(jsanaliz['documents'][i]['date'])
            prosmotrchoose = int(input('Выберите анализ для просмотра\n'))
            docID = jsanaliz['documents'][prosmotrchoose]['documentId']
            prosmotr = s.get(f'https://lk.emias.mos.ru/api/2/document?ehrId={idus}&documentId={docID}', headers = {'X-Access-JWT': authtoken})
            jspros = prosmotr.json()
            print(jspros['documentHtml'])
        def myldp():
            ldp = s.get(f'https://lk.emias.mos.ru/api/1/documents/research?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jsldp = ldp.json()
            for i in range(len(jsldp['documents'])):
                print(f'({i})',jsldp['documents'][i]['title'])
                print(jsldp['documents'][i]['date'])
                print(jsldp['documents'][i]['muName'])
            prosmotrchoose = int(input('Выберите анализ для просмотра\n'))
            docID = jsldp['documents'][prosmotrchoose]['documentId']
            prosmotr = s.get(f'https://lk.emias.mos.ru/api/2/document?ehrId={idus}&documentId={docID}', headers = {'X-Access-JWT': authtoken})
            jspros = prosmotr.json()
            print(jspros['documentHtml'])
        def myboln():
            print("Не доступно")
        def myspravki():
            spravki = s.get(f'https://lk.emias.mos.ru/api/1/documents/medical-certificates?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jssp = spravki.json()
            print(jssp)
            for i in range(len(jssp['certificates095'])):
                print(f"({i})Справка № 095/у")
                print(jssp['certificates095'][i]['educationalName'])
                print(jssp['certificates095'][i]['muName'])
                print(jssp['certificates095'][i]['medicalEmployeeSpeciality'])
                print(jssp['certificates095'][i]['medicalEmployeeName'])
                print(jssp['certificates095'][i]['dateCreated'])
            prosmotrchoose = int(input("Выберите справку для просмотра\n"))
            docID = jssp['certificates095'][prosmotrchoose]['documentId']
            prosmotr = s.get(f'https://lk.emias.mos.ru/api/2/document?ehrId={idus}&documentId={docID}', headers = {'X-Access-JWT': authtoken})
            jspros = prosmotr.json()
            hti = Html2Image()
            html = jspros['documentHtml']
            hti.screenshot(html_str=html, save_as='page.png')
        def mystacionar():
            stacionar = s.get(f'https://lk.emias.mos.ru/api/1/documents/epicrisis?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jsstac = stacionar.json()
            for i in range(len(jsstac['documents'])):
                print(f'({i})',jsstac['documents'][i]['organisation'])
                print(jsstac['documents'][i]['dischargeDate'])
            prosmotrchoose = int(input('Выберите выписку для просмотра\n'))
            docID = jsstac['documents'][prosmotrchoose]['documentId']
            prosmotr = s.get(f'https://lk.emias.mos.ru/api/2/document?ehrId={idus}&documentId={docID}', headers = {'X-Access-JWT': authtoken})
            jspros = prosmotr.json()
            print(jspros['documentHtml'])
        def myrecepies():
            recepies = s.get(f'https://lk.emias.mos.ru/api/2/receipt?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jsrec = recepies.json()
            for i in range(len(jsrec['receipts'])):
                print(f'({i})',jsrec['receipts'][i]['medicineName'])
                print('Выписан',jsrec['receipts'][i]['prescriptionDate'])
                print('Просрочен',jsrec['receipts'][i]['expirationDate'])
                if jsrec['receipts'][i]['prescriptionStatus'] == 'expired':
                    print("Просрочен")
                else:
                    print('Действует')
            prosmotrchoose = int(input('Выберите рецепт для просмотра\n'))
            docID = jsrec['receipts'][prosmotrchoose]['prescriptionNumber']
            prosmotr = s.get(f'https://lk.emias.mos.ru/api/2/document?ehrId={idus}&documentId={docID}', headers = {'X-Access-JWT': authtoken})
            jspros = prosmotr.json()
            print(jspros['documentHtml'])
                
        def myemergency():
            emergency = s.get(f'https://lk.emias.mos.ru/api/1/documents/ambulance?ehrId={idus}&shortDateFilter=all_time', headers = {'X-Access-JWT': authtoken})
            jsemg = emergency.json()
            for i in range(len(jsemg['documents'])):
                print(f'({i})',jsemg['documents'][i]['diagnosis'])
                print(jsemg['documents'][i]['callDate'])
            prosmotrchoose = int(input('Выберите рецепт для просмотра\n'))
            docID = jsemg['documents'][prosmotrchoose]['documentId']
            prosmotr = s.get(f'https://lk.emias.mos.ru/api/2/document?ehrId={idus}&documentId={docID}', headers = {'X-Access-JWT': authtoken})
            jspros = prosmotr.json()
            print(jspros['documentHtml'])
        if id == 1:
            covidtest()
        elif id == 2:
            myvacine()
        elif id == 3:
            myanamnes()
        elif id == 4:
            myanaliz()
        elif id == 5:
            myboln()
        elif id == 6:
            myldp()
        elif id == 7:
            myspravki()
        elif id == 8:
            mystacionar()
        elif id == 9:
            myrecepies()
        elif id == 10:
            myemergency()
class History(Screen):
    pass
class AlterApp(MDApp):
    def build(self):
        global day, sm, types,  year, s,  month, verifcode,userid, login,appID, specID, recpID, resID, complID, perenosEnd, perenosStart, docid, Twofactorverifcode, password, result, curuserid, polic, names, sure, male, age, idus, authtoken, counts, oms, bdates, ref, ass, spec, doclist,vrachchoose, speclist, datespec, create, cancel, shift, info
        
        #omsscreen

        day = None
        year = None
        month = None
        
        #mosscreen

        counts = 59
        Twofactorverifcode = None
        verifcode = None
        login = None
        password = None
        
        #universal
        s = None
        perenosEnd = None
        perenosStart = None
        bdates = None
        result = None
        polic = None
        curuserid = None
        idus = None
        authtoken = None
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
        types = None
        zapisvibor = None
        
        #mosscreen

        names = None
        sure = None
        male = None
        age = None

        sm = ScreenManager()
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
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return sm

if __name__ == '__main__':
    AlterApp().run()
#5494499745000410 1088989771000020