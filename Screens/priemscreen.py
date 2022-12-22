import requests
from kivy.uix.screenmanager import Screen
import locale
locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivymd.uix.label import MDLabel
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
import requests
from selenium.webdriver.chrome.options import Options
import time
from seletools.indexeddb import IndexedDB
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from kivy.uix.screenmanager import Screen
import requests
class Priem(Screen):
	dialogerror = None
	def report(self, report):
		dialog = None
		scrollview = ScrollView(size_hint=(.9, None))
		text = f"[b][size=45]{report['summary']['title'].replace('#', '')}[/size][/b]\n[size=25]{report['summary']['detail'].replace('#', '')}[/size]\n"
		for i in range(len(report['diseases'])):
			if int(report['diseases'][i]['probability'])>=50:
				prob = f"[b][color=ff0000]{report['diseases'][i]['probability'].replace('#', '')}[/color][/b]"
			else:
				prob = report['diseases'][i]['probability']
			text += f"[b][size=35]{report['diseases'][i]['title'].replace('#', '')}[/size][/b]\n[size=25]{report['diseases'][i]['detail'].replace('#', '')}[/size]\nВероятность: [size=35][i]{prob}[/i][/size]"
		lab = MDLabel(
		    text =text,
		    markup= True,
		    adaptive_height=True
		    )

		lab.size_hint_y = None        
		lab.text_size= lab.width, None        
		lab.height = lab.texture_size[1]
		scrollview.height = 900

		scrollview.add_widget(lab)
		but = MDRaisedButton(
		    text="Выйти",
		    on_release=lambda _: self.dialog.dismiss(),
		    size_hint=(None, None)
		)
		but.height = 150
		but.width = 200
		but.font_size = 30
		self.dialog = MDDialog(
		    type='custom',
		    content_cls=scrollview,
		    size_hint_x=.5,
		    elevation=0,
		    buttons=[
		        but,
		    ]
		)
		self.dialog.open()

	def error_dialog(self):
		if not self.dialogerror:
			self.dialogerror = MDDialog(
		        text="Первичный прием прерван",
		        buttons=[
		            MDFillRoundFlatButton(
		                text="ОК",
		                md_bg_color="ff0000",
		                on_release=lambda _: self.dialogerror.dismiss(),
		            )
		        ],
		    )
		self.dialogerror.open()
	def helzy(self):
		def priem(driver):
			driver.get('https://helzy.ru/anamnesis/1')
			driver.execute_script("document.body.style.zoom='200%'")
			driver.maximize_window()
			try:
			    while (driver.current_url != 'https://helzy.ru/report/1') and (driver.current_url != 'https://helzy.ru/'):
			        None
			    else:
			        if driver.current_url == 'https://helzy.ru/':
			          	priem(driver)
			        else:
			            driver.quit()
			            reports = requests.get('https://helzy.ru/api/v1/reports',
			                                  headers={'appsessionid': app}).json()
			            self.report(reports)
			except:
			    self.error_dialog()

		dc = DesiredCapabilities.CHROME
		dc["goog:loggingPrefs"] = {"browser": "ALL"}
		app = requests.post('https://helzy.ru/api/v1/sessions').json()['appSessionId']
		chrome_options = Options()
		chrome_options.add_argument("--app=https://helzy.ru")
		chrome_options.add_argument('--kiosk')
		chrome_options.add_experimental_option("useAutomationExtension", False)
		chrome_options.add_experimental_option(
		    "excludeSwitches", ["enable-automation"])
		chrome_options.add_argument('window-position=5000,5000')
		chrome_options.add_experimental_option('prefs', {
		    'credentials_enable_service': False,
		    'profile': {
		        'password_manager_enabled': False
		    }
		})


		driver = webdriver.Chrome(
		    options=chrome_options,
		    desired_capabilities=dc
		)
		driver.minimize_window()
		driver.get('https://helzy.ru/')
		idb = IndexedDB(driver, "ngStorage", 1)
		idb.add_value("localStorage", "helzyCheckId", app)
		priem(driver)