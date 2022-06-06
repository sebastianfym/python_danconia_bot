import telebot
import requests
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from config_data.config import config
from markup.markup import markup

bot = telebot.TeleBot(config['token'])

unique_dict_result = dict()
user_dict_results = dict()


# @bot.message_handler(commands=['calendar'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


def low_func_accomplishemnt(message, user, control):
    if user.command is not dict():
        user.command = dict()

    user.command['/lowprice'] = dict()

    if control.city_name is True:
        if message.text not in user.command['/lowprice']:
            user.command['/lowprice'][f"{message.text}"] = dict()
        bot.city_name = message.text
        bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
        control.count_hostels = True
        control.city_name = False

    elif control.count_hostels is True:
        if int(message.text) <= 0:
            bot.send_message(message.chat.id, "Введите корректное число.")
            control.count_hostels = False
            control.city_name = True
            bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
            return

        bot.count_hotels = message.text
        bot.send_message(message.chat.id,
                         f"Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                         "то введите желаемое количество фотографий\n", reply_markup=markup)

        control.count_hostels = False
        control.check_low = False
        control.first_func = True


def max_func_accomplishment(message, user, control):
    if control.city_name is True:
        if user.command is not dict():
            user.command = dict()

        user.command['/highprice'] = dict()
        if message.text not in user.command['/highprice']:
            user.command['/highprice'][f"{message.text}"] = dict()
        bot.city_name = message.text
        bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
        control.count_hostels = True
        control.city_name = False

    elif control.count_hostels is True:
        if int(message.text) <= 0:
            bot.send_message(message.chat.id, "Введите корректное число.")
            control.count_hostels = False
            control.city_name = True
            bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
            return

        bot.count_hotels = message.text
        bot.send_message(message.chat.id,
                         "Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                         "то введите желаемое количество фотографий", reply_markup=markup)

        control.count_hostels = False
        control.check_max = False
        control.second_func = True


def best_deal_func_accomplishment(message, user, control):
    if control.city_name is True:
        if user.command is not dict():
            user.command = dict()

        user.command['/bestdeal'] = dict()
        if message.text not in user.command['/bestdeal']:
            user.command['/bestdeal'][f"{message.text}"] = dict()

        bot.city_name = message.text
        bot.send_message(message.chat.id, f'Введите минимальную цену: ')
        control.min_price = True
        control.city_name = False

    elif control.min_price is True:
        min_price = message.text
        if int(message.text) <= 0:
            min_price = abs(int(message.text))
        bot.min_price = min_price

        bot.send_message(message.chat.id, f'Введите максимальную цену: ')
        control.min_price = False
        control.max_price = True

    elif control.max_price is True:
        max_price = message.text
        if int(message.text) <= 0:
            max_price = abs(int(message.text))
        bot.max_price = max_price

        bot.send_message(message.chat.id, f'Введите допустимое расстояние к центру: ')
        control.max_price = False
        control.length_to_center = True

    elif control.length_to_center is True:
        length_to_center = message.text
        if int(message.text) <= 0:
            length_to_center = abs(int(message.text))
        bot.length_to_center = length_to_center

        bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
        control.length_to_center = False
        control.count_hostels = True

    elif control.count_hostels is True:
        count_hostels = message.text
        if int(message.text) <= 0:
            count_hostels = abs(int(message.text))

        bot.count_hotels = count_hostels
        bot.send_message(message.chat.id,
                         "Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                         "то введите желаемое количество фотографий", reply_markup=markup)

        control.count_hostels = False
        control.check_best_deal = False
        control.third_func = True


def request_to_api(request_type, url, headers, querystring):
    try:
        response = requests.request(request_type, url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
    except TimeoutError:
        return TimeoutError


