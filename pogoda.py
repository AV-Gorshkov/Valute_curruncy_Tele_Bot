# pip install requests aiogram

import os

import requests
from setting import TG_TOKEN, Pogoda_TOKEN

import telebot
import datetime
import time
import json



from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# bot = Bot(token='your_bot_token')
bot = telebot.TeleBot(TG_TOKEN, skip_pending=True)

# Pogoda_TOKEN = 'b297aefdcbe2cb90cca6f16719a8d55f'
# @bot.message_handler()
# async def get_weather(message: types.Message):

city_name_1 = "москва"

lang = "ru"
units = "metric"
api_weather_1 = f'http://api.openweathermap.org/data/2.5/weather?q='
api_weather_2 = f'&lang={lang}&units={units}&appid={Pogoda_TOKEN}'
api_weather_3 = f'http://api.openweathermap.org/data/2.5/forecast?lat='

#  Маркер
user_marker = {}    # маркер сценария: 1 - курс валюты 2 - погода
predict_marker = {} # маркер сценария прогноза погоды
dict_predicat = {}  # словарь для прогноза на 5 дней
#  смайл погоды
code_to_smile = {
     "Clear": "Ясно \U00002600",
     "Clouds": "Облачно \U000026C5",   #\U00002601"
     "Rain": "Дождь \U00002614",
     "Drizzle": "Дождь \U0001F326",
     "Thunderstorm": "Гроза \U000026C8",
     "Snow": "Снег \U0001F328",
     "Fog": "Туман \U0001F32B",
     "Mist": "Туман \U0001F300"
}

# get(f"http://api.openweathermap.org/data/2.5/weather?q=москва&lang=ru&units=metric&appid={Pogoda_TOKEN}")
lon = "37.6156"
lat = "55.7522"

# 🌓🌕🌗⬆️↗️➡️↘️⬇️↙️⬅️↖️
#-- общие функ

# --- Роза ветров  - напрвеление ветра по град.
def rose_wind(wind):
    """     Роза ветров
        23 < ЮЗ <= 68
        68 < З <= 113
        113 < СЗ <= 158
        158 < С <= 203
        203 < СВ <= 248
        248 < В <= 293
        293 < ЮВ <= 338
        338 < Ю <= 360 and 0 < Ю <= 23
    """

    speed = round( float(wind["speed"]),1)  # ветер скорость
    deg = int(wind["deg"])     # нарпавление ветра

    if 23 < deg <= 68:
        direct = f'СВ ↗️'
    elif 68 < deg <= 113:
        direct = f'В ➡️'
    elif 113 < deg <= 158:
        direct = f'ЮВ ↘️'
    elif 158 < deg <= 203:
        direct = f'Ю ⬇️'
    elif 203 < deg <= 248:
        direct = f'ЮЗ ↙️'
    elif 248 < deg <= 293:
        direct = f'З ⬅️️'
    elif 293 < deg <= 338:
        direct = f'СЗ ↖️️️'
    else:
        direct = f'С ⬆️️'

    wind = f'{speed} {direct}'
    return wind

#----Запрос к сервису погоды
def api_weather(city_name):

    try:
        # response = requests.get(
        #     f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")
        response = requests.get(f'{api_weather_1}{city_name}{api_weather_2}')
        data = response.json()
        return data
    except:
        text = "error"
        return text

    #     #  парсим JSON запрос погоды
    #     city = data["name"]  # город
    #     temp_avg = float(data["main"]["temp"])  # температура средняя
    #     temp_min = float(data["main"]["temp_min"])  # температура min
    #     temp_max = float(data["main"]["temp_max"])  # температура max
    #     temp_feels = float(data["main"]["feels_like"])  # температура по ощущениям
    #     humidity = data["main"]["humidity"]  # влажность
    #     pressure = float(data["main"]["pressure"])  # давление гектопаскаль / 1,333
    #     wind = data["wind"]["speed"]  # ветер скорость
    #
    #     cur_weather = f'{round(temp_min, 1)}°C - {round(temp_max, 1)}°C, ощущается как {round(temp_feels, 1)}°C'  # температура для вывода
    #
    #     # получаем время рассвета и преобразуем его в читабельный формат
    #     sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M')
    #     # bot.send_message(message.chat.id, sunrise_timestamp.strftime('%H:%M') )
    #
    #     # то же самое проделаем со временем заката
    #     sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M')
    #     # продолжительность дня
    #     length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
    #                         datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    #
    #     # получаем значение погоды
    #     weather_description = data["weather"][0]["main"]
    #
    #     if weather_description in code_to_smile:
    #         wd = code_to_smile[weather_description]
    #     else:
    #         # если эмодзи для погоды нет, выводим другое сообщение
    #         wd = "Давай посмотрим в окно, я не понимаю, что там за погода..."
    #
    #     bot.send_message(message.chat.id, f"Погода на {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}:\n"
    #                                       f"В городе: {city}\nТемпература: {cur_weather}\n{wd}\n"
    #                                       f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер: {wind} м/с \n"
    #                                       f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
    #                      )
    # except:

