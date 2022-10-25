import requests
import json

ref = 'https://emias.info/api/emc/appointment-eip/v1/?getReferralsInfo'
ass = 'https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo'
spec = 'https://emias.info/api/emc/appointment-eip/v1/?getSpecialitiesInfo'
doclist = "https://emias.info/api/emc/appointment-eip/v1/?getAppointmentReceptionsByPatient"
speclist = 'https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo'
datespec = 'https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo'
create = "https://emias.info/api/emc/appointment-eip/v1/?createAppointment"
cancel = "https://emias.info/api/emc/appointment-eip/v1/?cancelAppointment"
shift = "https://emias.info/api/emc/appointment-eip/v1/?shiftAppointment"
info = 'https://emias.info/api/emc/appointment-eip/v1/?getPatientInfo3'

from selenium import webdriver
from requestium import Session, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

def mosloginemias(oms, password):
    firefox_options = Options()

    firefox_driver = webdriver.Firefox(executable_path="/home/user/Загрузки/Alter-main/AlTerGUI/geckodriver",
                                       options=firefox_options)
    s = Session(driver=firefox_driver)
    s.driver.get(
        "https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
    element = WebDriverWait(s.driver, 20).until(EC.element_to_be_clickable((By.ID, "login")))
    loginmos = s.driver.find_element(By.NAME, 'login')
    loginmos.send_keys(login)
    passwordmos = s.driver.find_element(By.NAME, 'password')
    passwordmos.send_keys(password)
    login_button = s.driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
    try:
        error = s.driver.find_element(By.XPATH,
                                      "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text
        print("Ошибка")
    except:
        verifcode = input("Код верификации\n")
        elements = WebDriverWait(s.driver, 20).until(EC.presence_of_element_located((By.ID, "otp_input")))
        usercode = s.driver.find_element(By.ID, 'otp_input')
        usercode.send_keys(verifcode)
        userid = WebDriverWait(s.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                   "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]")))
        name = s.driver.find_element(By.XPATH,
                                     "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]").text
        surename = s.driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[2]').text
        male = s.driver.find_element(By.ID, "profile_select_gender").text
        age = s.driver.find_element(By.ID, "profile_select_birth_date").text
        print("Пользователь: ", name, surename)
        print("Пол: ", male)
        print("Возраст", age)
        profdata = s.driver.execute_script("return window.sessionStorage.getItem('profile/profileData')")
        jsdata = json.loads(profdata)
        oms = jsdata['profile']['policyNum']
        bdate = jsdata['profile']['birthDate']
        assignment = requests.post(ass, json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                              "method": "getAssignmentsInfo",
                                              "params": {"omsNumber": oms, "birthDate": bdate}})
        jsass = assignment.json()
        specialities = requests.post(ass, json={"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                                                "method": "getSpecialitiesInfo",
                                                "params": {"omsNumber": oms, "birthDate": bdate}})
        jsspec = specialities.json()
        if "error" in jsass or "error" in jsspec:
            print(jsass["error"]["message"])
        else:
            emiaschoose = int(input("\nВыберите опцию:\n0 - Запись к врачу\n1 - Прикрепления\n"))
            if emiaschoose == 0:
                vrachchoose = int(input(
                    "\n0 - Запись к врачу\n1 - Просмотр записей\n2 - Просмотр направлений\n3 - Перенос записей\n4 - Отмена записей\n"))
                if vrachchoose == 0:
                    vrach(oms, bdate)
                elif vrachchoose == 1:
                    prosmotr(oms, bdate)
                elif vrachchoose == 2:
                    prosmotrnapr(oms, bdate)
                elif vrachchoose == 3:
                    perenos(oms, bdate)
                elif vrachchoose == 4:
                    otmena(oms, bdate)
            elif emiaschoose == 1:
                information(oms, bdate)

    s.driver.quit()

