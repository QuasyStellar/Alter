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
    
    if "error" in jsass or "error" in jsspec:
        print("error")
    else:
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
                times = jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['startTime']
                endtime = jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['endTime']
                print(f"({j})",times)
            timechoose = int(input("Время\n"))
            appocreate = requests.post(create, json ={"jsonrpc":"2.0","id":"AvyJzHk1dm8eNqyg5uzLx","method":"createAppointment","params":{"omsNumber":oms,"birthDate":bdate,"availableResourceId":docchoose,"complexResourceId":resid,"receptionTypeId":receptionTypeId,"startTime":times,"endTime":endtime}})


oms = int(input("Полис:\n"))
bdate = input("Дата рождения: year-month-day\n")

assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":oms,"birthDate":bdate}})
jsass = assignment.json()
specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":oms,"birthDate":bdate}})
jsspec = specialities.json()


if "error" in jsass or "error" in jsspec:
    print(jsass["error"]["message"])
else:
    print(oms)
    emiaschoose = int(input("\nВыберите опцию:\n0 - Запись к врачу\n1 - Учреждения\n2 - Справки\n3 - Рецепты\n"))


    if emiaschoose == 0:
        vrachchoose = int(input("\n0 - Запись к врачу\n1 - Просмотр записей\n2 - Просмотр направлений\n3 - Перенос записей\n4 - Отмена записей\n"))
        if vrachchoose == 0:
            vrach(oms, bdate)
        elif vrachchoose == 1:
            prosmotr(oms, bdate)
        elif vrachchoose == 2:
            prosmotrnapr(oms, bdate)
        elif vrachchoose == 3:
            None
        elif vrachchoose == 4:
            otmena(oms, bdate)
    elif emiaschoose == 1:
        None
    elif emiaschoose == 2:
        None
    elif emiaschoose == 3:
        None

#5494499745000410
#1088989771000020