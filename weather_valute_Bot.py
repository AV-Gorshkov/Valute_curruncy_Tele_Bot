
import requests
from setting import TG_TOKEN, Pogoda_TOKEN

import telebot
from telebot import types
import datetime
import time
import re
import os
import json

#===================
#    # Отправляем       # длинное       # сообщение       # по       # частям
    # log_query = requests.get(api_log)    # - текст длинного сообщения с сайта через API от сервера

    # currency_dict = log_query.json()['Valute']    # перевод в JSON ответа от сервера

    # todos = log_query.json()['Valute']   # данные в формате JSON

    # if len(str(todos)) > 4096:
    #     for x in range(0, len(str(todos)), 4096):
    #         bot.send_message(message.chat.id, str(todos)[x:x + 4096])
    # else:
    #     bot.send_message(message.chat.id, str(todos))
# ==========================



#----- Для REPL-IT
# # === обращение к БД Replit, поддержка работы 24/7

# import os
# import requests
# from backgroud import keep_alive  #импорт функции для поддержки работоспособности
#
# # from replit import db
# # import base
#
# import pip
# pip.main(['install', 'pytelegrambotapi'])
#
# import telebot
# from telebot import types
# import time
# import datetime
# import json
# import re
#
#
# my_secret = os.environ['token']
# my_secret_2 = os.environ['Pogoda_TOKEN']
#
# bot = telebot.TeleBot(my_secret, skip_pending=True)
# -----------------------------


bot = telebot.TeleBot(TG_TOKEN, skip_pending=True)

# 💹💰💴💵💶💷💸💲
# 📈📉📊

HELP = """
Приветствую!✌️ Я Чат-Бот! 
📊 Подскажу тебе курс самых популярных валют на текущую дату по курсу ЦБ РФ, или прогноз погоды в твоем городе! 🌤️🤷‍♂️☔
Нажми на кнопку ниже, что бы узнать функционал доступных команд и их описание:
©️
"""

#  ---------------- описание вызываемых команд
MENU = """✏️ Команды доступные в приложении:
/help - (Нelp, Справка, ? ) - вызов справки о программе, знакомство с приложением.
/info - (Info, Описание) - описание действия команд и кнопок приложения.
/list - (List, Список) - список валют, доступных для просмотра.
/end - (/End, /Отмена, /) -  отмена всех команд.
/usd - (/Usd, /Eur) - курс Доллара, Евро и изменение с предыдущем значением. 
/multy - (/Multy, /Мульти) - конвертер валют.
/weather - (/Weather, /Погода) - прогноз погоды на сегодня.
/predict - (/predict, /Прогноз) - прогноз погоды на несколько дней.
/menu - (Menu, Меню) - Меню - список доступных команд приложения.
"""

INFO = """ Описание взаимодействия с приложением:
✔️ Все команды из списка в "Menu" вызываются через слэш "/" 
(Пример: /list, /usd, /weather, /Menu)
✔️ Информация по курсу для одной валюты - ввести ID валюты из списка валют
(Пример: eur, NZD, Usd)
✔️ Информация о погоде в любом городе мира - ввести название города.
(Пример: Москва, санкт-петербург, PARIS, Viena)
✔️ Конвертер валют - информация о курсе выбранных валют. 
В качестве разделителя может быть: точка, тире, пробел
(Пример: usd-eur, AUD . NOK, Czk Zar)
"""

# ===== Блок переменных
dict_currency = {}   # словарь валют
# --- Маркер
user_marker = {}     # маркер сценария: 1 - курс валюты 2 - погода
predict_marker = {}  # маркер сценария прогноза погоды

# --- Базовые параметры

time_mow = 10800 # часовой пояс по Москве +3 ч - для ReplIT

api_log = 'https://www.cbr-xml-daily.ru/daily_json.js'  # сервис валют

# - сервис погоды
lang = "ru"   # русская локаль - ответы в поле text на русском
# units = "metric"
# - запрос текущей погоды
api_weather_1 = f"http://api.weatherapi.com/v1/current.json?key={Pogoda_TOKEN}&lang={lang}&q="

# - запрос прогноза погоды &days=3 (кол-во дней до 14 дней)
api_weather_2 = f"http://api.weatherapi.com/v1/forecast.json?key={Pogoda_TOKEN}&lang={lang}&q="