def moslogin(login, password):
    firefox_options = Options()

    firefox_driver = webdriver.Firefox(executable_path="/home/user/Загрузки/Alter-main/AlTerGUI/geckodriver", options = firefox_options)
    s = Session(driver=firefox_driver)
    s.driver.get("https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
    element = WebDriverWait(s.driver, 20).until(EC.element_to_be_clickable((By.ID, "login")))
    loginmos = s.driver.find_element(By.NAME, 'login')
    loginmos.send_keys(login)
    passwordmos = s.driver.find_element(By.NAME, 'password')
    passwordmos.send_keys(password)
    login_button = s.driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
    try:
        error = s.driver.find_element(By.XPATH,"/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text
        print("Ошибка")
    except:
        verifcode = input("Код верификации\n")
        elements = WebDriverWait(s.driver, 20).until(EC.presence_of_element_located((By.ID, "otp_input")))
        usercode = s.driver.find_element(By.ID, 'otp_input')
        usercode.send_keys(verifcode)
        userid = WebDriverWait(s.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                        "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]")))
        name = s.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]").text
        surename = s.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[2]').text
        male = s.driver.find_element(By.ID, "profile_select_gender").text
        age = s.driver.find_element(By.ID,"profile_select_birth_date").text
        print("Пользователь: ",name, surename)
        print("Пол: ",male)
        print("Возраст",age)
        idus = s.driver.execute_script("return window.sessionStorage.getItem('profile/currentProfileId')").replace('"', '')
        chooselist = int(input("(0) мои тесты на covid-19\n(1) мои прививки\n(2) мои приемы в поликлинике\n(3) мои анализы\n(4) мои исследования\n(5) мои больничные\n(6) мои справки и мед. заключения\n(7) мои выписки из стационара\n(8) мои рецепты\n(9) моя скорая помощь\n(10) мои врачебные консилиумы\n(11) мой дневник здоровья\n"))
    s.driver.quit()


def information(oms, bdate):
    inf = requests.post(info, json = {"jsonrpc":"2.0","id":"RUi98VgEkYYc8PPKR-OdE","method":"getPatientInfo3","params":{"omsNumber":oms,"birthDate":bdate,"typeAttach":[0,1,2], "onlyMoscowPolicy":False}})
    jsinf = inf.json()
    for i in range(len(jsinf['result']['attachments']['attachment'])):
        print(jsinf['result']['attachments']['attachment'][i]['lpu']['name'])
        print(jsinf['result']['attachments']['attachment'][i]['lpu']['address'])
        print(jsinf['result']['attachments']['attachment'][i]['status'])
        print(jsinf['result']['attachments']['attachment'][i]['createDate'])
