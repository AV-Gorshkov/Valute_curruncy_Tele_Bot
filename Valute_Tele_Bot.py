
import requests
from setting import TG_TOKEN

import telebot
from telebot import types
from datetime import datetime
from telebot import TeleBot
import time

import json
# import random

# # === обращение к БД Replit, поддержка работы 24/7
# import os
# from background import keep_alive  # #импорт функции для поддержки работоспособности
#
# from replit import db
# import base
#
# import pip
# pip.main(['install', 'pytelegrambotapi'])
#

# my_secret = os.environ['token']
# -----------------------------

bot = telebot.TeleBot(TG_TOKEN, skip_pending=True)

# 💹💰💴💵💶💷💸💲
# 📈📉📊

HELP = """
Приветствую!✌️ Я Чат-Бот! 
📊 Подскажу тебе курс самых популярных валют на текущую дату по курсу ЦБ РФ.
Нажми на кнопку ниже, что бы узнать функционал доступных команд и их описание:
©️
"""

#  ---------------- описание вызываемых команд
MENU = """✏️ Команды доступные в приложении
/info - (Info, Описание) - описание действия команд и кнопок приложения.
/help - (Нelp, Справка, ? ) - вызов справки о программе, знакомство с приложением.
/list - (List, Список) - список валют, доступных для просмотра.
/end - (/End, /Отмена, /) -  отмена всех команд.
/usd - (/Usd, /Eur) - курс Доллара, Евро и изменение с предыдущем значением. 
/multy - (Multy, Мульти) - конвертер валют.
/menu - (Menu, Меню) - Меню - список доступных команд приложения.
"""

#
INFO = """ Описание взаимодействия с приложением:
💵 Все команды из списка в "Menu" вызываются через слэш "/" 
(Пример: /list, /usd, /Menu)
💷 Информация по курсу для одной валюты - ввести ID валюты из списка валют
(Пример: eur, NZD, Usd)
💶 Конвертер валют - информация по курсу между двумя выбранными валютами 
(Пример: usd-eur, AUD-NOK, Czk - Zar)
"""

#  Блок переменных
dict_currency = {}   # словарь валют
dict_symbol = {"AUD":"$", "AZN":"₼", "GBP":"£", "AMD":"Դ", "BYN":"Br", "BGN":"лв", "BRL":"R$", "HUF":"Ft", "VND":"₫", "HKD":"$",
           "GEL":"₾", "DKK":"kr", "AED":"Dh", "USD":"$", "EUR":"€", "EGP":".ج.م •", "INR":"र", "IDR":"Rp", "KZT":"〒",
           "CAD":"$", "QAR":"ر.ع.", "KGS":"с", "CNY":"元", "MDL":"L", "NZD":"$", "NOK":"kr", "PLN":"zł", "RON":"L",
           "XDR":" СДР", "SGD":"$", "TJS":"с.", "THB":"฿", "TRY":"TL", "TMT":"m", "UZS":"сўм", "UAH":"₴", "CZK":"Kč",
           "SEK":"kr", "CHF":"₣", "RSD":"RSD", "ZAR":"R", "KRW":"₩", "JPY":"¥", "RUR": "₽"}  # словарь знаков валюты

# = = = общие функции
# ---запрос к серверу валют
def dict_curr():
    # запрос к сайту
    log_query = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
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
            text = f'{text}{key} - {val[0]}\n'
        else:
            symbol = dict_symbol[key]
            text = f'{text}{key} - {val[0]} ({symbol})\n'
    return text

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


# ⤵️↔️⬆️⬇️🔼🔼🔽⏸️🟢🔴🟠⤴️
# 💸💰⬆️⬇️🔻

# = = = Команды для управления приложением
# -----  Справка
@bot.message_handler(
    commands=["Справка", "СПРАВКА", "справка", "help", "Help", "HELP", "hElp", "heLp", "helP", "HElp", "HElP", "HELp",
              "hELp", "hELP", "heLp", "heLP", "?", "start", "START", "Start"])