# --- словарь знаков валюты
dict_symbol = {"AUD": "$", "AZN": "₼", "GBP":"£", "AMD":"Դ", "BYN":"Br", "BGN":"лв", "BRL":"R$", "HUF":"Ft", "VND":"₫",
       "HKD":"$", "GEL":"₾", "DKK":"kr", "AED":"Dh", "USD":"$", "EUR":"€", "EGP":"£", "INR":"र", "IDR":"Rp",
       "KZT":"〒", "CAD":"$", "QAR": "Dh", "KGS":"с", "CNY":"元", "MDL":"L", "NZD":"$", "NOK":"kr", "PLN":"zł",
       "RON":"L", "XDR": "XDR", "SGD": "$", "TJS": "с.", "THB": "฿", "TRY": "TL", "TMT": "m", "UZS": "сўм", "UAH": "₴",
       "CZK":"Kč", "SEK":"kr", "CHF":"₣", "RSD":"RSD", "ZAR":"R", "KRW": "₩", "JPY": "¥", "RUR": "₽"}

# --- смайл погоды
code_to_smile = {
     "ясно": " \U00002600",
     "солнечно": " \U0001F31E",
     "пасмурно": " \U0001F325",
     "облачно": " \U000026C5",   #\U00002601"
     # "дождь": "Дождь \U00002614",
     "дождь": " \U0001F326",
     "гроза": " \U000026C8",
     "снег": " \U0001F328",
     "туман": " \U0001F32B",
     "морось": " \U0001F4A7",
     "дымка": " \U0001F300"
}
# --- список название месяца
month_list = ['Янв.', 'Фев.', 'Мар.', 'Апр.', 'Май', 'Июн.', 'Июл.', 'Авг.', 'Сен.', 'Окт.', 'Ноя.', 'Дек.']

# = = = Общие функции
# ---запрос к серверу валют
def dict_curr():
    # запрос к сайту
    log_query = requests.get(api_log)
    currency_dict = log_query.json()['Valute']  # перевод в JSON ответа от сервера
    """
    формат ответа JSON
    {
        'CharCode': 'EUR',    - код валюты
        'ID': 'R01239',       - ID номер
        'Name': 'Евро',       - название валюты      
        'Nominal': 1,         - номинал (объем продажи)  
        'NumCode': '978',     - код....
        'Previous': 79.6765,  - предыдущее значение (вчера)
        'Value': 79.4966      - значение сегодня
            }
    """
    # создание словаря:  { EUR :[Евро, 79.4966, 79.6765, 1,]}
    for curr, list_val in currency_dict.items():
        dict_currency[curr] = [list_val['Name'], round( float(list_val['Value']), 2), round( float(list_val['Previous']), 2), list_val['Nominal']]

    return dict_currency

# - - - список ID - название валюты (EUR -  Евро)
def list_curr():
    list_valute = dict_curr()
    text = ''
    for key, val in list_valute.items():

        #  вывод знака валюты из словаря dict_symbol
        if dict_symbol.get(key) is None:
            text = f'{text}/{key} - {val[0]}\n'
        else:
            symbol = dict_symbol[key]
            text = f'{text}/{key} - {val[0]} ({symbol})\n'
    return text

#  - - - Курс ерво и доллара
def usd_eur():
    valute = dict_curr()  # запрос словаря из функции
    text = f'💹 Курсы валют на сегодня:\n'

    # $ USD разность курса сегодня - вчера
    delta_usd = round(float(valute["USD"][1]) - float(valute["USD"][2]), 2)
    if delta_usd > 0:
        text_usd = f'USD {valute["USD"][1]} ₽ за {valute["USD"][3]} $ (+{delta_usd}) 🟢 ⬆️\n'
    elif delta_usd == 0:
        text_usd = f'USD {valute["USD"][1]} ₽ за {valute["USD"][3]} $ ({delta_usd}) 🟠 ⏸️\n'
    else:
        text_usd = f'USD {valute["USD"][1]} ₽ за {valute["USD"][3]} $ (-{abs(delta_usd)}) 🔴 ️⬇️\n'

    # € EUR разность курса сегодня - вчера
    delta_eur = round(float(valute["EUR"][1]) - float(valute["EUR"][2]), 2)
    if delta_eur > 0:
        text_eur = f'EUR {valute["EUR"][1]} ₽ за {valute["EUR"][3]} € (+{delta_eur}) 🟢 ⬆️\n'
    elif delta_usd == 0:
        text_eur = f'EUR {valute["EUR"][1]} ₽ за {valute["EUR"][3]} € ({delta_eur}) 🟠 ⏸️\n'
    else:
        text_eur = f'EUR {valute["EUR"][1]} ₽ за {valute["EUR"][3]} € (-{abs(delta_eur)}) 🔴 ️⬇️\n'

    return text + text_usd + text_eur

