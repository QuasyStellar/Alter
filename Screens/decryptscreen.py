import os
import datetime
import re
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from kivy.uix.screenmanager import Screen, SlideTransition
import locale
from kivy.uix.image import Image
locale.setlocale(locale.LC_ALL, '')
from kivy.properties import DictProperty, ObjectProperty
from kivymd.uix.label import MDLabel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from kivymd.uix.card import MDCard
class Decrypt(Screen):
    def OKAKLK(self, instance):
        prosmotr = self.s.get(
            f'https://lk.emias.mos.ru/api/2/document?ehrId={self.idus}&documentId={instance.docid}',
            headers={'X-Access-JWT': self.authtoken})
        jspros = prosmotr.json()
        html = jspros['documentHtml'].replace('\n', '')
        self.OKAK(html, self.age, self.gender, instance.date)
    def OAMLK(self, instance):
        prosmotr = self.s.get(
            f'https://lk.emias.mos.ru/api/2/document?ehrId={self.idus}&documentId={instance.docid}',
            headers={'X-Access-JWT': self.authtoken})
        jspros = prosmotr.json()
        html = jspros['documentHtml'].replace('\n', '')
        self.OAM(html, self.age, self.gender, instance.date)
    def myanaliz(self):
        analiz = self.s.get(f'https://lk.emias.mos.ru/api/1/documents/analyzes?ehrId={self.idus}&shortDateFilter=all_time',
                       headers={'X-Access-JWT': self.authtoken})
        jsanaliz = analiz.json()
        for i in range(len(jsanaliz['documents'])):
            card = MDCard(orientation='vertical', size_hint=(1, None), height=300,
                      md_bg_color=(29 / 255, 89 / 255, 242 / 255, 1), radius=[30])
            layout = RelativeLayout()
            title = MDLabel(
                text=f"{jsanaliz['documents'][i]['title']}",
                theme_text_color='Custom',
                text_color='white',
            )
            title.font_size = 45
            title.pos_hint = {'center_x': .55, 'center_y': .8}
            layout.add_widget(title)
            time = datetime.datetime.fromisoformat(jsanaliz['documents'][i]['date'])
            timelab = MDLabel(
                text=f'{time.strftime("%a, %d %b %Y")}',
                theme_text_color='Custom',
                text_color='white',
            )
            timelab.font_size = 35
            timelab.pos_hint = {'center_x': 1.2, 'center_y': .65}
            if 'ОАК' in jsanaliz['documents'][i]['title'] or 'Общий клинический анализ крови' in jsanaliz['documents'][i]['title'] or ('кров' in jsanaliz['documents'][i]['title'] and 'общ' in jsanaliz['documents'][i]['title']):
                but = MDRaisedButton(
                    text="Расшифровать анализ",
                    on_release=self.OKAKLK,
                )
                but.pos_hint={'center_x': .7, 'center_y': .25}
                but.docid = jsanaliz['documents'][i]['documentId']
                but.date = jsanaliz['documents'][i]['date']
                layout.add_widget(but)
            elif 'ОАМ' in jsanaliz['documents'][i]['title'] or 'Общий клинический анализ мочи' in jsanaliz['documents'][i]['title'] or 'Клинический анализ мочи' in jsanaliz['documents'][i]['title'] or ('моч' in jsanaliz['documents'][i]['title'] and 'анализ' in jsanaliz['documents'][i]['title']):
                but = MDRaisedButton(
                    text="Расшифровать анализ",
                    on_release=self.OAMLK,
                )
                but.pos_hint={'center_x': .7, 'center_y': .25}
                but.docid = jsanaliz['documents'][i]['documentId']
                but.date = jsanaliz['documents'][i]['date']
                layout.add_widget(but)
            layout.add_widget(timelab)
            card.add_widget(layout)
            card.docid = jsanaliz['documents'][i]['documentId']
            card.bind(on_release=self.manager.get_screen('lkcard').documentview)
            self.ids.scrollid.add_widget(card)
        self.manager.current = 'decrypt'
    def OKAK(self, html, age, gender, date):
        try:
            today = datetime.date.today()
            time = datetime.datetime.strptime(age, "%Y.%m.%d") 
            year = int(time.strftime("%Y"))
            month = int(time.strftime('%m'))
            day = int(time.strftime('%d'))
            age = today.year - year - ((today.month, today.day) < (month, day))
            data = []
            list_header = []
            soup = BeautifulSoup(html,'html.parser')
            header = soup.find_all("table")[0].find("tr")
            for items in header:
                try:
                    list_header.append(items.get_text())
                except:
                    continue
            HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
            for element in HTML_data:
                sub_data = []
                for sub_element in element:
                    try:
                        sub_data.append(sub_element.get_text())
                    except:
                        continue
                data.append(sub_data)
            dataFrame = pd.DataFrame(data = data, columns = list_header)
            jsanaliz = json.loads(dataFrame.to_json(orient='index'))
            wbc = None
            rbc = None
            hgb = None
            htc = None
            mcv = None
            mch = None
            mchc = None
            plt = None
            for i in jsanaliz:
                for j in jsanaliz[i]:
                    if 'Количество лейкоцитов' in jsanaliz[i]['Тест'] or 'WBC' in jsanaliz[i]['Тест'] or 'Лейкоциты' in jsanaliz[i]['Тест']:
                        wbc = jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    if 'RBC' in jsanaliz[i]['Тест'] or 'Эритроциты' in jsanaliz[i]['Тест'] or 'Количество эритроцитов' in jsanaliz[i]['Тест']:
                        rbc = jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    if 'HGB' in jsanaliz[i]['Тест'] or 'Гемоглобин' in jsanaliz[i]['Тест']:
                        hgb = jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    if 'HCT' in jsanaliz[i]['Тест'] or 'Гематокрит' in jsanaliz[i]['Тест']:
                        try:
                            if float(jsanaliz[i]['Результат'])<1:
                                hct = float(jsanaliz[i]['Результат'])*100
                            else:
                                hct = float(jsanaliz[i]['Результат'])
                        except:
                            if float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.'))<1:
                                hct = float(jsanaliz[i]['Результат'].replace(",", '.'))*100
                            else:
                                hct = float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.'))
                        break
                    if 'MCV' in jsanaliz[i]['Тест'] or 'Средний объем эритроцита' in jsanaliz[i]['Тест']:
                        mcv = jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    if 'MCH' in jsanaliz[i]['Тест'] and 'MCHC' not in jsanaliz[i]['Тест'] or 'Среднее содержание гемоглобина в эритроците' in jsanaliz[i]['Тест']:
                        mch = jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    if 'MCHC' in jsanaliz[i]['Тест'] or 'Средняя концентрация гемоглобина в эритроците' in jsanaliz[i]['Тест']:
                        mchc = jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    if 'PLT' in jsanaliz[i]['Тест'] or 'Количество тромбоцитов' in jsanaliz[i]['Тест'] or 'Тромбоциты' in jsanaliz[i]['Тест']:
                        plt= jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
            if wbc != None and  rbc != None and hgb != None and hct !=None and mcv !=None and mch !=None and mchc !=None and plt !=None:
                s = requests.Session()
                s.get('https://helzy.ru/api/v1/analyses/carts')
                jsonreq = {
                  "patient": {
                    "age": age,
                    "gender": gender
                  },
                  "answers": [
                    {
                      "questionnaireId": "c33662be-1ac9-431e-a2a2-f5ce7c1cc992",
                      "items": [
                        {
                          "linkId": "ef6d4b47-87c2-4a63-bf9c-d18843d161e0",
                          "answer": {
                            "type": "ValueDate",
                            "value": date
                          }
                        },
                        {
                          "linkId": "32ebfb5d-6164-4c12-a0b4-caec6a070ddf",
                          "answer": {
                            "code": "1AtPalBW8rN177d14CKsOQ==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "SPMNYNneBIqzGV4e3O/vEA==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "*10^9/л",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=SPMNYNneBIqzGV4e3O/vEA=="
                            },
                            "type": "ValueQuantity",
                            "value": wbc
                          }
                        },
                        {
                          "linkId": "f55f2c8b-df38-41ea-a338-d997beb77ed6",
                          "answer": {
                            "code": "Xtex01/ntKCD0l+1070ybw==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "vNW/3ko1v6Md5M4cX69fHA==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "*10^12/л",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=vNW/3ko1v6Md5M4cX69fHA=="
                            },
                            "type": "ValueQuantity",
                            "value": rbc
                          }
                        },
                        {
                          "linkId": "417d57b4-123d-47c9-acc2-78de607d9049",
                          "answer": {
                            "code": "5S7QgKEmqz/BsIKNUrN4SQ==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "U1VWYg12QPgcaFhsF0K7Sw==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "г/л",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=U1VWYg12QPgcaFhsF0K7Sw=="
                            },
                            "type": "ValueQuantity",
                            "value": hgb
                          }
                        },
                        {
                          "linkId": "d6e3a43e-43ae-4bd0-bace-2b0885cbf52b",
                          "answer": {
                            "code": "oZIh7CciQPlNSz7UUNoHPA==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "PjCVLvP2Wm+Z3KSuAAaOjQ==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "%",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=PjCVLvP2Wm+Z3KSuAAaOjQ=="
                            },
                            "type": "ValueQuantity",
                            "value": hct
                          }
                        },
                        {
                          "linkId": "4ece3e1c-cf17-4a4d-b4b3-2d74e477e639",
                          "answer": {
                            "code": "vTMOSwu336TrjjTnP6n/+g==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "Md2b0SbwccYec3wAywq4hQ==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "fL",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=Md2b0SbwccYec3wAywq4hQ=="
                            },
                            "type": "ValueQuantity",
                            "value": mcv
                          }
                        },
                        {
                          "linkId": "5eb3ccd2-b69a-4dcd-b52b-3f7f135f2cff",
                          "answer": {
                            "code": "hMjjkZsXu8GZdhhyHBBYMg==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "n1hwnM4HLriOxa3U8ACD9A==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "пг",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=n1hwnM4HLriOxa3U8ACD9A=="
                            },
                            "type": "ValueQuantity",
                            "value": mch
                          }
                        },
                        {
                          "linkId": "144e0609-525e-428d-8cae-49eef0fafb40",
                          "answer": {
                            "code": "RljXQokPjufjMoNibhdHwg==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "U1VWYg12QPgcaFhsF0K7Sw==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "г/л",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=U1VWYg12QPgcaFhsF0K7Sw=="
                            },
                            "type": "ValueQuantity",
                            "value": mchc
                          }
                        },
                        {
                          "linkId": "356d9635-6d1e-447e-8248-a381eaf328c3",
                          "answer": {
                            "code": "9AFKfD5CrfAoaQy7xSuaZA==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "SPMNYNneBIqzGV4e3O/vEA==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "*10^9/л",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=SPMNYNneBIqzGV4e3O/vEA=="
                            },
                            "type": "ValueQuantity",
                            "value": plt
                          }
                        }
                      ]
                    }
                  ]}
                s.get('https://helzy.ru/api/v1/analyses/carts')
                s.get('https://helzy.ru/api/v1/analyses/catalog?pageNumber=1&pageSize=100')
                ids= s.cookies.get_dict()['HelzyAnalysesSessionId']
                debug = s.post('https://helzy.ru/api/v1/analyses/carts', json={"analysisId":"c33662be-1ac9-431e-a2a2-f5ce7c1cc992"})
                debug1 = s.post('https://helzy.ru/api/v1/analyses/interpretations', json=jsonreq)
                report = s.get('https://helzy.ru/api/v1/analyses/interpretations/reports').json()
                if 'error' in report:
                    print('Данный анализ не поддерживается, доступно выделение отклонений')
                else:
                    print(report)
            else:
                print('Данный анализ не поддерживается, доступно выделение отклонений.')
        except:
            print('Данный анализ не поддерживается, доступно выделение отклонений.')
    def OAM(self, html, age, gender, date):
        try:
            today = datetime.date.today()
            time = datetime.datetime.strptime(age, "%Y.%m.%d") 
            year = int(time.strftime("%Y"))
            month = int(time.strftime('%m'))
            day = int(time.strftime('%d'))
            age = today.year - year - ((today.month, today.day) < (month, day))
            data = []
            list_header = []
            soup = BeautifulSoup(html,'html.parser')
            header = soup.find_all("table")[0].find("tr")
            for items in header:
                try:
                    list_header.append(items.get_text())
                except:
                    continue
            HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
            for element in HTML_data:
                sub_data = []
                for sub_element in element:
                    try:
                        sub_data.append(sub_element.get_text())
                    except:
                        continue
                data.append(sub_data)
            dataFrame = pd.DataFrame(data = data, columns = list_header)
            jsanaliz = json.loads(dataFrame.to_json(orient='index'))
            protein = None
            bili = None
            gluc = None
            keton = None
            ph = None
            urobili = None
            bact = None
            mush = None
            cryst = None
            leik = None
            erit = None
            for i in jsanaliz:
                for j in jsanaliz[i]:
                    if 'Белок' in jsanaliz[i]['Тест'] or 'белок' in jsanaliz[i]['Тест'] or 'PRO' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                            protein = 'Не обнаружено'
                            proteincode = 'XmXOg59dJnz/v9XelUDt6g=='
                        else:
                            protein = 'Обнаружено'
                            proteincode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                        break
                    if 'Билирубин' in jsanaliz[i]['Тест'] or 'билирубин' in jsanaliz[i]['Тест'] or 'BILT' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                            bili = 'Не обнаружено'
                            bilicode = 'XmXOg59dJnz/v9XelUDt6g=='
                        else:
                            bili = 'Обнаружено в большом количестве'
                            bilicode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                        break
                    if 'Глюкоза' in jsanaliz[i]['Тест'] or 'глюкоза' in jsanaliz[i]['Тест'] or 'GLU' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                            gluc = 'Не обнаружено'
                            gluccode = 'XmXOg59dJnz/v9XelUDt6g=='
                        else:
                            gluc = 'Обнаружено в большом количестве'
                            gluccode = '8qM2SZXflJ8IRKhuEBRMsQ==' 
                        break
                    if 'Кетоновые' in jsanaliz[i]['Тест'] or 'кетон' in jsanaliz[i]['Тест'] or 'KET' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат'] or 16>float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')):
                            keton = 'Не обнаружено'
                            ketoncode = 'XmXOg59dJnz/v9XelUDt6g=='
                        else:
                            keton = 'Обнаружено в большом количестве'
                            ketoncode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                        break
                    if 'Ph' in jsanaliz[i]['Тест'] or 'PH' in jsanaliz[i]['Тест'] or 'pH' in jsanaliz[i]['Тест']:
                        ph = re.sub('[^0-9]', '', jsanaliz[i]['Результат']).replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')
                        break
                    else:
                        ph = 5.5
                    if 'Уробилиноген' in jsanaliz[i]['Тест'] or 'уробилиноген' in jsanaliz[i]['Тест'] or 'уробили' in jsanaliz[i]['Тест'] or 'URO' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат'] or 16>float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')):
                            urobili = 'Не обнаружено'
                            urobilicode = 'XmXOg59dJnz/v9XelUDt6g=='
                        else:
                            urobili = 'Обнаружено в большом количестве'
                            urobilicode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                        break
                    if 'Бактерии' in jsanaliz[i]['Тест'] or 'Бакт' in jsanaliz[i]['Тест'] or 'бактерии' in jsanaliz[i]['Тест'] or 'Бакт' in jsanaliz[i]['Тест']:
                        try:
                            if 26.4>=float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')):
                                bact = 'Не обнаружено'
                                bactcode = 'XmXOg59dJnz/v9XelUDt6g=='
                            else:
                                bact = 'Обнаружено в большом количестве'
                                bactcode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                            break
                        except:
                            if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                                bact = 'Не обнаружено'
                                bactcode = 'XmXOg59dJnz/v9XelUDt6g=='
                            else:
                                bact = 'Обнаружено в большом количестве'
                                bactcode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                            break
                    if 'Дрожжевые' in jsanaliz[i]['Тест'] or 'дрожж' in jsanaliz[i]['Тест'] or 'гриб' in jsanaliz[i]['Тест']:
                        try:
                            if 0==float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.')):
                                mush = 'Не обнаружено'
                                mushcode = 'XmXOg59dJnz/v9XelUDt6g=='
                            else:
                                mush =  'Обнаружено в большом количестве'
                                mushcode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                            break
                        except:
                            if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                                mush = 'Не обнаружено'
                                mushcode = 'XmXOg59dJnz/v9XelUDt6g=='
                            else:
                                mush = 'Обнаружено в большом количестве'
                                mushcode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                            break
                        break
                    else:
                        mush = 'Не обнаружено'
                        mushcode = 'XmXOg59dJnz/v9XelUDt6g=='
                    if 'Кристаллы' in jsanaliz[i]['Тест'] or 'крист' in jsanaliz[i]['Тест'] or 'кристаллы' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                            cryst = 'Не обнаружено'
                            crystcode = 'XmXOg59dJnz/v9XelUDt6g=='
                        else:
                            cryst = 'Обнаружено в большом количестве'
                            crystcode = '8qM2SZXflJ8IRKhuEBRMsQ=='
                        break
                    else:
                        cryst = 'Не обнаружено'
                        crystcode = 'XmXOg59dJnz/v9XelUDt6g=='
                    if 'Количество лейкоцитов' in jsanaliz[i]['Тест'] or 'WBC' in jsanaliz[i]['Тест'] or 'Лейкоциты' in jsanaliz[i]['Тест'] or 'лейкоц' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] and 4 not in jsanaliz[i]['Результат'] and 5 not in jsanaliz[i]['Результат'] and 6 not in jsanaliz[i]['Результат'] and 7 not in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                            leik = 0
                        else:
                            leik = 500
                        break
                    else:
                        leik = 0
                    if 'RBC' in jsanaliz[i]['Тест'] or 'Эритроциты' in jsanaliz[i]['Тест'] or 'эритро' in jsanaliz[i]['Тест']:
                        if 'не обнаружено' in jsanaliz[i]['Результат'] or 'Не обнаружено' in jsanaliz[i]['Результат'] or 'Отриц' in jsanaliz[i]['Результат'] or 'отриц' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or '0' in jsanaliz[i]['Результат'] or 'норм' in jsanaliz[i]['Результат'] or 'Норм' in jsanaliz[i]['Результат']:
                            erit = 0
                        else:
                            erit = float(jsanaliz[i]['Результат'].replace(",", '.').replace('/','.').replace("'", ".").replace(';','.'))
                        break
                    else:
                        erit = 0
            if protein != None and  bili != None and gluc != None and keton !=None and ph !=None and urobili !=None and bact !=None and mush !=None and cryst != None and leik != None and erit != None:
                s = requests.Session()
                jsonreq = {
                  "patient": {
                    "age": "19",
                    "gender": 0
                  },
                  "answers": [
                    {
                      "questionnaireId": "3418e3a0-df22-44d8-871b-cd4f8148f2b9",
                      "items": [
                        {
                          "linkId": "1465716c-f2e1-4529-835e-6b76cec98a87",
                          "answer": {
                            "type": "ValueDate",
                            "value": date
                          }
                        },
                        {
                          "linkId": "a5495407-0479-429d-8ade-ce6490ba2c6e",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": proteincode,
                            "display": protein,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "391454c8-784d-463d-8adb-6904a1718f48",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": bilicode,
                            "display": bili,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "1d36a90a-b3b9-4dfa-9037-07c8c56f1d46",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": gluccode,
                            "display": gluc,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "b7d5ea78-0053-453c-b760-6501a0a1afb6",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": ketoncode,
                            "display": keton,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "d8ea3193-3611-45d6-b6f2-57a1828117bd",
                          "answer": {
                            "code": "tCxlEmdvumqNzncMwp2B+Q==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "type": "ValueQuantity",
                            "value": ph
                          }
                        },
                        {
                          "linkId": "ad4b9c85-837a-4bce-a78a-85a587d481aa",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": urobilicode,
                            "display": urobili,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "d7c7c188-b366-4295-a7ad-ae08e5ff31c7",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": bactcode,
                            "display": bact,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "8c4cd3ec-c76e-4b13-ab8c-e8b42916fa56",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": mushcode,
                            "display": mush,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "317fa7da-9e4a-4e50-b05f-ce20fe13739f",
                          "answer": {
                            "system": "E+mbJrBpZqx6NRKva98rV7xe0s9DpAisWc3jfgCEM/c=",
                            "code": crystcode,
                            "display": cryst,
                            "type": "ValueCoding"
                          }
                        },
                        {
                          "linkId": "4bc42c09-80e9-4797-b032-5cc322369ce5",
                          "answer": {
                            "code": "bMmKKJro9EQlxiyYXxVVnQ==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "ITFgwPQzfXp7R25zIk25iw==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "клет/мкл",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=ITFgwPQzfXp7R25zIk25iw=="
                            },
                            "type": "ValueQuantity",
                            "value": leik
                          }
                        },
                        {
                          "linkId": "3072e099-ba3d-47df-bbdb-3f81947f500d",
                          "answer": {
                            "code": "YM5iHafNePCmd83YbfJlfw==",
                            "system": "v5thww05S+xTtCEIapu4O9hK9xPDKatFgxo1PhYYNL0=",
                            "units": {
                              "code": "ITFgwPQzfXp7R25zIk25iw==",
                              "system": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=",
                              "display": "клет/мкл",
                              "id": "xV5o9jUSgpCJmTHAATDRXwr7KOECtE4BLtj1Ms8bSC4=ITFgwPQzfXp7R25zIk25iw=="
                            },
                            "type": "ValueQuantity",
                            "value": erit
                          }
                        }
                      ]
                    }
                  ]
                }
                s.get('https://helzy.ru/api/v1/analyses/carts')
                s.get('https://helzy.ru/api/v1/analyses/carts')
                s.get('https://helzy.ru/api/v1/analyses/catalog?pageNumber=1&pageSize=100')
                ids= s.cookies.get_dict()['HelzyAnalysesSessionId']
                debug = s.post('https://helzy.ru/api/v1/analyses/carts', json={"analysisId":"3418e3a0-df22-44d8-871b-cd4f8148f2b9"})
                debug1 = s.post('https://helzy.ru/api/v1/analyses/interpretations', json=jsonreq)
                report = s.get('https://helzy.ru/api/v1/analyses/interpretations/reports').json()
                if 'error' in report:
                    print('Данный анализ не поддерживается, доступно выделение отклонений')
                else:
                    print(report)
            else:
                print('Данный анализ не поддерживается, доступно выделение отклонений.')
        except:
            print('Данный анализ не поддерживается, доступно выделение отклонений.')