def help(message):
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Список валют', callback_data='list_curr'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, HELP, reply_markup=keyboard)

# ----- Меню
@bot.message_handler(commands=["menu", "MENU", "Menu", "меню", "Меню", "МЕНЮ","мЕНЮ","меНЮ","менЮ"])
def menu(message):
    buttons = [
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Список валют', callback_data='list'),
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
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
        types.InlineKeyboardButton('Список валют', callback_data='list'),
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
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

    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Список валют', callback_data='list'),
        types.InlineKeyboardButton('Конвертер', callback_data='multy')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, usd_eur(), reply_markup=keyboard)

# ------ Список всех валют
@bot.message_handler(commands=["list", "List", "LIST", "Список", "список", "СПИСОК"])
def valute(message):
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Конвертер', callback_data='multy'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f'🔖 Список доступных валют:\n{list_curr()}', reply_markup=keyboard)

# ----- Конвертер валют
@bot.message_handler(commands=["Multy","multy", "MULTY", "Мульти", "мульти", "МУЛЬТИ"])
def multy(message):

    text = '♻️ Конвертер валют:\nВведите наименование двух валют для сравнения через тире\n' \
           '(Пример: usd-eur, AUD-NOK, Czk - Zar)'
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Отмена', callback_data='cancel'),
        types.InlineKeyboardButton('Список валют', callback_data='list')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

