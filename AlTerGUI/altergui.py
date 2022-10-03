from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager

import re

Window.fullscreen = True
Window.maximize()



KV = '''

ScreenManager:
    ENTERScreen:
    OMSScreen:
    MOSScreen:

<ENTERScreen>:
    name: 'ENTER'
    email: email_input
    password: text_field
    FloatLayout:
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .5}
            size_hint: .2, .6
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, .7
                MDLabel:
                    text: "Авторизация"
                    bold: True
                    size_hint: 1, 1
                    font_size: 45
                    pos_hint: {'center_x': .5, 'center_y': 0.9}
                    halign: 'center'
                MDTextField:
                    id: email_input
                    hint_text: "Логин"
                    mode: "fill"
                    pos_hint: {'center_x': .5, 'center_y': .7}
                    size_hint_y: .2
                    font_size: 30
                    helper_text: "mymail@mail.ru"
                    helper_text_mode: "on_focus"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: 30
                    pos_hint: {'center_x': .5, 'center_y': .45}
                    mode: "fill"
                    size_hint_y: .2
                    icon_left: "key-variant"

                MDFillRoundFlatButton:
                    text: "Войти в систему"
                    elevation: 4.5
                    shadow_offset: 0, 6
                    ripple_color: app.theme_cls.primary_color
                    size_hint: 0.8, .15
                    font_size: 45
                    md_bg_color: app.theme_cls.primary_dark
                    pos_hint: {'center_x': .5, 'center_y': .23}
                    bold: True
                    on_press: root.check()
                MDLabel:
                    text:"Войти с помощью:"
                    bold: True
                    font_size: 25
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': 0.1}
                    halign: 'center'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, .1
                MDFillRoundFlatButton:
                    text: "Полиса ОМС"
                    md_bg_color: app.theme_cls.primary_dark
                    bold: True
                    font_size: 25
                    on_press: root.oms()
                    ripple_color: app.theme_cls.primary_color
                    size_hint: .1, .8
                    pos_hint: {'center_x': .3, 'center_y': .8}
                MDFillRoundFlatButton:
                    text: "MOS.RU"
                    md_bg_color: 0.8, 0, 0.1, 1
                    font_size: 45
                    on_press: root.mos()
                    ripple_color: 1, 0, 0, 0.1
                    pos_hint: {'center_x': .3, 'center_y': .8}
                    size_hint: .1, .8
                    bold: True


<OMSScreen>:
    name: 'oms'
    MDLabel:
        text: "text"
        
<MOSScreen>:
    name: 'mos'
    MDLabel:
        text: "text"
        
        

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
    pass
class MOSScreen(Screen):
    pass
class AlterApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ENTERScreen(name='ENTER'))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(MOSScreen(name="mos"))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


AlterApp().run()
# E0FFFF
# 00CED1 BACKGROUND
