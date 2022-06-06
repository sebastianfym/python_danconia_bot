from handlers.handlers import *
from loader.loader import *


# @bot.message_handler(func=lambda message: message.text.lower() == "/help" or message.text.lower() == "привет"
#                                           or message.text.lower() == "/start")
# def help(message):
#     bot.send_message(message.chat.id, "Рад Вам помочь! Вот перечень моих "
#                                       "команд:\n/lowprice\n/highprice\n/bestdeal\n/my_request")
#     description_commands(message)
#     user = Users.get_user(message.from_user.id)
#     user.command = dict()
#
#
# @bot.message_handler(func=lambda message: message.text.lower() == "/lowprice")
# def low_price(message):
#     bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
#     control.check_low = True
#     control.city_name = True
#
#
# @bot.message_handler(func=lambda message: message.text.lower() == "/highprice")
# def high_price(message):
#     bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
#     control.check_max = True
#     control.city_name = True
#
#
# @bot.message_handler(func=lambda message: message.text.lower() == "/bestdeal")
# def best_deal(message):
#     bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Санкт-Петербург):")
#     control.check_best_deal = True
#     control.city_name = True


# @bot.message_handler(func=lambda message: message.text.lower() == "/my_request")
# def id_user(message):
#     watch_result(message)


# @bot.message_handler(func=lambda message: message.text.lower() == "да")
# def print_user_picture(message):
#     bot.send_message(message.chat.id, "Введите желаемое количество фотографий: ")
#     control.check_picture = True
#
#
# @bot.message_handler(func=lambda message: message.text.lower() == "нет")
# def continue_work(message):
#     bot.send_message(message.chat.id, "Как пожелаете.")
#     if control.first_func is True:
#         min_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), False, 0)
#         control.first_func = False
#
#     elif control.second_func is True:
#         max_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), False, 0)
#         control.second_func = False
#
#     elif control.third_func is True:
#         best_price_execute(message, bot.city_name, bot.min_price, bot.max_price, bot.length_to_center,
#                            bot.count_hotels, start(message), start(message), False, 0)
#         control.third_func = False


# @bot.message_handler(content_types=['text', 'number'])
# def performance_func(message):
#     user = Users.get_user(message.chat.id)
#     if control.check_low is True:
#         low_func_accomplishemnt(message, user, control)
#
#     elif control.check_max is True:
#         max_func_accomplishment(message, user, control)
#
#     elif control.check_best_deal is True:
#         best_deal_func_accomplishment(message, user, control)
#
#     elif control.check_picture is True:
#         if control.first_func is True:
#             control.max_count_pic = int(message.text.split(" ")[0])
#             min_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), True,
#                               control.max_count_pic)
#             control.first_func = False
#
#         elif control.second_func is True:
#             control.max_count_pic = int(message.text.split(" ")[0])
#             max_price_execute(message, bot.city_name, bot.count_hotels, start(message), start(message), True,
#                               control.max_count_pic)
#             control.second_func = False
#
#         elif control.third_func is True:
#             control.max_count_pic = int(message.text.split(" ")[0])
#             best_price_execute(message, bot.city_name, bot.min_price, bot.max_price, bot.length_to_center,
#                                bot.count_hotels, start(message), start(message), True, control.max_count_pic)
#             control.third_func = True


