import sys
import time
import datetime
import locale
locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
import threading
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class MOSScreen(Screen):
    dialogerror = None
    mobiles = None
    mobileerror = None
    waiterror = None
    factor = None
    timeclock = None
    def mosfunc(self):
        t = threading.Thread(
            target=self.open_moslogin, args=[], daemon=True
        )
        if not t.is_alive():
            t.start()

    def open_moslogin(self):
        chrome_options = Options()
        chrome_options.add_argument("--app=https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
       	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
        chrome_options.add_argument("window-size=600,960")
        chrome_options.add_argument('window-position=960,150')
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
                year = int(times.strftime("%Y"))
                month = int(times.strftime('%m'))
                day = int(times.strftime('%d'))
                age = f"{day}.{month}.{year}"

                s = requests.Session()
                for cookie in driver.get_cookies():
                    c = {cookie["name"]: cookie["value"]}
                    s.cookies.update(c)
                self.succ(names, sure, age, idus, authtoken, oms, bdates, s, gender)
                driver.quit()
        except Exception as ex:
            print(ex)
            driver.quit()
            self.err()
            sys.exit()


    @mainthread
    def err(self):
        self.error_dialog()
        self.manager.current = "mos"
    @mainthread
    def succ(self, names, sure, age, idus, authtoken, oms, bdates, s, gender):
        self.manager.current = "mosloged"
        self.manager.get_screen("mosloged").ids.authname.text = names
        self.manager.get_screen("mosloged").ids.sures.text = sure
        self.manager.get_screen("mosloged").ids.ages.text = age
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
    def back(self):
        self.manager.current = "enter"

    def error_dialog(self):
        if not self.dialogerror:
            self.dialogerror = MDDialog(
                text="Авторизация прервана.",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        md_bg_color="ff0000",
                        on_release=lambda _: self.dialogerror.dismiss(),
                    )
                ],
            )
        self.dialogerror.open()


    def check(self):
        self.mosfunc()
        self.manager.current = "load"
        if self.timeclock == None:
            self.timeclock = Clock.schedule_interval(self.manager.get_screen('mosloged').update, 1)