#  - - -Курс любой валюты, по запросу пользователя
def full_curr(word):
    valute = dict_curr()
    text_0 = f'💹 Курс валюты на сегодня:\n{valute[word][0]}\n'

    # значок валюты из словаря
    if dict_symbol.get(word) is None:
        sym = ""
    else:
        sym = str(dict_symbol[word])

    # разность курса сегодня - вчера
    delta = round(float(valute[word][1]) - float(valute[word][2]), 2)

    if delta > 0:
        text_1 = f'₽ {valute[word][1]} за {valute[word][3]} {sym} (+{delta}) 🟢 ⬆️'
    elif delta == 0:
        text_1 = f'₽ {valute[word][1]} за {valute[word][3]} {sym} (+{delta}) 🟠 ⏸️'
    else:
        text_1 = f'₽ {valute[word][1]} за {valute[word][3]} {sym} (-{abs(delta)}) 🔴 ️⬇️'

    return text_0 + text_1

# --- Роза ветров  - направление ветра по градусам
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
    deg = int(wind)     # нарпавление ветра

    if 23 < deg <= 68:
        # direct = f'СВ ↙️'
        direct = f'Северо-Восточный ↙️'
    elif 68 < deg <= 113:
        # direct = f'В ⬅️'
        direct = f'Восточный ⬅️'
    elif 113 < deg <= 158:
        # direct = f'ЮВ ↖️'
        direct = f'Юго-Восточный ↖️'
    elif 158 < deg <= 203:
        # direct = f'Ю ⬆️️'
        direct = f'Южный ⬆️️'
    elif 203 < deg <= 248:
        # direct = f'ЮЗ ↗️'
        direct = f'Юго-Западный ↗️'
    elif 248 < deg <= 293:
        # direct = f'З ➡️'
        direct = f'Западный ➡️'
    elif 293 < deg <= 338:
        # direct = f'СЗ ↘️'
        direct = f'Северо-Западный ↘️'
    else:
        # direct = f'С ⬇️'
        direct = f'Северный ⬇️'

    wind = direct
    return wind

#  - смайл температуры
def temp_smile(temp):
    temp = float(temp)

    if temp > 25:
        text = '\U0001F321'      #   🌡️
    elif temp > 18:
        text = '\U0001F3D6'     # '\U000026F1'  🏖️
    elif temp > 10:
        text = '\U0001F31E'           #   🌞
    elif temp > 3:
        text = '\U0001F9E2'     #\U0001F576'
    elif temp > -3:
        text = '\U00002744'
    elif temp < -10:
        text = '\U0001F9E3'
    elif temp < -20:
        text = '\U00002603'
    return text

# --- Запрос к сервису погоды
def api_weather(city_name):

    try:
        response = requests.get( f'{api_weather_1}{city_name}' )

        # data = response.json()

        data = response.json()

        return data
    except:
        text = "error"
        return text

#  --- Парсинг погоды на сегодня
def weather_loc(data):
    # передаем словарь data (JSON)

    # для вывода даты и часов
    # ------------------------------- погода по Моске + 3 часа для replIt
    # delta = int(datetime.datetime.fromtimestamp(timezone).strftime('%H'))
    # dt_obj = datetime.datetime.now() + datetime.timedelta(hours=delta)
    # ---------------------------------------------------------------------

    dt_obj = datetime.datetime.fromtimestamp(int( data["location"]["localtime_epoch"] ) )  # .strftime('%Y-%m-%d %H:%M:%S')
    # dt_obj = datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')
    # dt_obj = datetime.datetime.fromtimestamp(int(data["dt"]) + int(data["timezone"]))  # для ReplIT учет час.поясов

    int_Hours = int(datetime.datetime.strftime(dt_obj, '%H'))
    int_Mon = int(datetime.datetime.strftime(dt_obj, '%m'))
    int_Day = int(datetime.datetime.strftime(dt_obj, '%d'))

    text_data = f'{int_Day} {month_list[int_Mon - 1]}'

    #  смайл для часов
    if int_Hours < 5:
        p_time = f'🌑'
    elif int_Hours < 10:
        p_time = f'🌗'
    elif int_Hours < 17:
        p_time = f'🌕️'
    else:
        p_time = f'🌓️'
    #  - для сервера replIT  возращается время минс 3 часа datetime.datetime.now()
    # text_time = f"{p_time} {text_data} {datetime.datetime.now().strftime('%H:%M')}"

    text_time = f"{p_time} {text_data}"

    #  парсим JSON запрос погоды
    city = data["location"]["name"]  # город

    temp_avg = float(data["current"]["temp_c"])  # температура средняя
    temp_feels = float(data["current"]["feelslike_c"])  # температура по ощущениям
    humidity = data["current"]["humidity"]  # влажность
    pressure = float(data["current"]["pressure_mb"])  # давление гектопаскаль / 1,333
    wind = rose_wind(int( data["current"]["wind_degree"] ) )  # словарь с параметрами ветра в функцию
    wind_speed = round( data["current"]["wind_kph"] * 1000 / 3600, 1)  # скорость ветра в м/с
    #
    cur_weather = f'{round(temp_avg, 1)}°C,' \
                  f' ощущается как {round(temp_feels, 1)}°C {temp_smile(round(temp_feels, 1))}'  # температура для вывода

    # # получаем значение погоды для смайла
    weather_description = data["current"]["condition"]["text"]
    #
    for smile in code_to_smile.keys():
        match_ = re.search(smile, weather_description.replace(" ", "").lower())
        if match_:
            wd = f'{weather_description}{code_to_smile[smile]}'
            break
    else: # если эмодзи для погоды нет, выводим другое сообщение
        wd = f'{weather_description}...посмотрим в окно, я не понимаю, что там за погода...\U0001F32A'
    #
    weather_text = f"{text_time}\nВ городе {city}: {datetime.datetime.strftime(dt_obj, '%H:%M')}...{wd}\n"\
          f"Температура: {cur_weather}\n"\
          f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер: {wind_speed}м/с {wind}"
    return weather_text

