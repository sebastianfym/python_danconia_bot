import handlers
import loader
from handlers import ControlBot, Users
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = loader.bot
control = ControlBot()


@bot.message_handler(commands=['calendar'])
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


@bot.message_handler(func=lambda message: message.text.lower() == "/help" or message.text.lower() == "привет"
                                          or message.text.lower() == "/start")
def help(message):
    bot.send_message(message.chat.id, "Рад Вам помочь! Вот перечень моих "
                                      "команд:\n/lowprice\n/highprice\n/bestdeal\n/my_request")
    handlers.description_commands(message)
    user = Users.get_user(message.from_user.id)
    user.command = dict()


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
        handlers.min_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message))
        control.first_func = False

    elif control.second_func is True:
        handlers.max_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message))
        control.second_func = False

    elif control.third_func is True:
        handlers.best_price_execute(message, bot.city_name, bot.min_price, bot.max_price, bot.length_to_center,
                                    bot.count_hotels, start(message), start(message))
        control.third_func = False


@bot.message_handler(content_types=['text', 'number'])
def performance_func(message):
    # stm.cycle()
    if control.check_low is True:
        user = Users.get_user(message.chat.id)

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
                             "то введите желаемое количество фотографий\n", reply_markup=loader.markup)

            control.count_hostels = False
            control.check_low = False
            control.first_func = True

    elif control.check_max is True:

        if control.city_name is True:
            user = Users.get_user(message.chat.id)
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
                             "то введите желаемое количество фотографий", reply_markup=loader.markup)

            control.count_hostels = False
            control.check_max = False
            control.second_func = True

    elif control.check_best_deal is True:
        if control.city_name is True:

            user = Users.get_user(message.chat.id)
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
                             "то введите желаемое количество фотографий", reply_markup=loader.markup)

            control.count_hostels = False
            control.check_best_deal = False
            control.third_func = True

    elif control.check_picture is True:
        handlers.send_picture(message, int(message.text.split(" ")[0]))
        handlers.min_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(
            message))


"""
# Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
# - interval: int (default 0) - The interval between polling requests
# - timeout: integer (default 20) - Timeout in seconds for long polling.
# - allowed_updates: List of Strings (default None) - List of update types to request
"""
bot.infinity_polling(interval=0, timeout=10) #TODO это решает вопрос с timeout?

