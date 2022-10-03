from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RoundedRectangularElevationBehavior,
)

import re

Window.fullscreen = True
Window.maximize()



KV = '''

ScreenManager:
    ENTERScreen:
    OMSScreen:
    MOSScreen:
<ENTERScreen>:
    name: 'enter'
    email: email_input
    password: text_field
    Image:
        source: 'bg.png'
        allow_stretch: True
    RelativeLayout:
        MDLabel:
            text: "Добро пожаловать!"
            bold: True
            font_name: 'roboto'
            font_size: 45
            pos_hint: {'center_x': .5, 'center_y': 0.92}
            halign: 'center'
        MDLabel:
            text: "Для использования АльТер"
            bold: True
            font_name: 'roboto'
            font_size: 45
            pos_hint: {'center_x': .5, 'center_y': 0.88}
            halign: 'center'
        MDLabel:
            text: "необходимо авторизоваться в [color=#006ad4]EMIAS[/color]"
            bold: True
            font_size: 45
            font_name: 'roboto'
            markup: True
            pos_hint: {'center_x': .5, 'center_y': 0.84}
            halign: 'center'
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .65}
            size_hint: .2, .25
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDTextField:
                    id: email_input
                    hint_text: "Логин"
                    mode: "fill"
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    font_name: 'roboto'
                    font_size: 30
                    helper_text: "mymail@mail.ru"
                    helper_text_mode: "on_focus"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    size_hint: 1, .20
                    font_size: 30
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .50}
                    mode: "fill"

                    icon_left: "key-variant"
                MDFillRoundFlatButton:
                    text: "Войти в EMIAS"
                    elevation: 4.5
                    shadow_offset: 0, 6
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: 45
                    size_hint: .8, .27
                    md_bg_color: 0/255, 106/255, 240/255
                    pos_hint: {'center_x': .5, 'center_y': .20}
                    bold: True
                    on_press: root.check()
        MDSeparator:
            pos_hint: {'center_x': .435, 'center_y': .4888}
            size_hint_x: .1
            color: 128/255, 128/255, 128/255
        MDLabel:
            text: "[color=#808080]ИЛИ[/color]"
            bold: True
            markup: True
            font_name: 'roboto'
            font_size: 30
            pos_hint: {'center_x': .5, 'center_y': .4888}
            halign: 'center'
        MDSeparator:
            pos_hint: {'center_x': .565, 'center_y': .4888}
            size_hint_x: .1
            color: 128/255, 128/255, 128/255

        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .35}
            size_hint: .2, .20
            MDRelativeLayout:
                orientation: 'horizontal'
                MDFillRoundFlatButton:
                    text: "По полису ОМС"
                    md_bg_color: 0/255, 106/255, 240/255
                    bold: True
                    font_size: 35
                    font_name: 'roboto'
                    on_press: root.oms()
                    ripple_color: app.theme_cls.primary_color
                    size_hint: .6, .3
                    pos_hint: {'center_x': .38, 'center_y': 0.70}
                MDFillRoundFlatButton:
                    text: "MOS.RU"
                    md_bg_color: 0.8, 0, 0.1, 1
                    font_size: 35
                    font_name: 'roboto'
                    on_press: root.mos()
                    ripple_color: 1, 0, 0, 0.1
                    pos_hint: {'center_x': .38, 'center_y': .30}
                    size_hint: .6, .3
                    bold: True
                MDIcon:
                    icon: "emias.png"
                    pos_hint: {'center_x': .8, 'center_y': .70}
                    font_size: 90
                MDIcon:
                    icon: "mos.png"
                    pos_hint: {'center_x': .8, 'center_y': .30}
                    font_size: 90
                    
    
<OMSScreen>:
    name: 'oms'
    MDFillRoundFlatButton:
        text: "Вернуться"
        md_bg_color: 0/255, 106/255, 240/255
        font_size: 45
        on_press: root.getback()
        font_name: 'roboto'
        ripple_color: 1, 0, 0, 0.1
        bold: True
        
<MOSScreen>:
    name: 'mos'
    MDFillRoundFlatButton:
        text: "Вернуться"
        font_name: 'roboto'
        md_bg_color: 0/255, 106/255, 240/255
        font_size: 45
        on_press: root.getback()
        ripple_color: 1, 0, 0, 0.1
        bold: True
        
        
'''
class ENTERScreen(Screen):
    def check(self):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if re.match(pattern, self.email.text) is not None:
            self.email.helper_text_color_normal = 'white'
            self.email.helper_text_color_focus = 'white'
            self.email.helper_text = ""
            if len(self.password.text)>=8:
                self.password.helper_text_color_normal = 'white'
                self.password.helper_text_color_focus = 'white'
                self.password.helper_text = ""
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
        self.manager.current = 'oms'

    def mos(self):
        self.manager.current = 'mos'


    pass
class OMSScreen(Screen):
    def getback(self):
        self.manager.current = 'enter'
    pass
class MOSScreen(Screen):
    def getback(self):
        self.manager.current = 'enter'
    pass
class AlterApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ENTERScreen(name='enter'))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(MOSScreen(name="mos"))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


AlterApp().run()
# E0FFFF
# 00CED1 BACKGROUND
