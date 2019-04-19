#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# import time
# import datetime
# import os
# os.system('clear') - linux.Windows- os.system('CLS').
import os  # Подкл библиотеку , можем выполнять команды в терминале,для определения ip
import shutil #Для удаление каталога с файлами
import time
import threading  # Потоки
import datetime  # определение времени и даты
import os
import smtplib  # для отправки почты
from datetime import datetime
import subprocess #для присвоение переменной результат команды system()
import commands #для проверки даты создания последнего файла функция videosrv()






def log(message):
    try:
        print("\n -0---0----0---0--0---0--0--")
        from datetime import datetime
        print(datetime.now())
        print(message)
        print("-1-----1-----1-----1-----1---1--")
        datein = datetime.strftime(datetime.now(), "%d.%m.%Y")
        if os.path.exists('/home/pi/myprogramming/videoserver/log'):
            print("Проверка существования папки по пути: /home/pi/myprogramming/videoserver/log")

            datein = datetime.strftime(datetime.now(), "%d_%m_%Y")
            file = open('/home/pi/myprogramming/videoserver/log/' + datein + '.log', 'a')
            file.write("\n")
            file.write("\n")
            file.write("-0---0----0---0--0---0--0--")
            file.write("\n")
            file.write(str(datetime.now()))
            file.write("\n")
            file.write(message)
            file.write("\n")
            file.write("-1-----1-----1-----1-----1---1--")
            file.write("\n")
            file.write("\n")
            file.close()
        else:
            os.makedirs('/home/pi/myprogramming/videoserver/log')  # Создаю такую папку и пишу в нее
            print("Создал папку по пути: /home/pi/myprogramming/videoserver/log")
            datein = datetime.strftime(datetime.now(), "%d_%m_%Y")
            file = open('/home/pi/myprogramming/videoserver/log/' + datein + '.log', 'a')
            file.write("\n")
            file.write("\n")
            file.write("-0---0----0---0--0---0--0--")
            file.write("\n")
            file.write(str(datetime.now()))
            file.write("\n")
            file.write(message)
            file.write("\n")
            file.write("-1-----1-----1-----1-----1---1--")
            file.write("\n")
            file.write("\n")
            file.close()
    except Exception as err:
        log("Сработало Исключение в функции log.")
        log(str(err))



def email(emailmessage):
    try:
        smtpUser = 'от кого@mail.ru'
        smtpPass = 'пароль'
        toAdd = 'кому@mail.ru'
        fromAdd = smtpUser
        subject = 'Оповещение!'
        header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
        body = emailmessage
        print(header + '\n' + body)
        s = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n\n' + body)
        s.quit()
    except Exception as err:
        log("Сработало Исключение в функции email.")
        log(str(err))
        print("Сработало Исключение в функции email.")
        print(str(err))





def controlwritedisc():
    try:
        while True:
            time.sleep(60)
            resourcescpu = subprocess.check_output('ps -eo cmd,%cpu --sort=-%cpu | head', shell=True)
            print(resourcescpu)
            index = resourcescpu.find("ffmpeg")
            print(index)
            if index != -1:
                resourcescpu = resourcescpu[index:index + 33]
                print(resourcescpu)
                print(len(resourcescpu))
                if resourcescpu[31] != ' ':
                    text = resourcescpu[31]
                    if resourcescpu[30] != ' ':
                        text = text + resourcescpu[30]
                        if resourcescpu[29] != ' ':
                            text = text + resourcescpu[29]
                            if resourcescpu[28] != ' ':
                                text = text + resourcescpu[28]
                                if resourcescpu[27] != ' ':
                                    text = text + resourcescpu[27]
                text = text[::-1]
                cpuload = float(text)
                if cpuload < 20.0:
                    i = 0
                    while i < 10:
                        resourcescpu = subprocess.check_output('ps -eo cmd,%cpu --sort=-%cpu | head', shell=True)
                        index = resourcescpu.find("ffmpeg")
                        if index != -1:
                            resourcescpu = resourcescpu[index:index + 33]
                            print(resourcescpu)
                            print(len(resourcescpu))
                            if resourcescpu[31] != ' ':
                                text = resourcescpu[31]
                                if resourcescpu[30] != ' ':
                                    text = text + resourcescpu[30]
                                    if resourcescpu[29] != ' ':
                                        text = text + resourcescpu[29]
                                        if resourcescpu[28] != ' ':
                                            text = text + resourcescpu[28]
                                            if resourcescpu[27] != ' ':
                                                text = text + resourcescpu[27]
                            text = text[::-1]
                            cpuload = float(text)
                            if cpuload < 20.0:
                                i = i + 1
                                if i == 9:
                                    log("процесс ffmpeg потребляет менее 20%. Kill ffmpeg")
                                    os.system('killall - s 9 ffmpeg')
                            else:
                                break
                        time.sleep(10)
            else:
                log("ндекс == -1 значит процесса ffmpeg нет в head ввеху топа значит запись не идет килл ffmpeg")
                os.system('killall - s 9 ffmpeg')
    except Exception as err:
        log("Исключение функция controlwritedisc не сработала, запускаем заново функцию через 60 секунд.")
        log(str(err))
        email("Исключение функция controlwritedisc не сработала, запускаем заново функцию через 60 секунд.")
        email(str(err))
        time.sleep(60)
        log("перезапущена функция controlwritedisc")
        controlwritedisc()