def perenos(oms,bdate):
    compID = None
    c = 0
    spisokzapisei = requests.post(doclist, json = {"jsonrpc":"2.0","id":"H0XYtGjt9CtPQqfGt7NYp","method":"getAppointmentReceptionsByPatient","params":{"omsNumber":oms,"birthDate":bdate}})
    jsspisok = spisokzapisei.json()
    for i in range(len(jsspisok["result"])):
        if jsspisok["result"][i]['type'] == "RECEPTION":
            print(f"({i})",jsspisok["result"][i]['toDoctor']["specialityName"])
            print("Врач\n")
        else:
            print(f"({i})",jsspisok["result"][i]['toLdp']["ldpTypeName"])
            print("Процедура\n")
    zapisvibor = int(input("Выберите запись для переноса\n"))
    if jsspisok["result"][zapisvibor]['type'] == "RECEPTION":
        appID = jsspisok["result"][zapisvibor]['id']
        specID = jsspisok["result"][zapisvibor]["toDoctor"]['specialityId']
        recpID = jsspisok["result"][zapisvibor]["toDoctor"]['receptionTypeId']
        spisokvrachei = requests.post(speclist, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdate,"appointmentId":appID,"specialityId":specID}})
        jsvrachi = spisokvrachei.json()
        for i in range(len(jsvrachi["result"])):
            for j in range(len(jsvrachi["result"][i]['complexResource'])):
                    if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                        print(f"({i})",jsvrachi["result"][i]['name'])
                        c+=1
        if c == 0:
            print("Перенос не доступен")
        else:
            for i in range(len(jsvrachi["result"])):
                for j in range(len(jsvrachi["result"][i]['complexResource'])):
                        if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                            print(f"({i})",jsvrachi["result"][i]['name'])
            vrachchoose = int(input("Выберите врача\n"))
            resID = jsvrachi["result"][vrachchoose]["id"]
            for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                    complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
            dati = requests.post(datespec, json = {"jsonrpc":"2.0","id":"RUi98VgEkYYc8PPKR-OdE","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdate,"availableResourceId":resID,"complexResourceId":complID,"appointmentId":appID,"specialityId":specID}})
            jsdati = dati.json()
            for i in range(len(jsdati["result"]['scheduleOfDay'])):
                print(f"({i})", jsdati["result"]['scheduleOfDay'][i]['date'])
            datechoose = int(input("Выбор даты: \n"))
            for j in range(len(jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'])):
                print(f"({j})", jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['startTime'])
            vremya = int(input("Выбор времени:\n"))
            times = jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][vremya]['startTime']
            endTime = jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][vremya]['endTime']
            perenes = requests.post(shift, json = {"jsonrpc":"2.0","id":"RUi98VgEkYYc8PPKR-OdE","method":"shiftAppointment","params":{"omsNumber":oms,"birthDate":bdate,"appointmentId":appID,"specialityId":specID,"availableResourceId":resID,"complexResourceId":complID,"receptionTypeId":recpID,"startTime":times,"endTime":endTime}})
            jscheck = perenes.json()
            if "error" not in jscheck:
                print("Успешно")
            else:
                print("Произошла непредвиденная ошибка")
    else:
        appID = jsspisok["result"][zapisvibor]['id']
        recpID = jsspisok["result"][zapisvibor]["toLdp"]['ldpTypeId']
        spisokvrachei = requests.post(speclist, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdate,"appointmentId":appID}})
        jsvrachi = spisokvrachei.json()
        for i in range(len(jsvrachi["result"])):
            for j in range(len(jsvrachi["result"][i]['complexResource'])):
                if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                    print(f"({i})",jsvrachi["result"][i]['name'])
                    c+=1
        if c == 0:
            print("Перенос не доступен")
        else:
            for i in range(len(jsvrachi["result"])):
                for j in range(len(jsvrachi["result"][i]['complexResource'])):
                    if 'room' in jsvrachi["result"][i]['complexResource'][j]:
                        print(f"({i})",jsvrachi["result"][i]['name'])
            vrachchoose = int(input("Выберите врача\n"))
            resID = jsvrachi["result"][vrachchoose]["id"]
            for j in range(len(jsvrachi["result"][vrachchoose]['complexResource'])):
                if 'room' in jsvrachi["result"][vrachchoose]['complexResource'][j]:
                    complID = jsvrachi["result"][vrachchoose]['complexResource'][j]['id']
            dati = requests.post(datespec, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdate,"availableResourceId":resID,"complexResourceId":complID,"appointmentId":appID}})
            jsdati = dati.json()
            for i in range(len(jsdati["result"]['scheduleOfDay'])):
                print(f"({i})", jsdati["result"]['scheduleOfDay'][i]['date'])
            datechoose = int(input("Выбор даты: \n"))
            for j in range(len(jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'])):
                print(f"({j})", jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['startTime'])
            vremya = int(input("Выбор времени:\n"))
            times = jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][vremya]['startTime']
            endTime = jsdati["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][vremya]['endTime']
            perenes = requests.post(shift, json = {"jsonrpc":"2.0","id":"7LIqTOs9j1zSf-c7ohSzB","method":"shiftAppointment","params":{"omsNumber":oms,"birthDate":bdate,"appointmentId":appID,"availableResourceId":resID,"complexResourceId":complID,"receptionTypeId":recpID,"startTime":times,"endTime":endTime}})
            jscheck = perenes.json()
            if "error" not in jscheck:
                print("Успешно")
            else:
                print("Произошла непредвиденная ошибка")
def otmena(oms, bdate):
    prosmotr = requests.post(doclist, json = {"jsonrpc":"2.0","id":"tnSZKjovHE_X2b-JYQ0PB","method":"getAppointmentReceptionsByPatient","params":{"omsNumber":oms,"birthDate":bdate}})
    jsps = prosmotr.json()
    if len(jsps["result"]) == 0:
            print("Записей нет")
    else:
        for i in range(len(jsps["result"])):
            if jsps["result"][i]["type"] == "RECEPTION":
                print(f"({i})",jsps["result"][i]["toDoctor"]["specialityName"])
                print(jsps["result"][i]["startTime"])
                print(jsps["result"][i]["lpuAddress"])
                print(jsps["result"][i]["roomNumber"])
            else:
                print(f"({i})",jsps["result"][i]["toLdp"]["ldpTypeName"])
                print(jsps["result"][i]["startTime"])
                print(jsps["result"][i]["lpuAddress"])
                print(jsps["result"][i]["roomNumber"])
        otmenachoose = int(input("Выберите запись для отмены:\n"))
        appointmentId = jsps["result"][i]["id"]
        otmenas = requests.post(cancel, json = {"jsonrpc":"2.0","id":"lXe4h6pwr3IF-xCqBnESK","method":"cancelAppointment","params":{"omsNumber":oms,"birthDate":bdate,"appointmentId":appointmentId}})
        print("Отменено")


def prosmotrnapr(oms, bdate):
    prosmotrnaprs = requests.post(ref, json ={"jsonrpc":"2.0","id":"6Ov41JqE7a1bQ3i98ofeF","method":"getReferralsInfo","params":{"omsNumber":oms,"birthDate":bdate}})
    jsnp = prosmotrnaprs.json()
    if len(jsnp["result"]) == 0:
            print("Направлений нет")
    else:
        for i in range(len(jsnp["result"])):
            if jsnp["result"][i]["type"] == "REF_TO_DOCTOR":
                print(f"({i})",jsnp["result"][i]["toDoctor"]["specialityName"])
                print("Истекает: ",jsnp["result"][i]["startTime"])
                print(jsnp["result"][i]["toDoctor"]['specialityName'])
            else:
                print(f"({i})",jsnp["result"][i]["toLdp"]["ldpTypeName"])
                print("Истекает: ",jsnp["result"][i]["startTime"])
                print(jsnp["result"][i]["toLdp"]['ldpTypeName'])

     
def prosmotr(oms, bdate):
    prosmotr = requests.post(doclist, json = {"jsonrpc":"2.0","id":"tnSZKjovHE_X2b-JYQ0PB","method":"getAppointmentReceptionsByPatient","params":{"omsNumber":oms,"birthDate":bdate}})
    jsps = prosmotr.json()
    if len(jsps["result"]) == 0:
            print("Записей нет")
    else:
        for i in range(len(jsps["result"])):
            if jsps["result"][i]["type"] == "RECEPTION":
                print(f"({i})",jsps["result"][i]["toDoctor"]["specialityName"])
                print(jsps["result"][i]["startTime"])
                print(jsps["result"][i]["lpuAddress"])
                print(jsps["result"][i]["roomNumber"])
            else:
                print(f"({i})",jsps["result"][i]["toLdp"]["ldpTypeName"])
                print(jsps["result"][i]["startTime"])
                print(jsps["result"][i]["lpuAddress"])
                print(jsps["result"][i]["roomNumber"])




def vrach(oms, bdate):
    count = 0
    resid = 0
    c = 0

    specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdate}})
    jsspec = specialities.json()
    userid = jsass["id"]
    for i in range(len(jsspec["result"])):
        print(f"({i})", jsspec['result'][i]["name"])
    choose = int(input("Выберите запись\n"))
    specId = jsspec['result'][choose]["code"]
    zapis = requests.post(speclist, json = {"jsonrpc":"2.0","id":userid,"method":"getDoctorsInfo","params":{"omsNumber":oms,"birthDate":bdate,"specialityId": specId}})
    jszapis = zapis.json()
    for i in range(len(jszapis["result"])):
        for j in range(len(jszapis["result"][i]['complexResource'])):
            if 'room' in jszapis["result"][i]['complexResource'][j]:
                receptionTypeId = jszapis["result"][i]['receptionType'][0]['code']
                count+=1
    if count == 0:
        print("Записей нет")
    else:
        for i in range(len(jszapis["result"])):
            for j in range(len(jszapis["result"][i]['complexResource'])):
                if 'room' in jszapis["result"][i]['complexResource'][j]:
                    print(f"({c})",jszapis['result'][i]["name"])
                    c+=1
        uchoose = int(input("Выбор доктора\n"))
        docchoose = jszapis['result'][uchoose]["id"]
        for i in range(len(jszapis["result"])):
            if jszapis['result'][i]["id"] == docchoose:
                for j in range(len(jszapis["result"][i]['complexResource'])):
                    if 'room' in jszapis["result"][i]['complexResource'][j]:
                        resid = jszapis["result"][i]['complexResource'][j]['id']
        proczapis = requests.post(datespec, json = {"jsonrpc":"2.0","id":"7g9bgvEa8VkCd6A2XHJ7p","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":oms,"birthDate":bdate,"availableResourceId":docchoose,"complexResourceId":resid,"specialityId":"11"}})
        jsproczapis = proczapis.json()
        for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
            print("\n",f"({i})", jsproczapis["result"]['scheduleOfDay'][i]["date"])            
        datechoose = int(input("Выберите дату\n"))
        for j in range(len(jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'])):
            print(f"({j})",jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['startTime'])
        timechoose = int(input("Время\n"))
        times = jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][timechoose]['startTime']
        endtime = jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][timechoose]['endTime']
        appocreate = requests.post(create, json ={"jsonrpc":"2.0","id":"AvyJzHk1dm8eNqyg5uzLx","method":"createAppointment","params":{"omsNumber":oms,"birthDate":bdate,"availableResourceId":docchoose,"complexResourceId":resid,"receptionTypeId":receptionTypeId,"startTime":times,"endTime":endtime}})


