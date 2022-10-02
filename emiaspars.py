from calendar import day_abbr
from locale import currency
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

police = input("Полис: ")
day = input("День: ")
month = input("Месяц: ")
year = input("Год: ")

# options
options = webdriver.ChromeOptions()
# user-agent
#options.add_argument("headless")

driver = webdriver.Chrome(
    executable_path="chromedriver.exe",
    options=options
)



try:
    driver.get("https://emias.info/")
    

    police_input = driver.find_element(By.NAME, 'policy')
    police_input.send_keys(police)

    day_input = driver.find_element(By.NAME, 'day')
    day_input.send_keys(day)
    
    month_input = driver.find_element(By.NAME, 'month')
    month_input.send_keys(month)
    
    year_input = driver.find_element(By.NAME, 'year')
    year_input.send_keys(year)

    login_button = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div/div/div/form/button").click()
    time.sleep(5)
    if driver.current_url == "https://emias.info/appointment/create":
        print("Успешно")
        print("Вход выполнен с использованеим полиса: ",police[0:4], "**** ****", police[12:16])
        choose = int(input("Просмотреть мед. карту? 1 - Да, 2 - Нет\n"))
        if choose == 1:
            driver.get("https://lk.emias.mos.ru/")
            login = input("Телефон, электронная почта или СНИЛС: \n")
            password = input("Пароль: \n")


            log_input = driver.find_element(By.ID, 'login')
            log_input.send_keys(login)

            pass_input = driver.find_element(By.ID, 'password')
            pass_input.send_keys(password)

            login_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()

            verifcode = input("Для входа введите код с телефона\n")

            usercode = driver.find_element(By.ID, 'otp_input')
            usercode.send_keys(verifcode)

            time.sleep(10)


            
        elif choose == 2:
            driver.close()
            driver.quit()
            
        else:
            print("Были введены не верные данные")
    else:
        print("Произошла какая-то ошибка проверьте ввод")

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()


# 5494499745000410