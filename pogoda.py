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

#  смайл погоды
code_to_smile = {
     "Clear": "Ясно \U00002600",
     "Clouds": "Облачно \U00002601",
     "Rain": "Дождь \U00002614",
     "Drizzle": "Дождь \U00002614",
     "Thunderstorm": "Гроза \U000026A1",
     "Snow": "Снег \U0001F328",
     "Mist": "Туман \U0001F32B"
}

# get(f"http://api.openweathermap.org/data/2.5/weather?q=москва&lang=ru&units=metric&appid={Pogoda_TOKEN}")


@bot.message_handler(commands=['st'])
def start(message):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name_1}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")

    bot.send_message(message.chat.id, f"http://api.openweathermap.org/data/2.5/weather?q={city_name_1}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")
    data = response.json()

    # bot.send_message(message.chat.id, response)
    bot.send_message(message.chat.id, f'Дата\n{data}')


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
    city_name = message.text.lower().replace(" ","")

    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang={lang}&units={units}&appid={Pogoda_TOKEN}")

        data = response.json()

        #  парсим JSON запрос погоды
        city = data["name"]          # город
        temp_avg = float(data["main"]["temp"])          # температура средняя
        temp_min = float(data["main"]["temp_min"])      # температура min
        temp_max = float(data["main"]["temp_max"])      # температура max
        temp_feels = float(data["main"]["feels_like"])  # температура по ощущениям
        humidity = data["main"]["humidity"]             # влажность
        pressure = float(data["main"]["pressure"])      # давление гектопаскаль / 1,333
        wind = data["wind"]["speed"]                   # ветер скорость

        cur_weather = f'{round(temp_min,1)}°C - {round(temp_max,1)}°C, ощущается как {round(temp_feels,1)}°C'  # температура для вывода

        # получаем время рассвета и преобразуем его в читабельный формат
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M')
        # bot.send_message(message.chat.id, sunrise_timestamp.strftime('%H:%M') )

        # то же самое проделаем со временем заката
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M')
        # продолжительность дня
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                            datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # получаем значение погоды
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            # если эмодзи для погоды нет, выводим другое сообщение
            wd = "Давай посмотрим в окно, я не понимаю, что там за погода..."

        bot.send_message(message.chat.id, f"Погода на {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}:\n"
              f"В городе: {city}\nТемпература: {cur_weather}\n{wd}\n"
              f"Влажность: {humidity}%\nДавление: {round(pressure / 1.333 , 1)} мм.рт.ст\nВетер: {wind} м/с \n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
             )
    except:
        # buttons = [
        #     types.InlineKeyboardButton('Меню', callback_data='menu'),
        #     types.InlineKeyboardButton('Новый список', callback_data='add'),
        # ]
        # keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        # keyboard.add(*buttons)
        # bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)
        bot.send_message(message.chat.id, f'❌ Неизвестная команда.\nПроверьте название города')


while True:
  try:
    bot.polling(none_stop=True)
  except Exception as _ex:
    # print(_ex)
    time.sleep(15)