chooselogin = int(input('(1) Войти по полису ОМС\n(2) Войти через mos.ru\n'))
if chooselogin == 1:
    oms = int(input("Полис:\n"))
    bdate = input("Дата рождения: year-month-day\n")

    assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":oms,"birthDate":bdate}})
    jsass = assignment.json()
    specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdate}})
    jsspec = specialities.json()
    if "error" in jsass or "error" in jsspec:
        print(jsass["error"]["message"])
    else:
        emiaschoose = int(input("\nВыберите опцию:\n0 - Запись к врачу\n1 - Прикрепления\n"))
        if emiaschoose == 0:
            vrachchoose = int(input("\n0 - Запись к врачу\n1 - Просмотр записей\n2 - Просмотр направлений\n3 - Перенос записей\n4 - Отмена записей\n"))
            if vrachchoose == 0:
                vrach(oms, bdate)
            elif vrachchoose == 1:
                prosmotr(oms, bdate)
            elif vrachchoose == 2:
                prosmotrnapr(oms, bdate)
            elif vrachchoose == 3:
                perenos(oms,bdate)
            elif vrachchoose == 4:
                otmena(oms, bdate)
        elif emiaschoose == 1:
            information(oms,bdate)
        elif emiaschoose == 2:
            None
        elif emiaschoose == 3:
            None
else:
    login = input("Login:\n")
    password = input("Password\n")
    mainchoose = int(input("(1) Войти в ЕМИАС\n(2)Войти в электронную карту\n"))
    if mainchoose == 1:
        mosloginemias(login, password)
    else:
        moslogin(login, password)

#5494499745000410
#1088989771000020