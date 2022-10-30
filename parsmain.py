from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from types import SimpleNamespace
import requests
import json
import time


class AlterNamespace(SimpleNamespace):
    def __getitem__(self, name):
        if name in self.__dir__():
            return self.__getattribute__(name)
        else:
            return None

    def __contains__(self, name):
        return name in self.__dir__()


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

EMIAS_LK_API = f"https://lk.emias.mos.ru/"
MOS_RU_AUTH = "https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth"


def get_json(oms, bdate, method, **params):
    json = {"jsonrpc": "2.0", "id": "ULHOof43sz6OfDTK4KRf1",
            "method": method,
            "params": {"omsNumber": oms, "birthDate": bdate}}
    for param in params:
        json["params"][param] = params[param]
    return json


def question():
    emiaschoose = int(
        input("\nВыберите опцию:\n0 - Запись к врачу\n1 - Прикрепления\n"))
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
    elif emiaschoose == 2:
        None
    elif emiaschoose == 3:
        None


def mosloginemias(oms, password):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(
        executable_path=".\\AlterGUI\\geckodriver.exe", options=firefox_options)
    driver.get(
        MOS_RU_AUTH)
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
        driver.quit()
        jsdata = json.loads(
            profdata, object_hook=lambda d: AlterNamespace(**d))
        oms = jsdata.profile.policyNum
        bdate = jsdata.profile.birthDate
        assignment = requests.post(ass, json=get_json(
            oms, bdate, "getAssignmentsInfo"))
        jsass = assignment.json(object_hook=lambda d: AlterNamespace(**d))
        specialities = requests.post(
            ass, json=get_json(oms, bdate, "getSpecialitiesInfo"))
        jsspec = specialities.json(object_hook=lambda d: AlterNamespace(**d))
        if "error" in jsass or "error" in jsspec:
            print(jsass.error.message)
        else:
            question()