# --- погода на X дней вперед (по умолчанию сегодня + 5 дней прогноза)
def api_predicat(city_name, days=6):

    try:
        response = requests.get(f'{api_weather_2}{city_name}&days={days}')
        data = response.json()

        dict_param = {}       # словарь параметров погоды
        dict_predicat = {}    # словарь для сбора дата-> погода
        param_end = ''        # переменная сбора парамеров погоды для вывода
        list_hour = [0, 6, 12, 18, 21]  # вывод по часам 0/6/12/18/21
        day = 0               # кол-во дней для вывода прогноза

        # погода сегодня
        wheather_now = weather_loc(data)

        # дата начала прогноза (дата сегодня не попадает в прогноз)
        st_dt_obj = datetime.datetime.fromtimestamp(int(data["location"]["localtime_epoch"]))
        st_int_Hours = int(datetime.datetime.strftime(st_dt_obj, '%H'))
        st_date = datetime.datetime.strftime(st_dt_obj, '%Y-%m-%d')

        #  проход по датам прогноза
        for  line in data["forecast"]["forecastday"]:
            dict_param = {}

            # проход по часам в дате
            for hour in line["hour"]:
                dt_obj = datetime.datetime.fromtimestamp(int( hour['time_epoch'] ) )

                # берем час, день и месяц для вывода на экран
                int_Hours = int(datetime.datetime.strftime(dt_obj, '%H'))
                date_next = datetime.datetime.strftime(dt_obj, '%Y-%m-%d')

                # вывод по часам 0/6/12/18/21
                if int_Hours in list_hour:

                    if (st_date == date_next and int_Hours > st_int_Hours) or (st_date != date_next):

                        int_Mon = int(datetime.datetime.strftime(dt_obj, '%m'))
                        int_Day = int(datetime.datetime.strftime(dt_obj, '%d'))

                        #  смайл для часов
                        if int_Hours < 7:
                            p_time = f'🌗'
                        elif int_Hours < 13:
                            p_time = f'🌕️'
                        else:
                            p_time = f'🌓️'

                        text_data = f'{int_Day} {month_list[int_Mon - 1]}'
                        text_time = f'{p_time} {int_Hours}:00'

                        temp = float(hour["temp_c"])  # температура сред
                        temp_feels = round( float(hour["feelslike_c"]), 1)  # температура по ощущениям
                        humidity = hour["humidity"]  # влажность
                        pressure = float(hour["pressure_mb"])  # давление гектопаскаль / 1,333
                        wind = rose_wind( int( hour["wind_degree"] ) )  # словарь с параметрами ветра в функцию

                        cur_weather = f"{round(temp, 1)}°C (ощущается как {temp_feels}°C)"\
                                      f" {temp_smile(temp_feels)}"   # температура для вывода

                        # получаем значение погоды для смайла
                        weather_description = hour["condition"]["text"]

                        for smile in code_to_smile.keys():
                            match_ = re.search( smile, weather_description.replace(" ", "").lower() )
                            if match_ :
                                wd = f'{weather_description}{code_to_smile[smile]}'
                                break
                        else:  # если эмодзи для погоды нет, выводим другое сообщение
                            wd = f'{weather_description}...посмотрим в окно, я не понимаю, что там происходит...\U0001F32A'

                        wind_temp = f"{wd} {cur_weather}\n"

                        if int_Hours == 12:
                            param_end =  f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"

                        if int_Hours == 21:
                            if len(param_end) == 0 :
                                param_end = f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"

                            dict_param[text_time] = f'{wind_temp}{param_end}'
                            dict_predicat[text_data] = dict_param
                        else:
                            dict_param[text_time] = wind_temp  # добавление в словарь температуры и ветра по часам
                            dict_predicat[text_data] = dict_param    # в словарь по дате данные по часам из dict_param
                    else: pass
                else: pass

        return [wheather_now, dict_predicat, len(dict_predicat)]
    except:
        return ["error"]

                #     if i == 0:
                #         # погода на сейчас
                #         data_start = datetime.datetime.strftime(dt_obj, '%Y-%m-%d')
                #         param_st = f"{param}Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                #         dict_param[text_time] = param_st
                #         dict_predicat[text_data] = dict_param
                #     else:
                #         if data_start == data_next:
                #             # запись в словарь прогноза погоды на 6-12-18 часов
                #             if int_Hours == 6 or int_Hours == 12:
                #                 param_12 = f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                #                 dict_param[text_time] = param
                #                 dict_predicat[text_data] = dict_param
                #             elif int_Hours == 18:
                #                 if len(param_12) == 0:
                #                     param_18 = f"{param}Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                #                     dict_param[text_time] = param_18
                #                     dict_predicat[text_data] = dict_param
                #                 else:
                #                     dict_param[text_time] = f'{param}{param_12}'
                #                     dict_predicat[text_data] = dict_param
                #             else:
                #                 pass
                # else:
                #     data_start = data_next
                #     dict_param = {}
                #
                #     if int_Hours == 6 or int_Hours == 12:
                #         param_12 = f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                #         dict_param[text_time] = param
                #         dict_predicat[text_data] = dict_param
                #     elif int_Hours == 18:
                #         if len(param_12) == 0:
                #             param_18 = f"{param}Влажность: {humidity}%\nДавление: {round(pressure / 1.333, 1)} мм.рт.ст\nВетер м/с: {wind}\n"
                #             dict_param[text_time] = param_18
                #             dict_predicat[text_data] = dict_param
                #         else:
                #             dict_param[text_time] = f'{param}{param_12}'
                #             dict_predicat[text_data] = dict_param


