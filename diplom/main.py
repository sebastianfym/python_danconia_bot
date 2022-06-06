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
        handlers.min_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), False, 0)
        control.first_func = False

    elif control.second_func is True:
        handlers.max_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), False, 0)
        control.second_func = False

    elif control.third_func is True:
        handlers.best_price_execute(message, bot.city_name, bot.min_price, bot.max_price, bot.length_to_center,
                                    bot.count_hotels, start(message), start(message), False, 0)
        control.third_func = False


@bot.message_handler(content_types=['text', 'number'])
def performance_func(message):
    user = Users.get_user(message.chat.id)
    if control.check_low is True:
        loader.low_func_accomplishemnt(message, user, control)

    elif control.check_max is True:
        loader.max_func_accomplishment(message, user, control)

    elif control.check_best_deal is True:
        loader.best_deal_func_accomplishment(message, user, control)

    elif control.check_picture is True:
        if control.first_func is True:
            control.max_count_pic = int(message.text.split(" ")[0])
            handlers.min_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), True,
                                       control.max_count_pic)
            control.first_func = False
        elif control.second_func is True:
            control.max_count_pic = int(message.text.split(" ")[0])
            handlers.max_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), True,
                                       control.max_count_pic)
            control.second_func = False
        elif control.third_func is True:
            control.max_count_pic = int(message.text.split(" ")[0])
            handlers.best_price_execute(message, bot.city_name, bot.min_price, bot.max_price, bot.length_to_center,
                                        bot.count_hotels, start(message), start(message), True, control.max_count_pic)
            control.third_func = True


bot.infinity_polling(interval=0, timeout=10)
