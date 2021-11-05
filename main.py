import handlers
import loader
from handlers import ControlBot
from telebot import types

bot = loader.bot
control = ControlBot()

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_yes = types.KeyboardButton("Да")
button_no = types.KeyboardButton("Нет")

markup.add(button_yes, button_no)


@bot.message_handler(func=lambda message: message.text.lower() == "/help" or message.text.lower() == "привет"
                                          or message.text.lower() == "/start")
def help(message):
    bot.send_message(message.chat.id, "Рад Вам помочь! Вот перечень моих "
                                      "команд:\n/lowprice\n/highprice\n/bestdeal\n/my_request")
    handlers.description_commands(message)


@bot.message_handler(func=lambda message: message.text.lower() == "/lowprice")
def low_price(message):
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
    control.check_low = True
    control.city_name = True


@bot.message_handler(func=lambda message: message.text.lower() == "/highprice")
def high_price(message):
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
    control.check_max = True
    control.city_name = True


@bot.message_handler(func=lambda message: message.text.lower() == "/bestdeal")
def best_deal(message):
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
    control.check_best_deal = True
    control.city_name = True


@bot.message_handler(func=lambda message: message.text.lower() == "/my_request")
def id_user(message):
    handlers.watch_result(message)


@bot.message_handler(func=lambda message: message.text.lower() == "да")
def print_user_picture(message):
    bot.send_message(message.chat.id, "Введите желаемое количество фотографий: ")
    control.check_picture = True


@bot.message_handler(func=lambda message: message.text.lower() == "нет")
def continue_work(message):
    bot.send_message(message.chat.id, "Как пожелаете.")
    if control.first_func is True:
        handlers.min_price_execute(message, bot.city_name, bot.count_hotels)
        control.first_func = False

    elif control.second_func is True:
        handlers.max_price_execute(message, bot.city_name, bot.count_hotels)
        control.second_func = False

    elif control.third_func is True:
        handlers.best_price_execute(message, bot.city_name, bot.min_price, bot.max_price, bot.length_to_center,
                                    bot.count_hotels)
        control.third_func = False


@bot.message_handler(content_types=['text', 'number'])
def performance_func(message):
    if control.check_low is True:
        if control.city_name is True:
            bot.city_name = message.text

            bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
            control.count_hostels = True
            control.city_name = False

        elif control.count_hostels is True:
            bot.count_hotels = message.text
            bot.send_message(message.chat.id,
                             "Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                             "то введите желаемое количество фотографий", reply_markup=markup)

            control.count_hostels = False
            control.check_low = False
            control.first_func = True

    elif control.check_max is True:
        if control.city_name is True:
            bot.city_name = message.text

            bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
            control.count_hostels = True
            control.city_name = False

        elif control.count_hostels is True:
            bot.count_hotels = message.text
            bot.send_message(message.chat.id,
                             "Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                             "то введите желаемое количество фотографий", reply_markup=markup)

            control.count_hostels = False
            control.check_max = False
            control.second_func = True

    elif control.check_best_deal is True:
        if control.city_name is True:
            bot.city_name = message.text
            bot.send_message(message.chat.id, f'Введите минимальную цену: ')
            control.min_price = True
            control.city_name = False

        elif control.min_price is True:
            bot.min_price = message.text
            bot.send_message(message.chat.id, f'Введите максимальную цену: ')
            control.min_price = False
            control.max_price = True

        elif control.max_price is True:
            bot.max_price = message.text
            bot.send_message(message.chat.id, f'Введите допустимое расстояние к центру: ')
            control.max_price = False
            control.length_to_center = True

        elif control.length_to_center is True:
            bot.length_to_center = message.text
            bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
            control.length_to_center = False
            control.count_hostels = True

        elif control.count_hostels is True:
            bot.count_hotels = message.text
            bot.send_message(message.chat.id,
                             "Хотите ли вы увидеть фотографии отелей?\n\"Да/Нет\"\nЕсли Ваш выбор \'Да\',"
                             "то введите желаемое количество фотографий", reply_markup=markup)

            control.count_hostels = False
            control.check_best_deal = False
            control.third_func = True

    elif control.check_picture is True:
        handlers.send_picture(message, int(message.text.split(" ")[0]))
        handlers.min_price_execute(message, bot.city_name, bot.count_hotels)


bot.polling(none_stop=True, interval=0)
