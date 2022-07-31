from datetime import timedelta, date, datetime
from telegram_bot_calendar import DetailedTelegramCalendar

from db.user_request_db.user_request_db import get_data_in_db
from loader.loader import bot, ALL_STEPS
from markup.reply_markup.reply_keyboard_markup import markup
from main_state.main_state import UserRequestState
from telebot.types import Message, CallbackQuery
from handlers.handlers import min_price_execute, max_price_execute, best_price_execute
from handlers.handlers_help_funcs import show_result, get_calendar, calendar_command


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    bot.send_message(message.from_user.id, "Рад Вам помочь! Вот перечень моих "
                                           "команд:\n/lowprice\n/highprice\n/bestdeal\n/my_request")


@bot.message_handler(commands=['my_request'])
def my_request(message: Message) -> None:
    get_data_in_db("lowprice", message, bot)
    get_data_in_db("highprice", message, bot)
    get_data_in_db("bestdeal", message, bot)


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.city_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Bangkok):")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_state'] = 'low_price'



@bot.message_handler(commands=['highprice'])
def high_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.city_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Barcelona):")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_state'] = 'high_price'


@bot.message_handler(commands=['bestdeal'])
def best_deal(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.city_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Minsk):")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_state'] = 'best_deal'


@bot.message_handler(state=UserRequestState.city_name)
def city_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
        bot.set_state(message.from_user.id, UserRequestState.max_count_hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city_name'] = message.text
            data['list_with_date'] = list()
    else:
        bot.send_message(message.chat.id, f'Название города может содержать в себе только бувы. Пожалуйста, повторите '
                                          f'попытку')


@bot.message_handler(state=UserRequestState.max_count_hotels)
def max_count_hotels(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_count_hotels'] = int(message.text)
            if data['price_state'] == 'best_deal':
                bot.send_message(message.chat.id, f'Введите максимальную стоимость: ')
                bot.set_state(message.from_user.id, UserRequestState.max_price_hotels, message.chat.id)

            else:

                bot.send_message(message.chat.id, f'Хотите ли Вы увидеть фото отелей?',
                                 reply_markup=markup())
                bot.set_state(message.from_user.id, UserRequestState.check_photo, message.chat.id)
    else:
        bot.send_message(message.chat.id, f'Введите корректное число')


@bot.message_handler(state=UserRequestState.max_price_hotels)
def max_price_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.chat.id, f'Введите минимальную стоимость: ')
        bot.set_state(message.from_user.id, UserRequestState.min_price_hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price_hotels'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Введите корректное число')


@bot.message_handler(state=UserRequestState.min_price_hotels)
def min_price_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserRequestState.distance_to_center, message.chat.id)
        bot.send_message(message.chat.id, 'Введите расстояние к центру города: ')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price_hotels'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Введите корректное число')


@bot.message_handler(state=UserRequestState.distance_to_center)
def distance_to_center(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserRequestState.check_photo, message.chat.id)
        bot.send_message(message.chat.id, f'Хотите ли Вы увидеть фото отелей? ')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance_to_center'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Введите корректное число')


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def handle_arrival_date(call: CallbackQuery):
    today = date.today()
    result, key, step = get_calendar(calendar_id=1,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_in'] = result

            bot.edit_message_text(f"Дата заезда {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            bot.send_message(call.from_user.id, "Выберите дату выезда")
            calendar, step = get_calendar(calendar_id=2,
                                          min_date=result + timedelta(days=1),
                                          max_date=result + timedelta(days=365),
                                          locale="ru",
                                          )

            bot.send_message(call.from_user.id,
                             f"Выберите {ALL_STEPS[step]}",
                             reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_arrival_date(call: CallbackQuery):
    today = date.today()

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        result, key, step = get_calendar(calendar_id=2,
                                         current_date=today,
                                         min_date=data['check_in'],
                                         max_date=data['check_in'] + timedelta(days=365),
                                         locale="ru",
                                         is_process=True,
                                         callback_data=call)
        if not result and key:
            bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                                  call.from_user.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:

            data['check_out'] = result

            first_date_str, second_date_str = str(data['check_in']).split('-'), str(data['check_out']).split('-')
            first_date_date_format = datetime(int(first_date_str[0]), int(first_date_str[1]), int(first_date_str[2]))
            second_date_date_format = datetime(int(second_date_str[0]), int(second_date_str[1]), int(second_date_str[2]))

            if str(second_date_date_format - first_date_date_format).split(' ')[0] == '0:00:00':
                data['days_between_dates'] = 1
                show_result(data["message"], best_price_execute, max_price_execute, min_price_execute, data['check_in'],
                            result, data['max_count_hotels'], data['days_between_dates'])

            elif int(str(second_date_date_format - first_date_date_format).split(' ')[0]) == 1:
                data['days_between_dates'] = 2
                show_result(data["message"], best_price_execute, max_price_execute, min_price_execute, data['check_in'],
                            result, data['max_count_hotels'], data['days_between_dates'])
                
            else:
                data['days_between_dates'] = int(str(second_date_date_format - first_date_date_format).split(' ')[0])
                show_result(data["message"], best_price_execute, max_price_execute, min_price_execute, data['check_in'],
                            result, data['max_count_hotels'], data['days_between_dates'])


@bot.message_handler(func=lambda message: message.text.lower() == "да", state=UserRequestState.check_photo)
def show_user_picture(message) -> None:
    bot.send_message(message.chat.id, "Введите желаемое количество фотографий: ")
    bot.set_state(message.from_user.id, UserRequestState.get_count_photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_photo'] = True
        data["message_chat_id"] = message.chat.id
        data["user_id"] = message.from_user.id
        data["message"] = message


@bot.message_handler(func=lambda message: message.text.lower() == "нет", state=UserRequestState.check_photo)
def check_photo(message) -> None:
    bot.send_message(message.chat.id, "Как пожелаете.\n")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_photo'] = False
        data['count_photo'] = 0
        data["message_chat_id"] = message.chat.id
        data["user_id"] = message.from_user.id
        data["message"] = message
        calendar_command(message)

    bot.set_state(message.from_user.id, UserRequestState.show_result, message.chat.id)


@bot.message_handler(state=UserRequestState.get_count_photo)
def get_count_photo(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.show_result, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_photo'] = int(message.text)
    calendar_command(message)
    bot.set_state(message.from_user.id, UserRequestState.show_result, message.chat.id)


