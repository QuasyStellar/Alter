from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import json
import time
from types import SimpleNamespace


class AlterNamespace(SimpleNamespace):
    def __getitem__(self, name):
        return self.__getattribute__(name)

    def __contains__(self, name):
        return name in self.__dir__()


EMIAS_API = "https://emias.info/api/emc/appointment-eip/v1/"
EMIAS_REFERRALS_INFO = EMIAS_API + '?getReferralsInfo'
EMIAS_ASSIGNMENTS_INFO = EMIAS_API + "getAssignmentsInfo"
EMIAS_SPECIALISTIES_INFO = EMIAS_API + "getSpecialitiesInfo"
EMIAS_RECEPTIONS_BY_PATIENT = EMIAS_API + "getAppointmentReceptionsByPatient"
EMIAS_DOCTORS_INFO = EMIAS_API + "getDoctorsInfo"
EMIAS_SHEDULE_INFO = EMIAS_API + "getAvailableResourceScheduleInfo"
EMIAS_CREATE_APPOINTMENT = EMIAS_API + "createAppointment"
EMIAS_CANCEL_APPOINTMENT = EMIAS_API + "cancelAppointment"
EMIAS_SHIFT_APPOINTMENT = EMIAS_API + "shiftAppointment"
EMIAS_PATIENT_INFO = EMIAS_API + "getPatientInfo3"
EMIAS_LK = "https://lk.emias.mos.ru/"
MOS_RU_AUTH = "https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth"

EMIAS_JSON_FILL = {"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
                   "method": "getAssignmentsInfo",
                   "params": {"omsNumber": None, "birthDate": None}}


def get_json(oms: str, birthDate: str, **params):
    temp = EMIAS_JSON_FILL.copy()
    temp.params.omsNumber = oms
    temp.params.birthDate = birthDate
    for paramName in params:
        temp.params[paramName] = params[paramName]
    return temp


def mosloginemias(oms, password):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(
        executable_path=".\\AlterGUI\\geckodriver.exe", options=firefox_options)
    driver.get(MOS_RU_AUTH)
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login")))
    loginmos = driver.find_element(By.NAME, 'login')
    loginmos.send_keys(login)
    passwordmos = driver.find_element(By.NAME, 'password')
    passwordmos.send_keys(password)
    login_button = driver.find_element(
        By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
    try:
        error = driver.find_element(By.XPATH,
                                    "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text
        print("Ошибка")
    except:
        verifcode = input("Код верификации\n")
        elements = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "otp_input")))
        usercode = driver.find_element(By.ID, 'otp_input')
        usercode.send_keys(verifcode)
        userid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                 "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]")))
        name = driver.find_element(By.XPATH,
                                   "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]").text
        surename = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[2]').text
        male = driver.find_element(By.ID, "profile_select_gender").text
        age = driver.find_element(By.ID, "profile_select_birth_date").text
        print("Пользователь: ", name, surename)
        print("Пол: ", male)
        print("Возраст", age)
        profdata = driver.execute_script(
            "return window.sessionStorage.getItem('profile/profileData')")

        jsdata = json.loads(
            profdata, object_hook=lambda d: AlterNamespace(**d))
        oms = jsdata.profile.policyNum
        bdate = jsdata.profile.birthDate
        assignment = requests.post(
            EMIAS_ASSIGNMENTS_INFO, json=get_json(oms, bdate))
        jsass = assignment.json(object_hook=lambda d: AlterNamespace(**d))
        specialities = requests.post(
            EMIAS_ASSIGNMENTS_INFO, json=get_json(oms, bdate))
        jsspec = specialities.json(object_hook=lambda d: AlterNamespace(**d))
        if "error" in jsass or "error" in jsspec:
            print(jsass.error.message)
        else:
            emiasQuestion()

    driver.quit()


