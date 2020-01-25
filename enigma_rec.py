# Импорт необходимых библиотек
import subprocess
import platform
import datetime
import os
import time
import webbrowser
import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
from pyspectator.processor import Cpu
import psutil
import wikipedia
import pyowm
import pyspeedtest
import tkinter as tk
from tkinter import messagebox as mb

#Список ссылок , которые понадобятся в процессе выполнения некоторых запросов от пользователя
url = "www.google.com"
url1 = "https://www.youtube.com/"
url2 = "https://yummyanime.club"
url3 = "https://www.youtube.com/results?search_query=lofi&pbjreload=10"
url4 = "https://www.bbc.com/"
url5 = "https://www.google.com/search?q=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0&oq=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0&aqs=chrome.0.69i59j0j35i39j0l3.1651j0j7&sourceid=chrome&ie=UTF-8"
url6 = "https://www.google.com/search?q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA&oq=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA&aqs=chrome..69i57j0l5.1126j0j7&sourceid=chrome&ie=UTF-8"
url7 = "https://www.google.com.ua/maps/"
url8 = "https://www.google.com/maps/place/"
url9 = "http://rozklad.nau.edu.ua/timetable/group/%D0%A4%D0%9A%D0%9A%D0%9F%D0%86%20141/1"
url10 = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B3%D1%80%D0%BD&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B3%D1%80%D0%BD&aqs=chrome..69i57j0l5.13186j1j7&sourceid=chrome&ie=UTF-8"
url11 = "https://kinokrad.co"
url12 = "https://www.google.com/maps/@50.4206522,30.4214908,13z/data=!5m1!1e1"
url13 = "https://www.povarenok.ru/"







# Настройки  с командами , на которые будет реагировать Enigma и которые доступны пользователю
# для одной команды возможны несколько вариаций , для удобства пользователя
opts = {
    
    "searchweather": ("погода","какая погода у","какая погода в","погода в"),
    "searchgoogle": ("поиск" , "найди что такое" , "гугл" , "загугли что такое",'google'),
    "wiki" : ("найди мне статтю у википедии" , "Сделай запрос у Википедии" , "Википедия" , "википедия"),
    "alias": ('enigma','энигма',"бэта","бэта-энигма","енигма"),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси','открой',"зайди" , "включи"),
    "cmds": {'ctime': ('текущее время', 'сейчас времени', 'который час'),
             'brows': ('открой браузер',  "открой гугл"),
             'anime': ("открой аниме", "включи аниме", "Включи ями аниме", "открой сайт аниме","Включи ямианиме"),
             'lofi': ("включи лоуфай","открой лоу фай","лоу фай музыку"),
             'calend' : ("какое число","покажи дату","открой календарь"),
             "list" : ("включи список дел","открой список дел","список","какие на сегодня дела"),
             'news': ("что нового в мире","покажи новости","включи новости","что творится в мире"),
             'weather' : ("погода",'открой погоду','какая сегодня погода','какая будет погода'),
             "trans" : ("открой переводчик","переводчик гугл","переведи слово"),
             "map" : ("открой карту","карту"),
             "loc":("где я","моё местоположение","покажи меня на карте"),
             "calc" : ("калькулятор","запусти калькулятор","включи калькулятор"),
             "cam" : ("камера"," сделай фото","сделай снимок","фото"),
             "telega":("телегам","открой телеграм","зайди в телеграм","зайди в телегу","включи телеграм","telegram"),
             "off" : ("выключи пк","выключи ноутбук","отключи ноутбук"),
             "sleep":("поставь ноутбук на ждущий режим","спящий режим","поставь ноутбук на спящий режим","ждущий режим"),
             "reboot" : ("перезапусти ноутбук","перезагрузи ноутбук","перезагрузка","перезагрузи пк"),
             "lock" : ("заблокируй ноутбук","блокировка","заблокируй учетную запись",),
            "stat" : ("характеристики ноутбука","характеристики системы","характеристики","информация о конфигурации"),
             "devices" : ("открой диспетчер устройств","запусти диспетчер устройств","диспетчер устройств","какие устройства подключены"),
             "tasks" :("открой диспетчер задач","запусти диспетчер задач","диспетчер задач"),
             "timetable" : ("рассписание нау"," покажи рассписание нау","включи рассписание нау","рассписание"),
             "dollar" : ("курс доллара","покажи курс доллара","какой курс доллара"),
             "movie" : ("хочу посмотреть фильм ","включи сайт кино","сайт с кино","сайт кино","скучно , хочу посмотерь фильм"),
             "jams" : ("пробки","где сейчас пробки","пробки Киев","На дороге много пробок?","Покажи пробки","Покажи пробки в Киеве"),
             "cook" : ("что бы приготовить","сайт по кулинарии","что бы приготовить на ужин","что бы приготовить на обед","что бы приготовить на завтрак"),
             'youtub': ('открой ютуб', 'хочу глянуть видео', 'хочу что-то посмотреть', 'зайди в ютуб', "включи ютуб" , "включи youtube"),
             "mypc" : ("состояние моего ноутбука","проверь состояние моего ноутбука"),
             "spdtst": ("скорость интернета","тест скорости","спидтест"," тест скорости интернета", "speedtest"),
             "reminder": ("напомни мне кое-что сделать","напомни","напоминалка","ремайндер","reminder" ),
             "memory_usage": ("использование памяти","память","память использование","отчет по использовании памяти" , "отчет по памяти")
             
             }

}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)    
    speak_engine.runAndWait()     #После фразы помощница будет молчать и ждать вашей фразы , чтобы не перебывать вас
    speak_engine.stop()


