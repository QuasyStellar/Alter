from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.behaviors import ButtonBehavior


from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RoundedRectangularElevationBehavior,
)

import re

Window.fullscreen = True
Window.size = (1920, 1080)
#Window.maximize()



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
                    on_press: root.mos()
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
                    on_press: root.oms()
                    Image:
                        source: 'oms.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 362, 65
                    
                
                    
    
<OMSScreen>:
    name: 'oms'
    MDFillRoundFlatButton:
        text: "На экран авторизации"
        pos_hint: {'center_x': .1, 'center_y': .92}
        font_name: 'roboto'
        font_size: dp(30)
        size_hint_y: .1
        md_bg_color: 0/255, 106/255, 240/255
        on_press: root.getback()
        ripple_color: 1, 0, 0, 0.1
        bold: True
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
                    text: "Вход по полису ОМС:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: email_input
                    hint_text: "Номер полиса"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "Например, 7100 0000 0000 0000"
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
                MDFillRoundFlatButton:
                    text: "Войти"
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: 45
                    size_hint: .8, .1
                    md_bg_color: 0/255, 106/255, 240/255
                    pos_hint: {'center_x': .5, 'center_y': .25}
                    bold: True
                    on_press: root.check()
                MDLabel:
                    text: "[color=#808080]Авторизируясь по полису вам будет доступен не полный функционал![/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .10}
                    halign: 'center'
        
<MOSScreen>:
    name: 'mos'
    MDFillRoundFlatButton:
        text: "На экран авторизации"
        pos_hint: {'center_x': .1, 'center_y': .92}
        font_name: 'roboto'
        font_size: dp(30)
        size_hint_y: .1
        md_bg_color: 0/255, 106/255, 240/255
        on_press: root.getback()
        ripple_color: 1, 0, 0, 0.1
        bold: True
        
        
'''
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