def moslogin(login, password):
    def covidtest(*args):
        covid = s.get(
            EMIAS_LK + f"api/1/documents/covid-analyzes?ehrId={idus}&shortDateFilter=all_time", headers={'X-Access-JWT': authtoken})
        jscov = covid.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jscov.documents)):
            print(f'({i})', jscov.documents[i].title)
            print(jscov.documents[i].date)
        prosmotr = int(input("Для просмотра результатов выберите тест:\n"))
        documentID = jscov.documents[prosmotr].documentId
        covidprosmotr = requests.get(
            EMIAS_LK + f'api/2/document?ehrId={idus}&documentId={documentID}', headers={'X-Access-JWT': authtoken})
        jscovpros = covidprosmotr.json(
            object_hook=lambda d: AlterNamespace(**d))
        print(jscovpros.title)
        print(jscovpros.documentHtml)
        print(jscovpros.date)

    def myvacine(*args):
        vacin = s.get(
            EMIAS_LK + f"api/3/vaccinations?ehrId={idus}", headers={'X-Access-JWT': authtoken})
        jsvac = vacin.json(object_hook=lambda d: AlterNamespace(**d))
        vacinchoose = int(
            input('(0) Профилактические прививки\n(1) Иммунодиагностические тесты\n'))
        if vacinchoose == 0:
            print(jsvac.doneList)
            for i in range(len(jsvac.doneList)):
                print(
                    f"({i})", jsvac.doneList[i].infectionList[0].infectionName)
                print(jsvac.doneList[i].dateVaccination)
                print('Возраст: ', jsvac.doneList[i].age)
            viewchoose = int(
                input('Выберите тест или прививку для просмотра реузльтатов'))
        else:
            for i in range(len(jsvac.tubList)):
                print(
                    f"({i})", jsvac.tubList[i].infectionList[0].infectionName)
                print(jsvac.tubList[i].dateVaccination)
                print('Возраст: ', jsvac.tubList[i].age)
            viewchoose = int(
                input('Выберите тест или прививку для просмотра реузльтатов'))

        None
    firefox_options = Options()
    # firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(
        executable_path=".\\AlterGUI\\geckodriver.exe", options=firefox_options)
    driver.get(MOS_RU_AUTH)
    element = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.ID, "login")))
    loginmos = driver.find_element(By.NAME, 'login')
    loginmos.send_keys(login)
    passwordmos = driver.find_element(By.NAME, 'password')
    passwordmos.send_keys(password)
    login_button = driver.find_element(
        By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
    try:
        error = driver.find_element(
            By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text
        print("Ошибка")
    except:
        c = 0
        flag = False
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "otp_input")))
        usercode = driver.find_element(By.ID, 'otp_input')
        while driver.current_url == EMIAS_LK:
            while c != 3:
                verifcode = input("Код верификации\n")
                usercode.send_keys(verifcode)
                time.sleep(5)
                if driver.current_url != EMIAS_LK:
                    flag = True
                    break
                else:
                    print("Введен не верный код")
                    c += 1
            if flag == True:
                break
            else:
                print(
                    "Было введено слишком много неправильных кодов, доступ временно заблокирован")
                time.sleep(60)
                c = 0
        userid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                                 "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]")))
        name = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]").text
        surename = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[2]').text
        male = driver.find_element(By.ID, "profile_select_gender").text
        age = driver.find_element(By.ID, "profile_select_birth_date").text
        print("Пользователь: ", name, surename)
        print("Пол: ", male)
        print("Возраст", age)
        idus = driver.execute_script(
            "return window.sessionStorage.getItem('profile/currentProfileId')").replace('"', '')
        authtoken = driver.execute_script(
            "return window.localStorage.getItem('patient.web.v2.accessToken')").replace('"', '')
        s = requests.Session()
        for cookie in driver.get_cookies():
            c = {cookie.name:  cookie.value}
            s.cookies.update(c)
        choseoptions = {
            0: covidtest,
            1: myvacine
        }
        chooselist = int(input("(0) мои тесты на covid-19\n(1) мои прививки\n(2) мои приемы в поликлинике\n(3) мои анализы\n(4) мои исследования\n(5) мои больничные\n(6) мои справки и мед. заключения\n(7) мои выписки из стационара\n(8) мои рецепты\n(9) моя скорая помощь\n(10) мои врачебные консилиумы\n(11) мой дневник здоровья\n"))
        if (chooselist in choseoptions):
            choseoptions[chooselist]()
        else:
            print("Выбран несуществующий вариант!")
        # elif chooselist == 2:
        #     myanamnes()
        # elif chooselist == 3:
        #     myanaliz()
        # elif chooselist == 4:
        #     myldp()
        # elif chooselist == 5:
        #     myboln()
        # elif chooselist == 6:
        #     myspravki()
        # elif chooselist == 7:
        #     mystacionar()
        # elif chooselist == 8:
        #     myrecepies()
        # elif chooselist == 9:
        #     myemergency()
        # elif chooselist == 10:
        #     doccons()
        # elif chooselist == 11:
        #     mydiary()