def callback(recognizer, audio):        # Функция для того , чтобы можно было узнать погоду в определенном городе
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()  # Сам распознаватель голоса
        print("[log] Распознано: " + voice)                                   # Вывод в консоль того , что смогла распознать Энигма
                       
        if voice.startswith(opts["searchweather"]):
            
            w = print("[weather] Распознано: " + voice )
            
            cmd = voice
            for x in opts['searchweather']:
                cmd = cmd.replace(x, "").strip()
            
            
            owm = pyowm.OWM('Ваш API для работы с pyowm')
            observation = owm.weather_at_place(cmd)
            wt = observation.get_weather()
            temperature = wt.get_temperature("celsius")['temp']
            wte = wt.get_detailed_status()
            speak("Время в " + str(cmd) + " в даный момент :" + str(wt.get_reference_time(timeformat='iso')) + "\n" + "Хмарность в " + str(cmd) + " сейчас " + str(wt.get_clouds()) + " процентов.\n" + "Температура равна " + str(int(temperature)) + " градусов по Цельсию. \n" + "Влажность сейчас " + str(wt.get_humidity()) + " процентов.\n" + "Время восхода солнца : " + str(wt.get_sunrise_time('iso')) + ".\n" + "Время заката: " + str(wt.get_sunset_time('iso')) + ".\n" )
            print("Состояние погоды в целом : " + wte + ".")
            
            
        
        
        elif voice.startswith(opts["wiki"]):      # Поиск информации у Википедии
                    
            n=print("[wiki] Распознано: " + voice )    
            cmd = voice
            for x in opts['wiki']:
                cmd = cmd.replace(x, "").strip()
            wikipedia.set_lang("ru")
            speak(wikipedia.summary(cmd))
        
        elif voice.startswith(opts["searchgoogle"]):  #Поиск в Гугле
            g = print("[google] Распознано: " + voice)
            command_to_search = voice
            for x in opts['searchgoogle']:
                command_to_search = command_to_search.replace(x, "").strip()
            url = "https://www.google.co.in/search?q=" +(str(command_to_search))+ "&oq="+(str(command_to_search))+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
            webbrowser.open_new(url)
        
        
        elif voice.startswith(opts["alias"]):
            # обращаются к Энигме
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

                # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
      

        
        
        
                
            
            

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == "brows":
        # открыть браузер (Гугл)
        webbrowser.open(url)

    elif cmd == "youtub":
        # Код для запуска Ютуба в браузере
        webbrowser.open(url1)
    elif cmd == "anime":
        # Код для запуска сайта с аниме - yyummyanime в браузере
        webbrowser.open(url2)
    elif cmd == "lofi":
        # Код для запуска Ютуба с критерием "lofi" в  поиске
        webbrowser.open(url3)
    elif cmd == "calend":
        # Код для вывода и озвучивания  даты
        now = datetime.datetime.now()
        print("Сегодня " + str(now.day) + "." + str(now.month)+ "."+ str(now.year))
        speak("Можете не благодарить")
    elif cmd == "list":
        # Код для запуска и озвучивания вашего списка дел (путь к нему у каждого индивидуальный ; Список нужно в ручную заполнять и изменять)
        with open("list.txt", "r") as file:
            content = file.read()
            speak(content)
    elif cmd == "news":
        # Код для запуска новостей BBC в браузере
        webbrowser.open(url4)
    elif cmd == "weather":
        # Код для запуска в браузере погодного приложения(Гугл)
        webbrowser.open(url5)
    elif cmd == "trans":
        # Код для переводчика (Гугл)
        webbrowser.open(url6)
    elif cmd == "map":
        # Код для запуска карты в браузере
        webbrowser.open(url7)
    elif cmd == "loc":
        # Код для для запуска карты с вами местоположением
        webbrowser.open(url8)
    elif cmd == "calc":
        # Код для запуска калькулятора (Пусть к Калькулятору у каждого пользователя свой)
        os.system("start C:/Users/111/calc.exe")
    elif cmd == "cam":
        # Код для запуска камеры(путь к Камере у каждого пользователя свой)
        os.system("start  C:/Users/111/Desktop/Камера")
    elif cmd == "telega":
        # Код для запуска Телеграмма(путь к Телеграмму у каждого пользователя свой)
        os.system("start C:/Users/111/AppData/Roaming/Microsoft/Windows/Telegram.lnk")
    elif cmd == "off":
        # Код для выключения вашего пк/ноутбука (спустя 1 мин)
        os.system('shutdown -s')
    elif cmd == "sleep":
        # Код для включения ждущего режима (сна) вашего пк/ноутбука
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif cmd == "reboot":
        # Код для перезагрузки вашего пк/ноутбука
        os.system("shutdown /r")
    elif cmd == "lock":
        # Код для блокировки учетной записи(для входа нужно будет ввести пароль, если такой имеется;)
        os.system("shutdown /l")
    elif cmd == "stat":
        # Код для просмотра основных характеристик Вашей системы
        st =platform.uname()
        print(st)
        speak("Как видите , выше я написала краткую информацию о характеристиках вашей системы. ")
    elif  cmd == "devices":
        # Код для вызова диспетчера устройств
        subprocess.call("control /name Microsoft.DeviceManager")
    elif cmd == "tasks":
        # Код для вызова диспетчера задач через модуль os
        os.system("start C:/Users/111/AppData/Roaming/Microsoft/Windows/Task.lnk")
    elif cmd == "timetable":
        # Код для просмотра рассписания в НАУ
        webbrowser.open(url9)
        speak("Можете не благодарить , хотя я вижу, что вы и так не сильно горели желанием.")
    elif cmd == "dollar":
        # Код для просмотра  курса доллара к гривне
        webbrowser.open(url10)
    elif cmd == "movie":
        # Для просмотра сайта с кино
        webbrowser.open(url11)
    elif cmd == "jams":
        # Для просмотра пробок на карте
        webbrowser.open(url12)
    elif cmd == "cook":
        # Код для открытия сайта по кулинарии в браузере
        webbrowser.open(url13)
    elif cmd == "mypc":
        print("Информация о памяти на вашем устройстве:\n")
        print(psutil.virtual_memory())
        print("Количество логических процессоров: "+ str(psutil.cpu_count()))
        print("Статистика о вашем ЦПУ: \n")
        print(psutil.cpu_stats())
        print("Частота вашего ЦПУ: \n")
        print(psutil.cpu_freq())
        print("Использование дисков: \n")
        print(psutil.disk_usage('/'))
        print("Общесистемные сокетные соединени: \n")
        print(psutil.net_connections())
        cpu = Cpu(monitoring_latency=1)
        speak("Температура вашего ЦПУ "+ str(cpu.temperature) + " градусов по Цельсию. "" Загруженость вашего ЦПУ: "+  str(int(psutil.cpu_percent()))+ " процентов.""Также я вывела в консоль информация о памяти на вашем устройстве , количестве логических процессоров ,  более точную статистику о вашем ЦПУ , информации  о использовании дисков , сокетных соединений. " " Посмотрите внимательнее , может найдёте что-то странное или подозрительное.")
    elif cmd == 'spdtst':
        st = pyspeedtest.SpeedTest()
        speak("Ваш пинг равен: " + str(int(st.ping())) + " миллисекунд.\n" + "Скорость приёма трафика равна: " + str(int(st.download())) + " мегабит в секунду.\n" + "Скорость отдачи трафика: " + str(int(st.upload())) + " мегабит в секунду." )
    elif cmd == 'reminder' :
        root = tk.Tk()
        root.withdraw()
        text = str(input("Введите , что именно я должна Вам напомнить: \n"))              
        local_time = float(input("Введите , через сколько минут мне Вам напомнить: \n"))
        print("Окей , будет сделано .")
        local_time = local_time * 60
        time.sleep(local_time)
        mb.showinfo("Напоминание", text)
    elif cmd ==  "memory_usage" :
        print("Информация о задейственной и свободной памяти: \n" + str(psutil.virtual_memory()))
        
        
        
    else:
        print('Команда не распознана, повторите!')

subprocess.call("control /name Microsoft.TaskManager")

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()


speak("Приветсвую , Друг")
speak("Энигма слушает")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # Бесконечный цикл