# ⤵️↔️⬆️⬇️🔼🔼🔽⏸️🟢🔴🟠⤴️
# 💸💰⬆️⬇️🔻


# = = = Команды для управления приложением
# ----- Курс валюты из списка list_curr
@bot.message_handler(commands=[x for x in dict_curr().keys()])
def all_curr(message):
    user_id = str(message.from_user.id)
    user_marker[user_id] = 1
    #  удаление слеш "\" из команды валюты \PLN
    word = message.text.replace("/", "")

    buttons = [
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, full_curr(word), reply_markup=keyboard)

# ----- Прогноз погоды /predict
@bot.message_handler(commands=['Прогноз', 'прогноз', 'ПРОГНОЗ', 'predict', 'Predict', 'PREDICT'])
def predict(message):
    user_id = str(message.from_user.id)
    user_marker[user_id] = 2
    predict_marker[user_id] = 1

    buttons = [
        types.InlineKeyboardButton('Отмена', callback_data='cancel'),
        types.InlineKeyboardButton('Курс валют', callback_data='list'),
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, "🔮 Напиши название города, и я покажу прогноз погоды на ближайшие дни", reply_markup=keyboard)

# -----  Справка
@bot.message_handler(
    commands=["Справка", "СПРАВКА", "справка", "help", "Help", "HELP", "hElp", "heLp", "helP", "HElp", "HElP", "HELp",
              "hELp", "hELP", "heLp", "heLP", "?", "start", "START", "Start"])
def help(message):
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Курс валют', callback_data='list'),
        types.InlineKeyboardButton('Погода', callback_data='weather')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, HELP, reply_markup=keyboard)

# ----- Меню
@bot.message_handler(commands=["menu", "MENU", "Menu", "меню", "Меню", "МЕНЮ","мЕНЮ","меНЮ","менЮ"])
def menu(message):
    buttons = [
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Курс валют', callback_data='list'),
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, MENU, reply_markup=keyboard)

# ----- Инфо - описание команд и кнопок
@bot.message_handler(commands=["info", "INFO", "Info", "iNfo", "список", "СПИСОК","Список"])
def info(message):
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Курс валют', callback_data='list'),
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, INFO, reply_markup=keyboard)