def information(oms, bdate):
    inf = requests.post(EMIAS_PATIENT_INFO, json=get_json(
        typeAttach=[0, 1, 2], onlyMoscowPolicy=False))
    jsinf = inf.json(object_hook=lambda d: AlterNamespace(**d))
    for i in range(len(jsinf.result.attachments.attachment)):
        print(jsinf.result.attachments.attachment[i].lpu.name)
        print(jsinf.result.attachments.attachment[i].lpu.address)
        print(jsinf.result.attachments.attachment[i].status)
        print(jsinf.result.attachments.attachment[i].createDate)


def perenos(oms, bdate):
    compID = None
    c = 0
    spisokzapisei = requests.post(
        EMIAS_RECEPTIONS_BY_PATIENT, json=get_json(oms, bdate))
    jsspisok = spisokzapisei.json(object_hook=lambda d: AlterNamespace(**d))
    for i in range(len(jsspisok.result)):
        if jsspisok.result[i].type == "RECEPTION":
            print(f"({i})", jsspisok.result[i].toDoctor.specialityName)
            print("Врач\n")
        else:
            print(f"({i})", jsspisok.result[i].toLdp.ldpTypeName)
            print("Процедура\n")
    zapisvibor = int(input("Выберите запись для переноса\n"))
    if jsspisok.result[zapisvibor].type == "RECEPTION":
        appID = jsspisok.result[zapisvibor].id
        specID = jsspisok.result[zapisvibor].toDoctor.specialityId
        recpID = jsspisok.result[zapisvibor].toDoctor.receptionTypeId
        spisokvrachei = requests.post(EMIAS_DOCTORS_INFO, json=get_json(
            oms, bdate, appointmentId=appID, specialityId=specID))
        jsvrachi = spisokvrachei.json(
            object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsvrachi.result)):
            for j in range(len(jsvrachi.result[i].complexResource)):
                if 'room' in jsvrachi.result[i].complexResource[j]:
                    print(f"({i})", jsvrachi.result[i].name)
                    c += 1
        if c == 0:
            print("Перенос не доступен")
        else:
            for i in range(len(jsvrachi.result)):
                for j in range(len(jsvrachi.result[i].complexResource)):
                    if 'room' in jsvrachi.result[i].complexResource[j]:
                        print(f"({i})", jsvrachi.result[i].name)
            vrachchoose = int(input("Выберите врача\n"))
            resID = jsvrachi.result[vrachchoose].id
            for j in range(len(jsvrachi.result[vrachchoose].complexResource)):
                if 'room' in jsvrachi.result[vrachchoose].complexResource[j]:
                    complID = jsvrachi.result[vrachchoose].complexResource[j].id
            dati = requests.post(EMIAS_SHEDULE_INFO, json=get_json(
                oms, bdate, availableResourceId=resID, complexResourceId=complID, appointmentId=appID, specialityId=specID))
            jsdati = dati.json(object_hook=lambda d: AlterNamespace(**d))
            for i in range(len(jsdati.result.scheduleOfDay)):
                print(f"({i})", jsdati.result.scheduleOfDay[i].date)
            datechoose = int(input("Выбор даты: \n"))
            for j in range(len(jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot)):
                print(
                    f"({j})", jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[j].startTime)
            vremya = int(input("Выбор времени:\n"))
            times = jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[vremya].startTime
            endTime = jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[vremya].endTime
            perenes = requests.post(EMIAS_SHIFT_APPOINTMENT, json=get_json(oms, bdate, appointmentId=appID, specialityId=specID,
                                    availableResourceId=resID, complexResourceId=complID, receptionTypeId=recpID, startTime=times, endTime=endTime))
            jscheck = perenes.json(object_hook=lambda d: AlterNamespace(**d))
            if "error" not in jscheck:
                print("Успешно")
            else:
                print("Произошла непредвиденная ошибка")
    else:
        appID = jsspisok.result[zapisvibor].id
        recpID = jsspisok.result[zapisvibor].toLdp.ldpTypeId
        spisokvrachei = requests.post(
            EMIAS_DOCTORS_INFO, json=get_json(oms, bdate, appointmentId=appID))
        jsvrachi = spisokvrachei.json(
            object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsvrachi.result)):
            for j in range(len(jsvrachi.result[i].complexResource)):
                if 'room' in jsvrachi.result[i].complexResource[j]:
                    print(f"({i})", jsvrachi.result[i].name)
                    c += 1
        if c == 0:
            print("Перенос не доступен")
        else:
            for i in range(len(jsvrachi.result)):
                for j in range(len(jsvrachi.result[i].complexResource)):
                    if 'room' in jsvrachi.result[i].complexResource[j]:
                        print(f"({i})", jsvrachi.result[i].name)
            vrachchoose = int(input("Выберите врача\n"))
            resID = jsvrachi.result[vrachchoose].id
            for j in range(len(jsvrachi.result[vrachchoose].complexResource)):
                if 'room' in jsvrachi.result[vrachchoose].complexResource[j]:
                    complID = jsvrachi.result[vrachchoose].complexResource[j].id
            dati = requests.post(EMIAS_SHEDULE_INFO, json=get_json(
                oms, bdate, availableResourceId=resID, complexResourceId=complID, appointmentId=appID))
            jsdati = dati.json(object_hook=lambda d: AlterNamespace(**d))
            for i in range(len(jsdati.result.scheduleOfDay)):
                print(f"({i})", jsdati.result.scheduleOfDay[i].date)
            datechoose = int(input("Выбор даты: \n"))
            for j in range(len(jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot)):
                print(f"({j})", jsdati.result.scheduleOfDay[datechoose]
                      .scheduleBySlot[0].slot[j].startTime)
            vremya = int(input("Выбор времени:\n"))
            info_obj = jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[vremya]
            times = info_obj.startTime
            endTime = info_obj.endTime
            perenes = requests.post(EMIAS_SHIFT_APPOINTMENT, json=get_json(oms, bdate, appointmentId=appID,
                                    availableResourceId=resID, complexResourceId=complID, receptionTypeId=recpID, startTime=times, endTime=endTime))
            jscheck = perenes.json(object_hook=lambda d: AlterNamespace(**d))
            if "error" not in jscheck:
                print("Успешно")
            else:
                print("Произошла непредвиденная ошибка")