def moslogin(login, password):
    def covidtest(*args):
        covid = s.get(
            EMIAS_LK_API + f"api/1/documents/covid-analyzes?ehrId={idus}&shortDateFilter=all_time", headers={'X-Access-JWT': authtoken})
        jscov = covid.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jscov.documents)):
            print(f'({i})', jscov.documents[i].title)
            print(jscov.documents[i].date)
        prosmotr = int(input("Для просмотра результатов выберите тест:\n"))
        documentID = jscov.documents[prosmotr].documentId
        covidprosmotr = requests.get(
            EMIAS_LK_API + f'api/2/document?ehrId={idus}&documentId={documentID}', headers={'X-Access-JWT': authtoken})
        jscovpros = covidprosmotr.json(
            object_hook=lambda d: AlterNamespace(**d))
        print(jscovpros.title)
        print(jscovpros.documentHtml)
        print(jscovpros.date)

    def myvacine(*args):
        vacin = s.get(
            EMIAS_LK_API + f"api/3/vaccinations?ehrId={idus}", headers={'X-Access-JWT': authtoken})
        jsvac = vacin.json(object_hook=lambda d: AlterNamespace(**d))
        vacinchoose = int(
            input('(0) Профилактические прививки\n(1) Иммунодиагностические тесты\n'))
        if vacinchoose == 0:
            for i in range(len(jsvac.doneList)):
                print(
                    f"({i})", jsvac.doneList[i].infectionList[0].infectionName)
                print(jsvac.doneList[i].dateVaccination)
                print('Возраст: ', jsvac.doneList[i].age)

        else:
            for i in range(len(jsvac.tubList)):
                print(
                    f"({i})", jsvac.tubList[i].infectionList[0].infectionName)
                print(jsvac.tubList[i].dateVaccination)
                print(jsvac.tubList[i].tubResultList[0].reactionKind)
                print('Возраст: ', jsvac.tubList[i].age)

    def myanamnes(*args):
        anamnes = s.get(
            EMIAS_LK_API + f'api/1/documents/inspections?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jsanam = anamnes.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsanam.documents)):
            flag = False
            try:
                print(f'({i})', jsanam.documents[i].doctorSpecialization)
            except:
                print(f'({i})', jsanam.documents[i].title)
                flag = True
            if flag == False:
                print(jsanam.documents[i].title)
            if 'doctorName' in jsanam.documents[i]:
                print(jsanam.documents[i].doctorName)
            if 'appointmentDate' in jsanam.documents[i]:
                print(jsanam.documents[i].appointmentDate)
            if 'organisation' in jsanam.documents[i]:
                print(jsanam.documents[i].organisation)
        anamchoose = int(input("Выберите прием для просмотра\n"))
        docID = jsanam.documents[anamchoose].documentId
        prosmotr = s.get(
            EMIAS_LK_API + f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def myanaliz(*args):
        analiz = s.get(
            EMIAS_LK_API + f'api/1/documents/analyzes?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jsanaliz = analiz.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsanaliz.documents)):
            print(f'({i})', jsanaliz.documents[i].title)
            print(jsanaliz.documents[i].date)
        prosmotrchoose = int(input('Выберите анализ для просмотра\n'))
        docID = jsanaliz.documents[prosmotrchoose].documentId
        prosmotr = s.get(
            f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def myldp():
        ldp = s.get(
            EMIAS_LK_API + f'api/1/documents/research?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jsldp = ldp.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsldp.documents)):
            print(f'({i})', jsldp.documents[i].title)
            print(jsldp.documents[i].date)
            print(jsldp.documents[i].muName)
        prosmotrchoose = int(input('Выберите анализ для просмотра\n'))
        docID = jsldp.documents[prosmotrchoose].documentId
        prosmotr = s.get(
            EMIAS_LK_API + f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def myboln():
        print("Не доступно")

    def myspravki():
        spravki = s.get(
            EMIAS_LK_API + f'api/1/documents/medical-certificates?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jssp = spravki.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jssp.certificates095)):
            print(f"({i})Справка № 095/у")
            sertificate = jssp.certificates095[i]
            print(sertificate.educationalName)
            print(sertificate.muName)
            print(sertificate.medicalEmployeeSpeciality)
            print(sertificate.medicalEmployeeName)
            print(sertificate.dateCreated)
        prosmotrchoose = int(input("Выберите справку для просмотра\n"))
        docID = jssp.documents[prosmotrchoose].documentId
        prosmotr = s.get(
            EMIAS_LK_API + f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def mystacionar():
        stacionar = s.get(
            EMIAS_LK_API + f'api/1/documents/epicrisis?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jsstac = stacionar.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsstac.documents)):
            print(f'({i})', jsstac.documents[i].organisation)
            print(jsstac.documents[i].dischargeDate)
        prosmotrchoose = int(input('Выберите выписку для просмотра\n'))
        docID = jsstac.documents[prosmotrchoose].documentId
        prosmotr = s.get(
            f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def myrecepies():
        recepies = s.get(
            EMIAS_LK_API + f'api/2/receipt?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jsrec = recepies.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsrec.receipts)):
            receipt = jsrec.receipts[i]
            print(f'({i})', receipt.medicineName)
            print('Выписан', receipt.prescriptionDate)
            print('Просрочен', receipt.expirationDate)
            if receipt.prescriptionStatus == 'expired':
                print("Просрочен")
            else:
                print('Действует')
        prosmotrchoose = int(input('Выберите рецепт для просмотра\n'))
        docID = jsrec.receipts[prosmotrchoose].prescriptionNumber
        prosmotr = s.get(
            f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def myemergency():
        emergency = s.get(
            EMIAS_LK_API + f'api/1/documents/ambulance?ehrId={idus}&shortDateFilter=all_time', headers={'X-Access-JWT': authtoken})
        jsemg = emergency.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsemg.documents)):
            print(f'({i})', jsemg.documents[i].diagnosis)
            print(jsemg.documents[i].callDate)
        prosmotrchoose = int(input('Выберите рецепт для просмотра\n'))
        docID = jsemg.documents[prosmotrchoose].documentId
        prosmotr = s.get(
            EMIAS_LK_API + f'api/2/document?ehrId={idus}&documentId={docID}', headers={'X-Access-JWT': authtoken})
        jspros = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
        print(jspros.documentHtml)

    def doccons():
        print("Не доступно")

    def mydiary():
        print('Не доступно')

        None
    firefox_options = Options()
    firefox_options.add_argument("--headless")
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
        driver.quit()
    except:
        c = 0
        flag = False
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "otp_input")))
        usercode = driver.find_element(By.ID, 'otp_input')
        while driver.current_url == EMIAS_LK_API:
            while c <= 3:
                verifcode = input("Код верификации\n")
                usercode.send_keys(verifcode)
                time.sleep(5)
                if driver.current_url != EMIAS_LK_API:
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
        driver.quit()
        choseOptions = {
            0: covidtest,
            1: myvacine,
            2: myanamnes,
            3: myanaliz,
            4: myldp,
            5: myboln,
            6: myspravki,
            7: mystacionar,
            8: myrecepies,
            9: myemergency,
            10: doccons,
            11: mydiary}
        chooselist = int(input("(0) мои тесты на covid-19\n(1) мои прививки\n(2) мои приемы в поликлинике\n(3) мои анализы\n(4) мои исследования\n(5) мои больничные\n(6) мои справки и мед. заключения\n(7) мои выписки из стационара\n(8) мои рецепты\n(9) моя скорая помощь\n(10) мои врачебные консилиумы\n(11) мой дневник здоровья\n"))
        if (chooselist in choseOptions):
            choseOptions[chooselist](oms, bdate)
        else:
            print("Введено неверное значение!")


def information(oms, bdate):
    inf = requests.post(info, json=get_json(
        oms, bdate, "getPatientInfo3", typeAttach=[0, 1, 2], onlyMoscowPolicy=False))
    jsinf = inf.json(object_hook=lambda d: AlterNamespace(**d))
    for i in range(len(jsinf.result.attachments.attachment)):
        attachment = jsinf.result.attachments.attachment[i]
        print(attachment.lpu.name)
        print(attachment.lpu.address)
        print(attachment.status)
        print(attachment.createDate)


def perenos(oms, bdate):
    compID = None
    c = 0
    spisokzapisei = requests.post(doclist, json=get_json(
        oms, bdate, "getAppointmentReceptionsByPatient"))
    jsspisok = spisokzapisei.json(object_hook=lambda d: AlterNamespace(**d))
    for i in range(len(jsspisok.result)):
        if jsspisok.result[i].type == "RECEPTION":
            print(f"({i})", jsspisok.result[i].toDoctor.specialityName)
            print("Врач\n")
        else:
            print(f"({i})", jsspisok.result[i].toLdp.ldpTypeName)
            print("Процедура\n")
    zapisvibor = int(input("Выберите запись для переноса\n"))
    zapis = jsspisok.result[zapisvibor]
    if zapis.type == "RECEPTION":
        appID = zapis.id
        specID = zapis.toDoctor.specialityId
        recpID = zapis.toDoctor.receptionTypeId
        spisokvrachei = requests.post(speclist, json=get_json(
            oms, bdate, "getDoctorsInfo", appointmentId=appID, specialityId=specID))
        jsvrachi = spisokvrachei.json(
            object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsvrachi.result)):
            result = jsvrachi.result[i]
            for j in range(len(result.complexResource)):
                if 'room' in result.complexResource[j]:
                    print(f"({i})", result.name)
                    c += 1
        if c == 0:
            print("Перенос не доступен")
        else:
            for i in range(len(jsvrachi.result)):
                result = jsvrachi.result[i]
                for j in range(len(result.complexResource)):
                    if 'room' in result.complexResource[j]:
                        print(f"({i})", result.name)
            vrachchoose = int(input("Выберите врача\n"))
            resID = jsvrachi.result[vrachchoose].id
            for j in range(len(jsvrachi.result[vrachchoose].complexResource)):
                if 'room' in jsvrachi.result[vrachchoose].complexResource[j]:
                    complID = jsvrachi.result[vrachchoose].complexResource[j].id
            dati = requests.post(datespec, json=get_json(oms, bdate, "getAvailableResourceScheduleInfo",
                                 availableResourceId=resID, complexResourceId=complID, appointmentId=appID, specialityId=specID))
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
            perenes = requests.post(shift, json=get_json(oms, bdate, "shiftAppointment", appointmentId=appID, specialityId=specID,
                                    availableResourceId=resID, complexResourceId=complID, receptionTypeId=recpID, startTime=times, endTime=endTime))
            jscheck = perenes.json(object_hook=lambda d: AlterNamespace(**d))
            if "error" not in jscheck:
                print("Успешно")
            else:
                print("Произошла непредвиденная ошибка")
    else:
        appID = zapis.id
        recpID = zapis.toLdp.ldpTypeId
        spisokvrachei = requests.post(speclist, json=get_json(
            oms, bdate, "getDoctorsInfo", appointmentId=appID))
        jsvrachi = spisokvrachei.json(
            object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsvrachi.result)):
            for j in range(len(result.complexResource)):
                if 'room' in result.complexResource[j]:
                    print(f"({i})", result.name)
                    c += 1
        if c == 0:
            print("Перенос не доступен")
        else:
            for i in range(len(jsvrachi.result)):
                result = jsvrachi.result[i]
                for j in range(len(result.complexResource)):
                    if 'room' in result.complexResource[j]:
                        print(f"({i})", result.name)
            vrachchoose = int(input("Выберите врача\n"))
            vrach = jsvrachi.result[vrachchoose]
            resID = vrach.id
            for j in range(len(vrach.complexResource)):
                if 'room' in vrach.complexResource[j]:
                    complID = vrach.complexResource[j].id
            dati = requests.post(datespec, json=get_json(oms, bdate, "getAvailableResourceScheduleInfo",
                                 availableResourceId=resID, complexResourceId=complID, appointmentId=appID))
            jsdati = dati.json(object_hook=lambda d: AlterNamespace(**d))
            for i in range(len(jsdati.result.scheduleOfDay)):
                print(f"({i})", jsdati.result.scheduleOfDay[i].date)
            datechoose = int(input("Выбор даты: \n"))
            for j in range(len(jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot)):
                print(
                    f"({j})", jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[j].startTime)
            vremya = int(input("Выбор времени:\n"))
            timeInfo = jsdati.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[vremya]
            times = timeInfo.startTime
            endTime = timeInfo.endTime
            perenes = requests.post(shift, json=get_json(oms, bdate, "shiftAppointment", appointmentId=appID,
                                                         availableResourceId=resID, complexResourceId=complID, receptionTypeId=recpID, startTime=times, endTime=endTime))
            jscheck = perenes.json(object_hook=lambda d: AlterNamespace(**d))
            if "error" not in jscheck:
                print("Успешно")
            else:
                print("Произошла непредвиденная ошибка")


def otmena(oms, bdate):
    prosmotr = requests.post(doclist, json=get_json(
        oms, bdate, "getAppointmentReceptionsByPatient"))
    jsps = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
    if len(jsps.result) == 0:
        print("Записей нет")
    else:
        for i in range(len(jsps.result)):
            result = jsps.result[i]
            if result.type == "RECEPTION":
                print(f"({i})", result.toDoctor.specialityName)
                print(result.startTime)
                print(result.lpuAddress)
                print(result.roomNumber)
            else:
                print(f"({i})", result.toLdp.ldpTypeName)
                print(result.startTime)
                print(result.lpuAddress)
                print(result.roomNumber)
        otmenachoose = int(input("Выберите запись для отмены:\n"))
        appointmentId = jsps.result[otmenachoose].id
        otmenas = requests.post(cancel, json=get_json(
            oms, bdate, "cancelAppointment", appointmentId=appointmentId))
        print("Отменено")


def prosmotrnapr(oms, bdate):
    prosmotrnaprs = requests.post(
        ref, json=get_json(oms, bdate, "getReferralsInfo"))
    jsnp = prosmotrnaprs.json(object_hook=lambda d: AlterNamespace(**d))
    if len(jsnp.result) == 0:
        print("Направлений нет")
    else:
        for i in range(len(jsnp.result)):
            result = jsnp.result[i]
            if result.type == "REF_TO_DOCTOR":
                print(f"({i})", result.toDoctor.specialityName)
                print("Истекает: ", result.startTime)
                print(result.toDoctor.specialityName)
            else:
                print(f"({i})", result.toLdp.ldpTypeName)
                print("Истекает: ", result.startTime)
                print(result.toLdp.ldpTypeName)


def prosmotr(oms, bdate):
    prosmotr = requests.post(doclist, json=get_json(
        oms, bdate, "getAppointmentReceptionsByPatient"))
    jsps = prosmotr.json(object_hook=lambda d: AlterNamespace(**d))
    if len(jsps.result) == 0:
        print("Записей нет")
    else:
        for i in range(len(jsps.result)):
            result = jsps.result[i]
            if result.type == "RECEPTION":
                print(f"({i})", result.toDoctor.specialityName)
                print(result.startTime)
                print(result.lpuAddress)
                print(result.roomNumber)
            else:
                print(f"({i})", result.toLdp.ldpTypeName)
                print(result.startTime)
                print(result.lpuAddress)
                print(result.roomNumber)


def vrach(oms, bdate):
    count = 0
    resid = 0
    c = 0

    specialities = requests.post(
        ass, json=get_json(oms, bdate, "getSpecialitiesInfo"))
    jsspec = specialities.json(object_hook=lambda d: AlterNamespace(**d))
    userid = jsass.id
    for i in range(len(jsspec.result)):
        print(f"({i})", jsspec.result[i].name)
    choose = int(input("Выберите запись\n"))
    specId = jsspec.result[choose].code
    zapis = requests.post(speclist, json=get_json(
        oms, bdate, "getDoctorsInfo", specialityId=specId))
    jszapis = zapis.json(object_hook=lambda d: AlterNamespace(**d))
    for i in range(len(jszapis.result)):
        result = jszapis.result[i]
        for j in range(len(result.complexResource)):
            if 'room' in result.complexResource[j]:
                receptionTypeId = result.receptionType[0].code
                count += 1
    if count == 0:
        print("Записей нет")
    else:
        for i in range(len(jszapis.result)):
            result = jszapis.result[i]
            for j in range(len(result.complexResource)):
                if 'room' in result.complexResource[j]:
                    print(f"({c})", result.name)
                    c += 1
        uchoose = int(input("Выбор доктора\n"))
        docchoose = jszapis.result[uchoose].id
        for i in range(len(jszapis.result)):
            if result.id == docchoose:
                for j in range(len(result.complexResource)):
                    if 'room' in result.complexResource[j]:
                        resid = result.complexResource[j].id
        proczapis = requests.post(datespec, json=get_json(oms, bdate, "getAvailableResourceScheduleInfo",
                                  availableResourceId=docchoose, complexResourceId=resid, specialityId="11"))
        jsproczapis = proczapis.json(object_hook=lambda d: AlterNamespace(**d))
        for i in range(len(jsproczapis.result.scheduleOfDay)):
            print("\n", f"({i})", jsproczapis.result.scheduleOfDay[i].date)
        datechoose = int(input("Выберите дату\n"))
        for j in range(len(jsproczapis.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot)):
            print(
                f"({j})", jsproczapis.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[j].startTime)
        timechoose = int(input("Время\n"))
        timeInfo = jsproczapis.result.scheduleOfDay[datechoose].scheduleBySlot[0].slot[timechoose]
        times = timeInfo.startTime
        endtime = timeInfo.endTime
        appocreate = requests.post(create, json=get_json(oms, bdate, "createAppointment", availableResourceId=docchoose,
                                   complexResourceId=resid, receptionTypeId=receptionTypeId, startTime=times, endTime=endtime))


chooselogin = int(input('(1) Войти по полису ОМС\n(2) Войти через mos.ru\n'))
if chooselogin == 1:
    oms = int(input("Полис:\n"))
    bdate = input("Дата рождения: year-month-day\n")

    assignment = requests.post(ass, json=get_json(
        oms, bdate, "getAssignmentsInfo"))
    jsass = assignment.json(object_hook=lambda d: AlterNamespace(**d))
    specialities = requests.post(
        ass, json=get_json(oms, bdate, "getSpecialitiesInfo"))
    jsspec = specialities.json(object_hook=lambda d: AlterNamespace(**d))
    if "error" in jsass or "error" in jsspec:
        print(jsass.error.message)
    else:
        question()
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