# ----- Отмена всех команд /end
@bot.message_handler(commands=["Отмена", "ОТМЕНА", "отмена", "end", "END", "End", "/"])
def end(message):

    # обнуление команд ??????
    buttons = [
        types.InlineKeyboardButton('Меню', callback_data='menu'),
        types.InlineKeyboardButton('Описание команд', callback_data='info'),
        types.InlineKeyboardButton('Список валют', callback_data='list'),
        types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

# = = = Реагирование на кнопки = = =
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = str(call.from_user.id)
    message_id = call.message.message_id
    chat_id = call.message.chat.id


    if call.message:
        # ----- Выполнение кнопки "Отмена"
        if call.data == "menu":
            buttons = [
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
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
                types.InlineKeyboardButton('Список валют', callback_data='list_curr'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            # bot.send_message(call.message.chat.id, HELP, reply_markup=keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=HELP, reply_markup=keyboard)

        # -----Выполнение Кнопка "Отмена" - завершение всех команд
        elif call.data == "cancel":

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Новый список', callback_data='add')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)
            bot.send_message(call.message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

        # ----- Выполнение кнопка "Info" Описание команд
        elif call.data == 'info':
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
            keyboard.add(*buttons)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=INFO, reply_markup=keyboard)

        # ----- Кнопка курс валют USD / EUR
        elif call.data == "UsdEur":
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Список валют', callback_data='list'),
                types.InlineKeyboardButton('Конвертер', callback_data='multy')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id,  usd_eur(), reply_markup=keyboard)

        # ----- Кнопка курс валют USD / EUR
        elif call.data == "multy":
            text = '♻️ Конвертер валют:\nВведите наименование двух валют для сравнения через тире\n' \
                   '(Пример: usd-eur, AUD-NOK, Czk - Zar)'

            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Отмена', callback_data='cancel'),
                types.InlineKeyboardButton('Список валют', callback_data='list')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, text, reply_markup=keyboard)

        # ----- Кнопка Список валют
        elif call.data == 'list':
            buttons = [
                types.InlineKeyboardButton('Меню', callback_data='menu'),
                types.InlineKeyboardButton('Описание команд', callback_data='info'),
                types.InlineKeyboardButton('Конвертер', callback_data='multy'),
                types.InlineKeyboardButton('Курс USD/EUR', callback_data='UsdEur')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            bot.send_message(call.message.chat.id, f'🔖 Список доступных валют:\n{list_curr()}', reply_markup=keyboard)


        bot.answer_callback_query(callback_query_id=call.id)  # обработка данного callback-запроса завершена.


# = = = Выполнение сценариев = = =
@bot.message_handler(content_types=["text"])
def echo(message):

    # user_id = str(message.from_user.id)
    # user_name = str(message.from_user.username)  # Log пользователя
    # time_sms = message.date

    word = message.text.upper().replace(" ", "")
    valute = dict_curr() # запрос словаря из функции

    # ---Сценарий - завершение всех команд
    if word == "/":

        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "⛔ Выполнение команды завершено.", reply_markup=keyboard)

    # --- Конвертер валют (если больше 3 символов в запросе)  🚫♻️
    elif len(word) > 3 and "-" in word:
        text_ = word.split(maxsplit=1, sep="-")
        valute_1 = text_[0].upper()
        valute_2 = text_[1].upper()

        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Новый список', callback_data='add'),
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
            #
            # text_0 = f'Конвертер валют: {sym_1} {valute_1} - {sym_2} {valute_2}\n'
            text_0 = f'💸 Конвертер валют:\n {sym_1} {valute[valute_1][0]} - {sym_2} {valute[valute_2][0]}\n'
            convert = round( float( valute[valute_1][1] ) * float( valute[valute_2][3] ) / float( valute[valute_2][1] ), 2)

            text_1 = f'{valute[valute_1][3]} {sym_1} ({valute_1}) = {convert} {sym_2} ({valute_2})'

            bot.send_message(message.chat.id, text_0 + text_1)
        else:

            bot.send_message(message.chat.id, f'🚫 Названия валют не найдено.\n'
                    f'Проверьте правильность написания, и наличие валюты в списке /list', reply_markup=keyboard)

    #- --- курс одной валюты, если название валюты есть в словаре:  { EUR :[Евро, 79.4966, 79.6765, 1,]}
    #                                                           { Word:[ 0(имя)  1(сегодня) 2(вчера) 3(номинал)]}
    # ⤵️↔️⬆️⬇️🔼🔼🔽⏸️🟢🔴🟠⤴️
    # 💸💰⬆️⬇️🔻    ⬆️⬇️
    elif valute.get(word) is not None:

        text_0 = f'💹 Курс валюты на сегодня:\n{valute[word][0]}\n'
        # значок валюты из словаря
        if dict_symbol.get(word) is None:
            sym = ""
        else:
            sym = dict_symbol[word]

        # разность курса сегодня - вчера
        delta = round(float(valute[word][1]) - float(valute[word][2]), 2)

        if delta > 0:
            text_1 = f'₽ {valute[word][1]} за {valute[word][3]} {sym} (+{delta}) 🟢 ⬆️'
        elif delta == 0:
            text_1 = f'₽ {valute[word][1]} за {valute[word][3]} {sym}  (+{delta}) 🟠 ⏸️'
        else:
            text_1 = f'₽ {valute[word][1]} за {valute[word][3]} {sym}  (-{abs(delta)}) 🔴 ️⬇️'

        # _text = dict_curr()
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Справка', callback_data='help')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, text_0 + text_1, reply_markup=keyboard)


    # --- Сценарий команды нет в списке
    else:

        _text = ('❌ Неизвестная команда.')  # + ' \n' + 'Для вызова списка команд введите - /menu')
        buttons = [
            types.InlineKeyboardButton('Меню', callback_data='menu'),
            types.InlineKeyboardButton('Справка', callback_data='help')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура (кол-во кнопок в ряд)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, _text, reply_markup=keyboard)




#
# Отправляем длинное сообщение по частям
# todos = log_qyery.json()['Valute']   # данные в формате JSON
#     if len(str(todos)) > 4096:
#         for x in range(0, len(str(todos)), 4096):
#             bot.send_message(message.chat.id, str(todos)[x:x + 4096])
#     else:
#         bot.send_message(message.chat.id, str(todos))
# -----------------------------------

 #




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