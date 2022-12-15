# html = '' 
# age = 19
# gender = 0
# date = '2022-12-01T00:00:00+03:00'
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
class analizis(Screen):
    def OKAK(html, age, gender, date):
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
                    wbc = jsanaliz[i]['Результат'].replace(",", '.')
                    break
                if 'RBC' in jsanaliz[i]['Тест'] or 'Эритроциты' in jsanaliz[i]['Тест'] or 'Количество эритроцитов' in jsanaliz[i]['Тест']:
                    rbc = jsanaliz[i]['Результат'].replace(",", '.')
                    break
                if 'HGB' in jsanaliz[i]['Тест'] or 'Гемоглобин' in jsanaliz[i]['Тест']:
                    hgb = jsanaliz[i]['Результат'].replace(",", '.')
                    break
                if 'HCT' in jsanaliz[i]['Тест'] or 'Гематокрит' in jsanaliz[i]['Тест']:
                    try:
                        if float(jsanaliz[i]['Результат'])<1:
                            hct = float(jsanaliz[i]['Результат'])*100
                        else:
                            hct = jsanaliz[i]['Результат'].replace(",", '.')
                    except:
                        if float(jsanaliz[i]['Результат'].replace(",", '.'))<1:
                            hct = float(jsanaliz[i]['Результат'].replace(",", '.'))*100
                        else:
                            hct = jsanaliz[i]['Результат']
                    break
                if 'MCV' in jsanaliz[i]['Тест'] or 'Средний объем эритроцита' in jsanaliz[i]['Тест']:
                    mcv = jsanaliz[i]['Результат'].replace(",", '.')
                    break
                if 'MCH' in jsanaliz[i]['Тест'] and 'MCHC' not in jsanaliz[i]['Тест'] or 'Среднее содержание гемоглобина в эритроците' in jsanaliz[i]['Тест']:
                    mch = jsanaliz[i]['Результат'].replace(",", '.')
                    break
                if 'MCHC' in jsanaliz[i]['Тест'] or 'Средняя концентрация гемоглобина в эритроците' in jsanaliz[i]['Тест']:
                    mchc = jsanaliz[i]['Результат'].replace(",", '.')
                    break
                if 'PLT' in jsanaliz[i]['Тест'] or 'Количество тромбоцитов' in jsanaliz[i]['Тест'] or 'Тромбоциты' in jsanaliz[i]['Тест']:
                    plt= jsanaliz[i]['Результат'].replace(",", '.')
                    break
        if wbc != None and  rbc != None and hgb != None and hct !=None and mcv !=None and mch !=None and mchc !=None and plt !=None:
            s = requests.Session()
            s.get('https://helzy.ru/api/v1/analyses/carts')
            json = {
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
            s.post('https://helzy.ru/api/v1/analyses/carts', json={"analysisId":"c33662be-1ac9-431e-a2a2-f5ce7c1cc992"}).json()
            s.post('https://helzy.ru/api/v1/analyses/interpretations', json=json)
            print(s.get('https://helzy.ru/api/v1/analyses/interpretations/reports').json())
        else:
            print('Данный анализ не поддерживается, доступно выделение отклонений.')
    def OAM(html, age, gender, date):
        None