# ------ Курс USD и EUR евро €, рубль ₽ $
@bot.message_handler(commands=["usd", "USD", "Usd", "Eur", "eur", "EUR"])
def usdeur(message):
    # valute = dict_curr()  # запрос словаря из функции
    # text = f'Курсы валют на сегодня:\n'
    #
    # # $ USD разность курса сегодня - вчера
    # delta_usd = round(float(valute["USD"][1]) - float(valute["USD"][2]), 2)
    # if delta_usd > 0:
    #     text_usd = f'USD {valute["USD"][1]} ₽ за {valute["USD"][3]} $ (+{delta_usd}) 🟢 🔼\n'
    # elif delta_usd == 0:
    #     text_usd = f'USD {valute["USD"][1]} ₽ за {valute["USD"][3]} $ ({delta_usd}) 🟠 ⏸️\n'
    # else:
    #     text_usd = f'USD {valute["USD"][1]} ₽ за {valute["USD"][3]} $ (-{abs(delta_usd)}) 🔴 ️🔽\n'
    #
    # # € EUR разность курса сегодня - вчера
    # delta_eur = round(float(valute["EUR"][1]) - float(valute["EUR"][2]), 2)
    # if delta_eur > 0:
    #     text_eur = f'EUR {valute["EUR"][1]} ₽ за {valute["EUR"][3]} € (+{delta_eur}) 🟢 🔼\n'
    # elif delta_usd == 0:
    #     text_eur = f'EUR {valute["EUR"][1]} ₽ за {valute["EUR"][3]} € ({delta_eur}) 🟠 ⏸️\n'
    # else:
    #     text_eur = f'EUR {valute["EUR"][1]} ₽ за {valute["EUR"][3]} € (-{abs(delta_eur)}) 🔴 ️🔽\n'

    user_id = str(message.from_user.id)
    user_marker[user_id] = 1

    buttons = [
        types.InlineKeyboardButton('Список валют', callback_data='list'),
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, usd_eur(), reply_markup=keyboard)

# ------ Список всех валют
@bot.message_handler(commands=["list", "List", "LIST", "Список", "список", "СПИСОК"])
def valute(message):
    user_id = str(message.from_user.id)
    user_marker[user_id] = 1

    buttons = [
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'🔖 Список доступных валют:\n{list_curr()}', reply_markup=keyboard)

