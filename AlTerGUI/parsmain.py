import requests
import json

ref = 'https://emias.info/api/emc/appointment-eip/v1/?getReferralsInfo'
ass = 'https://emias.info/api/emc/appointment-eip/v1/?getAssignmentsInfo'
spec = 'https://emias.info/api/emc/appointment-eip/v1/?getSpecialitiesInfo'
speclist = 'https://emias.info/api/emc/appointment-eip/v1/?getDoctorsInfo'
datespec = 'https://emias.info/api/emc/appointment-eip/v1/?getAvailableResourceScheduleInfo'
create = "https://emias.info/api/emc/appointment-eip/v1/?createAppointment"

count = 0
resid = 0
c = 0

assignment = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getAssignmentsInfo","params":{"omsNumber":"5494499745000410","birthDate":"2005-05-04"}})
jsass = assignment.json()
specialities = requests.post(ass, json = {"jsonrpc":"2.0","id":"ULHOof43sz6OfDTK4KRf1","method":"getSpecialitiesInfo","params":{"omsNumber":"5494499745000410","birthDate":"2005-05-04"}})
jsspec = specialities.json()


if "error" in jsass or "error" in jsspec:
    print("error")
else:
    userid = jsass["id"]
    for i in range(len(jsspec["result"])):
        print(f"({i})", jsspec['result'][i]["name"])
    choose = int(input("Выберите запись\n"))
    specId = jsspec['result'][choose]["code"]
    zapis = requests.post(speclist, json = {"jsonrpc":"2.0","id":userid,"method":"getDoctorsInfo","params":{"omsNumber":"5494499745000410","birthDate":"2005-05-04","specialityId": specId}})
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
        proczapis = requests.post(datespec, json = {"jsonrpc":"2.0","id":"7g9bgvEa8VkCd6A2XHJ7p","method":"getAvailableResourceScheduleInfo","params":{"omsNumber":"5494499745000410","birthDate":"2005-05-04","availableResourceId":docchoose,"complexResourceId":resid,"specialityId":"11"}})
        jsproczapis = proczapis.json()
        for i in range(len(jsproczapis["result"]['scheduleOfDay'])):
            print("\n",f"({i})", jsproczapis["result"]['scheduleOfDay'][i]["date"])            
        datechoose = int(input("Выберите дату\n"))
        for j in range(len(jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'])):
            times = jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['startTime']
            endtime = jsproczapis["result"]['scheduleOfDay'][datechoose]['scheduleBySlot'][0]['slot'][j]['endTime']
            print(f"({j})",times)
        timechoose = int(input("Время\n"))
        appocreate = requests.post(create, json ={"jsonrpc":"2.0","id":"AvyJzHk1dm8eNqyg5uzLx","method":"createAppointment","params":{"omsNumber":"5494499745000410","birthDate":"2005-05-04","availableResourceId":docchoose,"complexResourceId":resid,"receptionTypeId":receptionTypeId,"specialityId":choose,"startTime":times,"endTime":endtime}})
        




    
    


