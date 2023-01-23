import sys
from kivy.properties import DictProperty, ObjectProperty
import threading
from kivy.clock import Clock, mainthread
from kivymd.uix.screen import MDScreen as Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.effects.fadingedge.fadingedge import FadingEdgeEffect
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import FadeTransition
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField
import requests

      

class OMSScreen(Screen):
    def on_touch_down(self, touch=None):
        
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

    timeclocks = None
    day = None
    year = None
    month = None
    def back(self):
        self.ids.policy.text =""
        self.day = None
        self.year = None
        self.month = None
        self.manager.current = 'enter'
        self.ids.counts.text_color ='white'
        x = ToggleButtonBehavior.get_widgets('x')
        for i in x:
            i.state = 'normal'
        y = ToggleButtonBehavior.get_widgets('y')
        for i in y:
            i.state = 'normal'
        z = ToggleButtonBehavior.get_widgets('z')
        for i in z:
            i.state = 'normal'
    @mainthread
    def error(self):
        self.manager.current = "omserror"
        self.day = None
        self.year = None
        self.month = None
        x = ToggleButtonBehavior.get_widgets('x')
        for i in x:
            i.state = 'normal'
        y = ToggleButtonBehavior.get_widgets('y')
        for i in y:
            i.state = 'normal'
        z = ToggleButtonBehavior.get_widgets('z')
        for i in z:
            i.state = 'normal'
    @mainthread
    def unkerror(self):
        self.manager.current = "omserrorunk"
        self.day = None
        self.year = None
        self.month = None
        x = ToggleButtonBehavior.get_widgets('x')
        for i in x:
            i.state = 'normal'
        y = ToggleButtonBehavior.get_widgets('y')
        for i in y:
            i.state = 'normal'
        z = ToggleButtonBehavior.get_widgets('z')
        for i in z:
            i.state = 'normal'
    @mainthread
    def succ(self, policy, bdate):
        self.ids.policy.text =""
        self.day = None
        self.year = None
        self.month = None
        self.ids.counts.text_color ='white'
        x = ToggleButtonBehavior.get_widgets('x')
        for i in x:
            i.state = 'normal'
        y = ToggleButtonBehavior.get_widgets('y')
        for i in y:
            i.state = 'normal'
        z = ToggleButtonBehavior.get_widgets('z')
        for i in z:
            i.state = 'normal'
        self.manager.current = "loged"
        policnum = f"{policy[0:4] + ' **** **** ' + policy[12:16]}"
        self.manager.get_screen("loged").ids.authname.text = policnum
        self.manager.get_screen("loged").oms = policy
        self.manager.get_screen('loged').bdates = bdate
        self.manager.get_screen('loged').types = 'oms'
        self.manager.get_screen('priem').cur = 'omsloged'

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
            self.unkerror()
            print(ex)
        sys.exit()

    def omslogin(self):
        if len(self.ids.policy.text) < 16 or len(self.ids.policy.text) > 16:
            None
        elif self.day !=None and self.month !=None and self.year !=None:
            bdate = f'{self.year}-{self.month}-{self.day}'
            self.omsfunc(self.ids.policy.text, bdate)
            self.manager.current = "load"
        else:
            None

    def cou(self):
        self.ids.counts.text = f'{len(self.ids.policy.text)}/16'
        if 16>len(self.ids.policy.text) or len(self.ids.policy.text)>16:
            self.ids.counts.text_color = get_color_from_hex("#72C3AC")
        else:
            self.ids.counts.text_color = get_color_from_hex("#72C3AC")
    def days(self, instance):
        if instance.state == 'down':
            self.day = str(instance.date).zfill(2)
        else:
            self.day = None
    def months(self, instance):
        if instance.state == 'down':
            if instance.month == 'Январь':
                self.month = '01'
            if instance.month == 'Февраль':
                self.month = '02'
            if instance.month == 'Март':
                self.month = '03'
            if instance.month == 'Апрель':
                self.month = '04'
            if instance.month == 'Май':
                self.month = '05'
            if instance.month == 'Июнь':
                self.month = '06'
            if instance.month == 'Июль':
                self.month = '07'
            if instance.month == 'Август':
                self.month = '08'
            if instance.month == 'Сентябрь':
                self.month = '09'
            if instance.month == 'Октябрь':
                self.month = '10'
            if instance.month == 'Ноябрь':
                self.month = '11'
            if instance.month == 'Декабрь':
                self.month = '12'
        else:
            self.month = None


    def years(self, instance):
        if instance.state == 'down':
            self.year = instance.year
        else:
            self.year = None
    pass

class OMSErrorScreen(Screen):
    def on_touch_down(self, touch=None):
        
        def inactive(*args):
            self.manager.get_screen('oms').ids.policy.text =""
            self.manager.get_screen('oms').day = None
            self.manager.get_screen('oms').year = None
            self.manager.get_screen('oms').month = None
            self.manager.get_screen('oms').manager.current = 'enter'
            self.manager.get_screen('oms').ids.counts.text_color ='white'
            try:
                if self.manager.get_screen('timetable').children[0].check == True:
                        self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            except:
                None
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

class OMSErrorUnkScreen(Screen):
    def on_touch_down(self, touch=None):
        
        def inactive(*args):
            self.manager.get_screen('oms').ids.policy.text =""
            self.manager.get_screen('oms').day = None
            self.manager.get_screen('oms').year = None
            self.manager.get_screen('oms').month = None
            self.manager.get_screen('oms').manager.current = 'enter'
            self.manager.get_screen('oms').ids.counts.text_color ='white'
            try:
                if self.manager.get_screen('timetable').children[0].check == True:
                        self.manager.get_screen('timetable').remove_widget(self.manager.get_screen('timetable').children[0])
            except:
                None
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
    def back(self):
        if self.manager.get_screen('loged').types == None:
            self.manager.current = 'oms'
        elif self.manager.get_screen('loged').types == 'oms':
            self.manager.current = 'loged'
        else:
            self.manager.current = 'mosloged'

    pass