def cleardisk():
    try:
        while True:
            time.sleep(600)
            textnamedisk = subprocess.check_output('df -h', shell=True)
            index = textnamedisk.find("/dev/sd")
            index = index + 5
            textnamedisk = textnamedisk[index:index + 4]
            print(textnamedisk)
            output = subprocess.check_output('df -h /dev/' + textnamedisk, shell=True)
            lst = output.split()
            lst = lst[11]
            lst = lst[:-1]
            lst = int(lst)
            print("Тип lst:")
            print(type(lst))
            if (lst > 90):
                email("Videoserver: Диск занят более 90%, запускается cleardisk")
                textnamedisk = subprocess.check_output('df -h', shell=True)
                index = textnamedisk.find("media")
                index = index + 9
                textnamedisk = textnamedisk[index:]
                textnamedisk = textnamedisk[:-1]
                path = '/media/pi/' + textnamedisk
                name_list = os.listdir(path)
                full_list = [os.path.join(path, i) for i in name_list]
                time_sorted_list = sorted(full_list, key=os.path.getmtime)
                shutil.rmtree(time_sorted_list[0])
                shutil.rmtree(time_sorted_list[1])
                shutil.rmtree(time_sorted_list[2])
                shutil.rmtree(time_sorted_list[3])
                shutil.rmtree(time_sorted_list[4])
                email("Videoserver: Удалены старые 5 папок.")
            else:
                print(1)
    except Exception as err:
        log("Исключение функция cleardisk не сработала, запускаем заново функцию через 60 секунд.")
        log(str(err))
        email("Исключение функция cleardisk не сработала, запускаем заново функцию через 60 секунд.")
        email(str(err))
        time.sleep(60)
        log("перезапущена функция cleardisk")
        cleardisk()



def videosrv():
    try:
        while True:
            now = datetime.now()
            datein = datetime.strftime(datetime.now(), "%d.%m.%Y")
            dirpath = datein
            gettime1 = 60 - now.minute
            if now.minute < 30:
                gettime1 = 30 - now.minute
            gettime1 = gettime1 * 60
            textnamedisk = subprocess.check_output('df -h', shell=True)
            index = textnamedisk.find("media")
            textnamedisk = textnamedisk[index:]
            textnamedisk = textnamedisk[:-1]
            print(textnamedisk)
            if os.path.exists('/media/pi/' + textnamedisk + '/' + dirpath):
                os.system('ffmpeg -t ' + str(gettime1) + ' -i rtsp://admin:password@192.168.1.69:554/onvif1' + ' /media/pi/' + textnamedisk + '/' + dirpath + '/' + '`date +%d.%m.%Y-%H:%M:%S`.avi')
            else:
                os.makedirs('/media/pi/' + textnamedisk + '/' + dirpath)
                os.system('ffmpeg -t ' + str(gettime1) + ' -i rtsp://admin:password@192.168.1.69:554/onvif1' + ' /media/pi/' + textnamedisk + '/' + dirpath + '/' + '`date +%d.%m.%Y-%H:%M:%S`.avi')
    except Exception as err:
        log("Исключение функция videosrv не сработала, запускаем заново функцию через 60 секунд.")
        log(str(err))
        email("Исключение функция videosrv не сработала, запускаем заново функцию через 60 секунд.")
        email(str(err))
        os.system('killall - s 9 ffmpeg')
        time.sleep(60)
        log("перезапущена функция videosrv")
        videosrv()

e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()

t1 = threading.Thread(target=videosrv, name="potok1-videosrv")
t2 = threading.Thread(target=cleardisk, name="potok2-cleardisk")
t3 = threading.Thread(target=controlwritedisc, name="potok3-controlwritedisc")
#Задержка запуска потоков, потому что винчестер не успевал примонтироваться
print("Задержка 15 сек. для монтирования винчестера")
time.sleep(15)
# start threads
log("Запуск 1-го и 2-го и 3-го потоков, старт программы")
t1.start()
t2.start()
t3.start()
# e1.set() # initiate the first event
# join threads to the main thread
t1.join()
t2.join()
t3.join()
log("Потоки отключены конец программы")
