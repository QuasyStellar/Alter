import re
import time
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker

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
                    on_release: root.omslogin()
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
    MDFillRoundFlatIconButton:
        text: "Войти в полную версию"
        bold: True
        markup: True
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .86}
        font_size: dp(30)
        size_hint: .2,.05
        right_icon: "delete"
        md_bg_color: 0/255, 106/255, 240/255
        on_release: root.moslogin()
        ripple_color: 1, 1, 1, 1
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
    def exits(self):
        self.manager.current = 'enter'
    pass


class MOSScreen(Screen):
    def getback(self):
        self.manager.current = 'enter'


class OMSLoged(Screen):
    

    pass



class AlterApp(MDApp):
    def build(self):
        global day
        global year
        global month
        day  = None
        year = None
        month = None
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
