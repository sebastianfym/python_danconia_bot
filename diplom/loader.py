from dotenv import load_dotenv
from pathlib import Path
import os
import telebot
from telebot import types


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_yes = types.KeyboardButton("Да")
button_no = types.KeyboardButton("Нет")

markup.add(button_yes, button_no)


load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
secret_key = os.getenv("key")
secret_key_api = os.getenv('key_api')
secret_key_pic = os.getenv('key_pic')

config = {
    "name": "DanconiaTravelBot",
    "token": secret_key
}


bot = telebot.TeleBot(config['token'])

unique_dict_result = dict()
user_dict_results = dict()


def low_func_accomplishemnt(message, user, control):
    # user = Users.get_user(message.chat.id)

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
                         "то введите желаемое количество фотографий\n", reply_markup=markup)#loader.markup)

        control.count_hostels = False
        control.check_low = False
        control.first_func = True


def max_func_accomplishment(message, user, control):
    if control.city_name is True:
        # user = Users.get_user(message.chat.id)
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
                         "то введите желаемое количество фотографий", reply_markup=markup)#loader.markup)

        control.count_hostels = False
        control.check_max = False
        control.second_func = True

def best_deal_func_accomplishment(message, user, control):
    if control.city_name is True:

        # user = Users.get_user(message.chat.id)
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
        if int(message.text) <= 0:
            handlers.check_property(message, control.min_price, control.check_best_deal)

        bot.min_price = message.text
        bot.send_message(message.chat.id, f'Введите максимальную цену: ')
        control.min_price = False
        control.max_price = True

    elif control.max_price is True:
        if int(message.text) <= 0:
            handlers.check_property(message, control.max_price, control.min_price)
        bot.max_price = message.text
        bot.send_message(message.chat.id, f'Введите допустимое расстояние к центру: ')
        control.max_price = False
        control.length_to_center = True

    elif control.length_to_center is True:
        if int(message.text) <= 0:
            handlers.check_property(message, control.length_to_center, control.max_price)

        bot.length_to_center = message.text
        bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
        control.length_to_center = False
        control.count_hostels = True

    elif control.count_hostels is True:
        bot.count_hotels = message.text
        bot.send_message(message.chat.id,
                         "Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                         "то введите желаемое количество фотографий", reply_markup=markup)#loader.markup)

        control.count_hostels = False
        control.check_best_deal = False
        control.third_func = True