# --- погода на 5 дней вперед
def api_predicat(lat, lon):

    try:
        # response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")

        response = requests.get(f'{api_weather_3}{lat}&lon={lon}{api_weather_2}')

        data = response.json()
        dict_param = {}       # словарь параметров погоды
        dict_predicat = {}    # словарь для сбора дата-> погода

        # ---cписок название месяца
        month_list = ['Янв.', 'Фев.', 'Мар.', 'Апр.', 'Май', 'Июн.',\
                      'Июл.', 'Авг.', 'Сен.', 'Окт.', 'Ноя.', 'Дек.']

        for i, line in enumerate(data['list']):

            dt_obj = datetime.datetime.strptime(line['dt_txt'], '%Y-%m-%d %H:%M:%S')   # дата в формате ПИТОНА Дате-Тайм

            # берем час, день и месяц для вывода на экран
            int_Hours = int(datetime.datetime.strftime(dt_obj, '%H'))
            int_Mon = int(datetime.datetime.strftime(dt_obj, '%m'))
            int_Day = int(datetime.datetime.strftime(dt_obj, '%d'))
            data_next = datetime.datetime.strftime(dt_obj, '%Y-%m-%d')

            #  смайл для часов
            if int_Hours < 7:
                p_time = f'🌗'
            elif int_Hours < 13:
                p_time = f'🌕️'
            else:
                p_time = f'🌓️'

            text_data = f'{int_Day} {month_list[int_Mon - 1]}'
            text_time = f'{p_time} {int_Hours}:00'

            temp_min = float(line["main"]["temp_min"])  # температура min
            temp_max = float(line["main"]["temp_max"])  # температура max
            temp_feels = float(line["main"]["feels_like"])  # температура по ощущениям
            humidity = line["main"]["humidity"]  # влажность
            pressure = float(line["main"]["pressure"])  # давление гектопаскаль / 1,333
            wind = rose_wind(line["wind"])  # словарь с параметрами ветра в функцию
            cur_weather = f"{round(temp_min, 1)}°...{round(temp_max, 1)}°C, ощущается как {round(temp_feels, 1)}°C"   # температура для вывода

            # получаем значение погоды для смайла
            weather_description = line["weather"][0]["main"]

            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                # если эмодзи для погоды нет, выводим другое сообщение
                wd = "Посмотрим в окно, я не понимаю, что там за погода...\U0001F32A"

            param = f"{wd}\n{cur_weather}\n"

            if i == 0:
                # погода на сейчас
                data_start = datetime.datetime.strftime(dt_obj, '%Y-%m-%d')
                param_st = f"{param}Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                dict_param[text_time] = param_st
                dict_predicat[text_data] = dict_param
            else:
                if data_start == data_next:
                    # запись в словарь прогноза погоды на 6-12-18 часов
                    if int_Hours == 6 or int_Hours == 12:
                        param_12 = f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                        dict_param[text_time] = param
                        dict_predicat[text_data] = dict_param
                    elif int_Hours == 18:
                        if len(param_12) == 0:
                            param_18 = f"{param}Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                            dict_param[text_time] = param_18
                            dict_predicat[text_data] = dict_param
                        else:
                            dict_param[text_time] = f'{param}{param_12}'
                            dict_predicat[text_data] = dict_param
                    else:
                        pass
                else:
                    data_start = data_next
                    dict_param = {}

                    if int_Hours == 6 or int_Hours == 12:
                        param_12 = f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                        dict_param[text_time] = param
                        dict_predicat[text_data] = dict_param
                    elif int_Hours == 18:
                        if len(param_12) == 0:
                            param_18 = f"{param}Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                            dict_param[text_time] = param_18
                            dict_predicat[text_data] = dict_param
                        else:
                            dict_param[text_time] = f'{param}{param_12}'
                            dict_predicat[text_data] = dict_param

        return dict_predicat
    except:
        text = "error"
        return text

    # bot.send_message(message.chat.id, f'Дата\n{data}')

    # f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang={lang}&units={units}&appid={Pogoda_TOKEN}"

    #
    # # api.openweathermap.org / data / 2.5 / forecast?    lat={lat}&lon={lon}&lang={lang}&units={units}&appid={Pogoda_TOKEN}
    # # key}
    # # response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name_1}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")
    #
    # # bot.send_message(message.chat.id, f"http://api.openweathermap.org/data/2.5/weather?q={city_name_1}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")
    # data = response.json()
    #
    # # bot.send_message(message.chat.id, response)
    # bot.send_message(message.chat.id, f'Дата\n{data}')