# ----- Конвертер валют
@bot.message_handler(commands=["Multy","multy", "MULTY", "Мульти", "мульти", "МУЛЬТИ"])
def multy(message):
    user_id = str(message.from_user.id)
    user_marker[user_id] = 1

    text = '♻️ Конвертер валют:\nВведите наименование двух валют для сравнения через разделитель' \
           '(тире, пробел, точка)\n(Пример: usd-eur, AUD . NOK, Czk Zar)'
    buttons = [
        types.InlineKeyboardButton('Список валют', callback_data='list'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Описание команд', callback_data='info')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

# ----- Погода
@bot.message_handler(commands=['Погода', 'ПОГОДА', 'погода', 'Weather', 'weather','WEATHER'])
def weather_one(message):
    user_id = str(message.from_user.id)
    user_marker[user_id] = 2
    predict_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Прогноз погоды', callback_data='predict'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Курс валют', callback_data='list'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, "🔮 Напиши название города, и я покажу какая там сейчас погода", reply_markup=keyboard)


# ----- Отмена всех команд /end
@bot.message_handler(commands=["Отмена", "ОТМЕНА", "отмена", "end", "END", "End", "/"])
def end(message):

    user_id = str(message.from_user.id)
    user_marker[user_id] = 2
    predict_marker[user_id] = 0

    buttons = [
        types.InlineKeyboardButton('Погода', callback_data='weather'),
        types.InlineKeyboardButton('Курс валют', callback_data='list'),
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

# = = = Реагирование на кнопки = = =
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    user_id = str(call.from_user.id)

    if call.message:
        # ----- Выполнение кнопки "Меню"
        if call.data == "menu":
            buttons = [
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Курс валют', callback_data='list'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=MENU, reply_markup=keyboard)

        # ----- Кнопка Справка
        elif call.data == "help":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Курс валют', callback_data='list'),
                types.InlineKeyboardButton('Погода', callback_data='weather')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            # bot.send_message(call.message.chat.id, HELP, reply_markup=keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=HELP, reply_markup=keyboard)

        # -----Выполнение Кнопка "Отмена" - завершение всех команд
        elif call.data == "cancel":

            user_marker[user_id] = 1
            predict_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Курс валют', callback_data='list'),
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

        # ----- Выполнение кнопка "Info" Описание команд
        elif call.data == 'info':
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Курс валют', callback_data='list'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=INFO, reply_markup=keyboard)

        # ----- Кнопка курс валют USD / EUR
        elif call.data == "UsdEur":

            user_marker[user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id,  usd_eur(), reply_markup=keyboard)

        # ----- Кнопка конвертер валют jpy-usd
        elif call.data == "multy":

            user_marker[user_id] = 1

            text = '♻️ Конвертер валют:\nВведите наименование двух валют для сравнения через разделитель' \
                   '(тире, пробел, точка)\n(Пример: usd-eur, AUD . NOK, Czk Zar)'
            buttons = [
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, text, reply_markup=keyboard)

        # ----- Кнопка Список валют
        elif call.data == 'list':

            user_marker[user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, f'🔖 Список доступных валют:\n{list_curr()}', reply_markup=keyboard)

        # ----- Кнопка Погода
        elif call.data == 'weather':
            user_marker[user_id] = 2
            predict_marker[user_id] = 0

            buttons = [
                types.InlineKeyboardButton('Прогноз погоды', callback_data='predict'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Курс валют', callback_data='list'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, "🔮 Напиши название города, и я покажу какая там сейчас погода",
                             reply_markup=keyboard)

        # ----- Кнопка Прогноз Погоды на 5 дней
        elif call.data == 'predict':
            user_marker[user_id] = 2
            predict_marker[user_id] = 1

            buttons = [
                types.InlineKeyboardButton('Отмена', callback_data='cancel'),
                types.InlineKeyboardButton('Курс валют', callback_data='list'),
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, "🔮 Напиши название города, и я покажу прогноз погоды на ближайшие дни",
                             reply_markup=keyboard)


        bot.answer_callback_query(callback_query_id=call.id)  # обработка данного callback-запроса завершена.


# = = = Выполнение сценариев = = =
@bot.message_handler(content_types=["text"])
def echo(message):

    user_id = str(message.from_user.id)
    user_marker.setdefault(user_id, 2)
    predict_marker.setdefault(user_id, 0)

    # word = message.text.upper().replace(" ", "")
    # word = message.text.upper().strip()

    word = message.text.strip()

    # ---Сценарий - завершение всех команд
    if word == "/":

        user_marker[user_id] = 2
        predict_marker[user_id] = 0

        buttons = [
            types.InlineKeyboardButton('Погода', callback_data='weather'),
            types.InlineKeyboardButton('Курс валют', callback_data='list'),
            types.InlineKeyboardButton('Конвертер', callback_data='multy'),
            types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

    # ----- сценарий Погода
    elif user_marker[user_id] == 2:

        city_name = word.lower().replace(" ", "")

        # запрос к серверу погоды
        data =  api_weather(city_name)



        # bot.send_message(message.chat.id, f'вывод {data}')
        # response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={Pogoda_TOKEN}&lang={lang}&q=уфа")
        # data = response.json()
        #
        # todos = data.json()  # данные в формате JSON
        # if len(str(todos)) > 4096:
        #         for x in range(0, len(str(todos)), 4096):
        #             bot.send_message(message.chat.id, str(todos)[x:x + 4096])
        # else:
        #         bot.send_message(message.chat.id, str(todos))

        #   {'location':
        #      {'name': 'Уфа', 'region': 'Bashkortostan', 'country': 'Россия',
        #       'lat': 54.78, 'lon': 56.04, 'tz_id': 'Asia/Yekaterinburg', 'localtime_epoch': 1703533206,
        #      'localtime': '2023-12-26 0:40'},
        #   'current':
        #       {'last_updated_epoch': 1703532600, 'last_updated': '2023-12-26 00:30',
        #       'temp_c': -2.0, 'is_day': 0,
        #   'condition':
        #           {'text': 'Небольшой снег', 'icon': '//cdn.weatherapi.com/weather/64x64/night/326.png', 'code': 1213},
        #   'wind_kph': 19.1,
        #   'wind_degree': 190,
        #   'wind_dir': 'S',
        #   'pressure_mb': 994.0,
        #   'precip_mm': 0.0,
        #   'humidity': 80
        #   cloud': 100,
        #   'feelslike_c': -5.1,
        #   'vis_km': 10.0}
        #   }

        buttons = [
            types.InlineKeyboardButton('Погода', callback_data='weather'),
            types.InlineKeyboardButton('Курс валют', callback_data='list'),
            types.InlineKeyboardButton('Отмена', callback_data='cancel'),
            types.InlineKeyboardButton('Описание команд', callback_data='info')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        if data == "error":
            bot.send_message(message.chat.id, f'❌ Cервис недоступен.\nПовторите запрос позже...⏳', reply_markup=keyboard)

        elif data.get("error"):
            bot.send_message(message.chat.id, f'❌ Неизвестная команда.\nПроверьте название города',
                             reply_markup=keyboard)

        elif data["location"].get("name") is None:
            bot.send_message(message.chat.id, f'❌ Неизвестная команда.\nПроверьте название города', reply_markup=keyboard)

        else:
        #  прогноз на несколько дат
            if predict_marker[user_id] == 1:

                log_data = api_predicat(city_name)

                if log_data[0] == "error":
                    bot.send_message(message.chat.id, f'❌ Возмодно сервис недоступен.\n'\
                            f'Проверьте название города и повторите запрос позже...⏳',
                            reply_markup=keyboard)
                else:
                    text = ""
                    for dt, line in log_data[1].items():
                        text = f'{text}{dt}\n'
                        for hours, parm in line.items():
                            text = f'{text}{hours}: {parm}'
                        text = f'{text}\n'

                    buttons = [
                        types.InlineKeyboardButton('Погода сейчас', callback_data='weather'),
                        types.InlineKeyboardButton('Курс валют', callback_data='list'),
                        types.InlineKeyboardButton('Отмена', callback_data='cancel'),
                        types.InlineKeyboardButton('Описание команд', callback_data='info')
                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(*buttons)

                    # возможно вывод прогноза на кол-во дней по запросу
                    bot.send_message(message.chat.id, f'{log_data[0]}\n'\
                                    f'\nПрогноз погоды в городе {city_name.capitalize()} на {log_data[2]} '\
                                    f'{"день" if log_data[2] == 1 else ("дня" if log_data[2] < 5 else "дней")}:\n{text}'\
                                    , reply_markup=keyboard)
        #  погода на сегодня
            elif predict_marker[user_id] == 0:

                text = weather_loc( data )
                buttons = [
                    types.InlineKeyboardButton('Прогноз погоды', callback_data='predict'),
                    types.InlineKeyboardButton('Описание команд', callback_data='info'),
                    types.InlineKeyboardButton('Курс валют', callback_data='list'),
                    types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                bot.send_message(message.chat.id, text, reply_markup=keyboard)

    # ---Сценарий курс валют
    elif user_marker[user_id] == 1:

        curr_rate = word.upper()
        valute = dict_curr()  # запрос словаря из функции

        # --- Конвертер валют (если больше 3 символов в запросе)  🚫♻️
        if len(curr_rate) > 3 and ("-" in curr_rate or "." in curr_rate or " " in curr_rate):
            delimiters = r"[ -.]+"
            text_ = re.split(delimiters,  curr_rate)

            valute_1 = text_[0].upper().strip()
            valute_2 = text_[1].upper().strip()

            buttons = [
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            if valute.get(valute_1) is not None and valute.get(valute_2) is not None:

                # значок валюты из словаря
                if dict_symbol.get(valute_1) is None:
                    sym_1 = ""
                else:
                    sym_1 = dict_symbol[valute_1]

                if dict_symbol.get(valute_2) is None:
                    sym_2 = ""
                else:
                    sym_2 = dict_symbol[valute_2]

                text_0 = f'💸 Конвертер валют:\n {sym_1} {valute[valute_1][0]} - {sym_2} {valute[valute_2][0]}\n'

                convert = round( float( valute[valute_1][1] ) * float( valute[valute_2][3] ) / float( valute[valute_2][1] ), 2)

                text_1 = f'{valute[valute_1][3]} {sym_1} ({valute_1}) = {convert} {sym_2} ({valute_2})'

                bot.send_message(message.chat.id, text_0 + text_1, reply_markup=keyboard)
            else:

                bot.send_message(message.chat.id, f'🚫 Названия валют не найдено.\n'
                        f'Проверьте правильность написания, и наличие валюты в списке /list', reply_markup=keyboard)

        #- --- курс одной валюты, если название валюты есть в словаре:  { EUR :[Евро, 79.4966, 79.6765, 1,]}
        #                                                           { Word:[ 0(имя)  1(сегодня) 2(вчера) 3(номинал)]}
        elif valute.get(word) is not None:

            buttons = [
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.send_message(message.chat.id, full_curr(word), reply_markup=keyboard)

        #  команда не распознана
        else:
            buttons = [
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur'),
                types.InlineKeyboardButton('Погода', callback_data='weather'),
                types.InlineKeyboardButton('Описание команд', callback_data='info')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, f'🚫 Названия валют не найдено.\n'
                                              f'Проверьте правильность написания, и наличие валюты в списке /list',
                             reply_markup=keyboard)

    # --- Сценарий команды нет в списке
    else:
        _text = ('❌ Неизвестная команда.')
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Описание команд', callback_data='info'),
            types.InlineKeyboardButton('Погода', callback_data='weather'),
            types.InlineKeyboardButton('Курс валюты', callback_data='curr')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)

        if user_marker[user_id] == 2:
            bot.send_message(message.chat.id, f'{_text}.\nПроверьте название города', reply_markup=keyboard)
        else:

            bot.send_message(message.chat.id, _text, reply_markup=keyboard)


# =========================================#
# Отправляем длинное сообщение по частям
# todos = log_qyery.json()['Valute']   # данные в формате JSON
#     if len(str(todos)) > 4096:
#         for x in range(0, len(str(todos)), 4096):
#             bot.send_message(message.chat.id, str(todos)[x:x + 4096])
#     else:
#         bot.send_message(message.chat.id, str(todos))
# -=================


# keep_alive()  #запускаем flask-сервер
# while True:
#   try:
#     bot.polling(none_stop=True)
#   except Exception as _ex:
#     print(_ex)
#     time.sleep(15)

# bot.polling(none_stop=True)


while True:
  try:
    bot.polling(none_stop=True)
  except Exception as _ex:
    # print(_ex)
    time.sleep(15)