def otmena(oms, bdate):
    prosmotr = requests.post(
        EMIAS_RECEPTIONS_BY_PATIENT, json=get_json(oms, bdate))
    jsps = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
    if len(jsps.result) == 0:
        print("Записей нет")
    else:
        for i in range(len(jsps.result)):
            if jsps.result[i].type == "RECEPTION":
                print(f"({i})", jsps.result[i]
                      .toDoctor.specialityName)
                print(jsps.result[i].startTime)
                print(jsps.result[i].lpuAddress)
                print(jsps.result[i].roomNumber)
            else:
                print(f"({i})", jsps.result[i].toLdp.ldpTypeName)
                print(jsps.result[i].startTime)
                print(jsps.result[i].lpuAddress)
                print(jsps.result[i].roomNumber)
        otmenachoose = int(input("Выберите запись для отмены:\n"))
        appointmentId = jsps.result[i].id
        otmenas = requests.post(EMIAS_CANCEL_APPOINTMENT, json=get_json(
            oms, bdate, appointmentId=appointmentId))
        print("Отменено")


def prosmotrnapr(oms, bdate):
    prosmotrnaprs = requests.post(
        EMIAS_REFERRALS_INFO, json=get_json(oms, bdate))
    jsnp = prosmotrnaprs.json(object_hook=lambda d: AlterNamespace(**d))
    if len(jsnp.result) == 0:
        print("Направлений нет")
    else:
        for i in range(len(jsnp.result)):
            if jsnp.result[i].type == "REF_TO_DOCTOR":
                print(f"({i})", jsnp.result[i]
                      .toDoctor.specialityName)
                print("Истекает: ", jsnp.result[i].startTime)
                print(jsnp.result[i].toDoctor.specialityName)
            else:
                print(f"({i})", jsnp.result[i].toLdp.ldpTypeName)
                print("Истекает: ", jsnp.result[i].startTime)
                print(jsnp.result[i].toLdp.ldpTypeName)


def prosmotr(oms, bdate):
    prosmotr = requests.post(
        EMIAS_RECEPTIONS_BY_PATIENT, json=get_json(oms, bdate))
    jsps = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
    if len(jsps.result) == 0:
        print("Записей нет")
    else:
        for i in range(len(jsps.result)):
            if jsps.result[i].type == "RECEPTION":
                print(f"({i})", jsps.result[i]
                      .toDoctor.specialityName)
                print(jsps.result[i].startTime)
                print(jsps.result[i].lpuAddress)
                print(jsps.result[i].roomNumber)
            else:
                print(f"({i})", jsps.result[i].toLdp.ldpTypeName)
                print(jsps.result[i].startTime)
                print(jsps.result[i].lpuAddress)
                print(jsps.result[i].roomNumber)


