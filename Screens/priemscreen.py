
import requests
from selenium.webdriver.chrome.options import Options
import time
from seletools.indexeddb import IndexedDB
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from kivy.uix.screenmanager import Screen
import requests
class Priem(Screen):
	def helzy(self):
		dc = DesiredCapabilities.CHROME
		dc["goog:loggingPrefs"] = {"browser": "ALL"}
		app = requests.post('https://helzy.ru/api/v1/sessions').json()['appSessionId']
		chrome_options = Options()
		chrome_options.add_argument("--app=about:blank")
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
		driver.get('https://helzy.ru/anamnesis/1')
		driver.execute_script("document.body.style.zoom='200%'")
		driver.maximize_window()

		try:
		    while (driver.current_url != 'https://helzy.ru/report/1') and (driver.current_url != 'https://helzy.ru/'):
		        None
		    else:
		        if driver.current_url == 'https://helzy.ru/':
		            print('Отмена')
		            driver.quit()
		        else:
		            driver.quit()
		            report = requests.get('https://helzy.ru/api/v1/reports',
		                                  headers={'appsessionid': app}).json()
		            print(report)
		except:
		    print("Окно закрыто")