# ----- команда прогноз погоды /predict
@bot.message_handler(commands=['Погода', 'погода', 'ПОГОДА', 'predict', 'Predict', 'PREDICT'])
def predict(message):
    user_id = str(message.from_user.id)
    user_marker[user_id] = 2
    predict_marker[user_id] = 1

    bot.send_message(message.chat.id, 'Введите название города, и я покажу прогноз погоды на ближайшие дни')



# @bot.message_handler(commands=['st'])
# def star(message):

# @bot.message_handler(commands=["1"])
# def menu(message):
#
#     try:
#         response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=москва&lang=ru&units=metric&appid={Pogoda_TOKEN}")
#         # response = requests.get( r"http://api.openweathermap.org/data/2.5/weather?q=москва&lang=ru&units=metric&appid=b297aefdcbe2cb90cca6f16719a8d55f")
#         data = response.json()
#
#         city = data["name"]
#         cur_temp = data["main"]["temp"]
#         humidity = data["main"]["humidity"]
#         pressure = data["main"]["pressure"]
#         wind = data["wind"]["speed"]

#     {
#     "coord":{ "lon":37.6156,"lat":55.7522},
#     "weather":[{"id":803,"main":"Clouds","description":"облачно с прояснениями","icon":"04n"}],
#     "base":"stations",
#     "main":{"temp":14.13,"feels_like":12.98,"temp_min":12.86,"temp_max":15.61,"pressure":1016,"humidity":53,"sea_level":1016,"grnd_level":999},
#     "visibility":10000,
#     "wind":{"speed":1.23,"deg":296,"gust":2.67},
#     "clouds":{"all":63},
#     "dt":1692988134,
#     "sys":{"type":2,"id":2000314,"country":"RU","sunrise":1692929998,"sunset":1692981841},
#     "timezone":10800,
#     "id":524901,
#     "name":"Москва",
#     "cod":200}
#



#         # получаем время рассвета и преобразуем его в читабельный формат
#         sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
#         # то же самое проделаем со временем заката
#         sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
#
#         # продолжительность дня
#         length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
#
#         bot.send_message(message.chat.id,data["name"] +  data["main"]["temp"]+  data["main"]["humidity"]+  data["main"]["pressure"] + data["wind"]["speed"])
#
#
#         bot.send.message(message.chat.id, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
#             f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
#             f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
#             f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
#              f"Хорошего дня!")

    # except:
    #     bot.send_message(message.chat.id, "Проверьте название города!")


 # = = = Выполнение сценариев = = =