def vrach(oms, bdate):
    count = 0
    resid = 0
    c = 0

    specialities = requests.post(
        EMIAS_ASSIGNMENTS_INFO, json=get_json(oms, bdate))
    jsspec = specialities.json(object_hook=lambda d: AlterNamespace(**d))
    userid = jsass.id
    for i in range(len(jsspec.result)):
        print(f"({i})", jsspec.result[i].name)
    choose = int(input("Выберите запись\n"))
    specId = jsspec.result[choose].code
    zapis = requests.post(EMIAS_DOCTORS_INFO, json=get_json(
        oms, bdate, specialityId=specId))
    jszapis = zapis.json(object_hook=lambda d: AlterNamespace(**d))
    for i in range(len(jszapis.result)):
        for j in range(len(jszapis.result[i].complexResource)):
            if 'room' in jszapis.result[i].complexResource[j]:
                receptionTypeId = jszapis.result[i].receptionType[0].code
                count += 1
    if count == 0:
        print("Записей нет")
    else:
        for i in range(len(jszapis.result)):
            for j in range(len(jszapis.result[i].complexResource)):
                if 'room' in jszapis.result[i].complexResource[j]:
                    print(f"({c})", jszapis.result[i].name)
                    c += 1
        uchoose = int(input("Выбор доктора\n"))
        docchoose = jszapis.result[uchoose].id
        for i in range(len(jszapis.result)):
            if jszapis.result[i].id == docchoose:
                for j in range(len(jszapis.result[i].complexResource)):
                    if 'room' in jszapis.result[i].complexResource[j]:
                        resid = jszapis.result[i].complexResource[j].id
        proczapis = requests.post(EMIAS_SHEDULE_INFO, json=get_json(
            oms, bdate, availableResourceId=docchoose, complexResourceId=resid, specialityId="11"))
        jsproczapis = proczapis.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsproczapis.result.scheduleOfDay)):
            print("\n", f"({i})",
                  jsproczapis.result.scheduleOfDay[i].date)
        datechoose = int(input("Выберите дату\n"))
        for j in range(len(jsproczapis.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot)):
            print(f"({j})", jsproczapis.result.scheduleOfDay
                  [datechoose].scheduleBySlot[0].slot[j].startTime)
        timechoose = int(input("Время\n"))
        times = jsproczapis.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[timechoose].startTime
        endtime = jsproczapis.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[timechoose].endTime
        appocreate = requests.post(EMIAS_CREATE_APPOINTMENT, json=get_json(oms, bdate, availableResourceId=docchoose,
                                   complexResourceId=resid, receptionTypeId=receptionTypeId, startTime=times, endTime=endtime))


def emiasQuestion():
    emiaschoose = int(
        input("\nВыберите опцию:\n0 - Запись к врачу\n1 - Прикрепления\n"))
    if emiaschoose == 0:
        vrashoptions = {
            0: vrach,
            1: prosmotr,
            2: prosmotrnapr,
            3: perenos,
            4: otmena
        }
        vrachchoose = int(input(
            "\n0 - Запись к врачу\n1 - Просмотр записей\n2 - Просмотр направлений\n3 - Перенос записей\n4 - Отмена записей\n"))
        if (vrachchoose in vrashoptions):
            vrashoptions[vrachchoose](oms, bdate)
        else:
            print("Введен несуществующий вариант!")
    elif emiaschoose == 1:
        information(oms, bdate)
    elif emiaschoose == 2:
        None
    elif emiaschoose == 3:
        None


chooselogin = int(input('(1) Войти по полису ОМС\n(2) Войти через mos.ru\n'))
if chooselogin == 1:
    oms = int(input("Полис:\n"))
    bdate = input("Дата рождения: year-month-day\n")

    assignment = requests.post(
        EMIAS_ASSIGNMENTS_INFO, json=get_json(oms, bdate))
    jsass = assignment.json(object_hook=lambda d: AlterNamespace(**d))
    specialities = requests.post(
        EMIAS_ASSIGNMENTS_INFO, json=get_json(oms, bdate))
    jsspec = specialities.json(object_hook=lambda d: AlterNamespace(**d))
    if "error" in jsass or "error" in jsspec:
        print(jsass.error.message)
    else:
        emiasQuestion()
else:
    login = input("Login:\n")
    password = input("Password\n")
    mainchoose = int(
        input("(1) Войти в ЕМИАС\n(2)Войти в электронную карту\n"))
    if mainchoose == 1:
        mosloginemias(login, password)
    else:
        moslogin(login, password)

# 5494499745000410
# 1088989771000020
