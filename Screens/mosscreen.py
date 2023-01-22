import sys
import time
import datetime
from kivy.properties import DictProperty, ObjectProperty
import threading
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
import requests
import json
from threading import Event
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class MOSScreen(Screen):
    def on_touch_down(self, touch=None):
        print('touch')
        def inactive(*args):
            self.manager.get_screen('oms').ids.policy.text =""
            self.manager.get_screen('oms').day = None
            self.manager.get_screen('oms').year = None
            self.manager.get_screen('oms').month = None
            self.manager.get_screen('oms').manager.current = 'enter'
            self.manager.get_screen('oms').ids.counts.text_color ='white'
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            try:
                if self.manager.get_screen('timetable').children[0].check == True:
                        self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            except:
                None
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            x = ToggleButtonBehavior.get_widgets('x')
            for i in x:
                i.state = 'normal'
            y = ToggleButtonBehavior.get_widgets('y')
            for i in y:
                i.state = 'normal'
            z = ToggleButtonBehavior.get_widgets('z')
            for i in z:
                i.state = 'normal'
            self.manager.get_screen('mos').check(flag=True)
            self.manager.current = 'afk'

        if self.manager.get_screen('enter').timer is not None:
            self.manager.get_screen('enter').timer.cancel()
        self.manager.get_screen('enter').timer = Clock.schedule_once(inactive, 300)
        if touch !=None:
            return super(Screen, self).on_touch_down(touch)

    def mosfunc(self, event, width, height):
        t = threading.Thread(
            target=self.open_moslogin, args=[event, width, height], daemon=True
        )
        if not t.is_alive():
            t.start()

    def open_moslogin(self, event, width, height):
        chrome_options = Options()
        chrome_options.add_argument("--app=https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
       	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
        chrome_options.add_argument(f"window-size={width},{height}")
        chrome_options.add_argument(f'window-position={int(width*0.56)},{int(height*0.05)}')
        print(f'{int(width/0.1)},{int(height/0.1)}')
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        driver = webdriver.Chrome(
            options=chrome_options
        )
        try:
            while driver.current_url !="https://lk.emias.mos.ru/medical-records":
                if event.is_set():
                    driver.quit()
                    sys.exit()
                time.sleep(1)
            else:
                driver.minimize_window()
                time.sleep(5) 
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
                names = jsdata["profile"]['firstName']
                if jsdata["profile"]['gender'] == 'MALE':
                    gender = 0
                else:
                    gender = 1
                sure = jsdata["profile"]['middleName'] +" "+jsdata["profile"]['lastName']
                times = datetime.datetime.strptime(bdates, "%Y-%m-%d")
                year = times.strftime("%Y")
                month = times.strftime('%m')
                day = times.strftime('%d')
                age = f"{day}.{month}.{year}"

                s = requests.Session()
                for cookie in driver.get_cookies():
                    c = {cookie["name"]: cookie["value"]}
                    s.cookies.update(c)
                self.succ(names, sure, age, idus, authtoken, oms, bdates, s, gender)
                driver.quit()
        except Exception as ex:
            self.mosfunc(event, width, height)
            driver.quit()
            sys.exit()

    @mainthread
    def succ(self, names, sure, age, idus, authtoken, oms, bdates, s, gender):
        self.manager.current = "mosloged"
        self.manager.get_screen("mosloged").ids.authname.text = f'{names} {sure}'
        self.manager.get_screen("mosloged").age = age
        self.manager.get_screen("mosloged").gender = gender
        self.manager.get_screen("lkcard").age = age
        self.manager.get_screen("lkcard").gender = gender
        self.manager.get_screen("lkcard").idus = idus
        self.manager.get_screen("lkcard").authtoken = authtoken
        self.manager.get_screen("decrypt").age = age
        self.manager.get_screen("decrypt").gender = gender
        self.manager.get_screen("decrypt").idus = idus
        self.manager.get_screen("decrypt").authtoken = authtoken
        self.manager.get_screen("decrypt").s = s
        self.manager.get_screen("priv").idus = idus
        self.manager.get_screen("priv").authtoken = authtoken
        self.manager.get_screen("lkcard").s = s
        self.manager.get_screen("priv").s = s
        self.manager.get_screen("loged").oms = oms
        self.manager.get_screen('loged').bdates = bdates
        self.manager.get_screen('loged').types = 'mos'
        self.manager.get_screen('priem').cur = 'mosloged'
    def back(self):
        self.manager.current = "enter"

    def check(self, flag=None):
        if flag == None:
            self.event = Event()
            self.mosfunc(self.event, self.widths, self.heights)
        else:
            try:
                self.event.set()
            except:
                None
class HelpScreen(Screen):
    def on_touch_down(self, touch=None):
        print('touch')
        def inactive(*args):
            self.manager.get_screen('oms').ids.policy.text =""
            self.manager.get_screen('oms').day = None
            self.manager.get_screen('oms').year = None
            self.manager.get_screen('oms').month = None
            self.manager.get_screen('oms').manager.current = 'enter'
            self.manager.get_screen('oms').ids.counts.text_color ='white'
            self.manager.get_screen('zapisi').ids.scrollid.clear_widgets()
            self.manager.get_screen('perenos').ids.scrollid.clear_widgets()
            self.manager.get_screen('timetable').ids.lay.clear_widgets()
            if self.manager.get_screen('timetable').children[0].check == True:
                self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            self.manager.get_screen('prik').ids.lay.clear_widgets()
            self.manager.get_screen('napr').ids.scrollid.clear_widgets()
            x = ToggleButtonBehavior.get_widgets('x')
            for i in x:
                i.state = 'normal'
            y = ToggleButtonBehavior.get_widgets('y')
            for i in y:
                i.state = 'normal'
            z = ToggleButtonBehavior.get_widgets('z')
            for i in z:
                i.state = 'normal'
            self.manager.get_screen('mos').check(flag=True)
            self.manager.current = 'afk'

        if self.manager.get_screen('enter').timer is not None:
            self.manager.get_screen('enter').timer.cancel()
        self.manager.get_screen('enter').timer = Clock.schedule_once(inactive, 300)
        if touch !=None:
            return super(Screen, self).on_touch_down(touch)
    pass