@bot.message_handler(content_types=["text"])
def echo(message):
    # city_name = "москва"
    user_id = str(message.from_user.id)
    city_name = message.text.lower().replace(" ","")

    predict_marker[user_id] = 1
    user_marker[user_id] = 2

# ----- сценарий Погода
    if user_marker[user_id] == 2:

        # запрос к серверу погоды
        data = api_weather(city_name)
        if data == "error":
            bot.send_message(message.chat.id, f'❌ Cервис недоступен')

        elif data.get("name") is None:
            bot.send_message(message.chat.id, f'❌ Неизвестная команда.\nПроверьте название города')
        else:

        #  прогноз на несколько дат
            if predict_marker[user_id] == 1:
                # координаты города из запроса
                lon = data["coord"]["lon"]
                lat = data["coord"]["lat"]
                data = api_predicat(lat, lon)

                text = ""
                for dt, line in data.items():
                    text = f'{text}{dt}\n'
                    for hours, parm in line.items():
                        text = f'{text}{hours}: {parm}'
                    text = f'{text}\n'

                bot.send_message(message.chat.id, text)


        #  погода на сегодня
            elif predict_marker[user_id] == 0:

                #  парсим JSON запрос погоды
                city = data["name"]          # город
                temp_avg = float(data["main"]["temp"])          # температура средняя
                temp_min = float(data["main"]["temp_min"])      # температура min
                temp_max = float(data["main"]["temp_max"])      # температура max
                temp_feels = float(data["main"]["feels_like"])  # температура по ощущениям
                humidity = data["main"]["humidity"]             # влажность
                pressure = float(data["main"]["pressure"])      # давление гектопаскаль / 1,333
                wind = rose_wind(data["wind"])                      # словарь с параметрами вертра в функцию

                # wind = data["wind"]["speed"]                    # ветер скорость
                # rose_w = rose_wind( int(data["wind"]["deg"]) )  # нарпавление ветра

                cur_weather = f'{round(temp_min,1)}°...{round(temp_max,1)}°C, ощущается как {round(temp_feels,1)}°C'  # температура для вывода

                # получаем время рассвета и преобразуем его в читабельный формат
                sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M')
                # bot.send_message(message.chat.id, sunrise_timestamp.strftime('%H:%M') )

                # то же самое проделаем со временем заката
                sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M')
                # продолжительность дня
                length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                                    datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

                # получаем значение погоды для смайла
                weather_description = data["weather"][0]["main"]

                if weather_description in code_to_smile:
                    wd = code_to_smile[weather_description]
                else:
                    # если эмодзи для погоды нет, выводим другое сообщение
                    wd = "Посмотрим в окно, я не понимаю, что там за погода...\U0001F32A"

                bot.send_message(message.chat.id, f"Погода на {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}:\n"
                      f"В городе: {city}\nТемпература: {cur_weather}\n{wd}\n"
                      f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333 , 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                      f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                     )

# ---Сценарий курс валют
    elif user_marker[user_id] == 1:
        pass

# --- нет команды
    else:
        bot.send_message(message.chat.id, f'❌ Неизвестная команда.\nПроверьте название города')

while True:
  try:
    bot.polling(none_stop=True)
  except Exception as _ex:
    # print(_ex)
    time.sleep(15)

 #    построчный вывод сообщения
    # if len(str(data)) > 4096:
    #     for x in range(0, len(str(data)), 4096):
    #         bot.send_message(message.chat.id, str(data)[x:x + 4096])
    # else:
    #     bot.send_message(message.chat.id, str(data))

    # ----Пример
    # ob = '2023-08-25 21:00:00'
    #
    # dt_ob = datetime.datetime.strptime(ob, '%Y-%m-%d %H:%M:%S')
    #
    # text_H = int(datetime.datetime.strftime(dt_ob, '%H'))
    # text_M = int(datetime.datetime.strftime(dt_ob, '%m'))
    # text_D = int(datetime.datetime.strftime(dt_ob, '%d'))
    #
    # text_1 = datetime.datetime.strftime( \
    #     datetime.datetime.strptime(ob, '%Y-%m-%d %H:%M:%S'), \
    #     '%d %B. %H:%M')