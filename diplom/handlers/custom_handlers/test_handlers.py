from loader.loader import bot, start
from markup.reply_markup.reply_keyboard_markup import request_photo_keyboard
from test_state.test_state import UserRequestState
from telebot.types import Message
from handlers.handlers import ControlBot, min_price_execute, max_price_execute, best_price_execute

control = ControlBot()


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.help, message.chat.id)
    bot.send_message(message.from_user.id, "Рад Вам помочь! Вот перечень моих "
                                           "команд:\n/lowprice\n/highprice\n/bestdeal\n/my_request")


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.city_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Tver):")
    control.min_price_func_check_in_test_handlers = True


@bot.message_handler(commands=['highprice'])
def high_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.city_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Saint Petersburg):")
    control.high_price_func_check_in_test_handlers = True


@bot.message_handler(commands=['bestdeal'])
def best_deal(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.city_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите желаемый город для отдыха (Пример: Moscow):")
    control.best_deal_func_check_in_test_handlers = True


@bot.message_handler(state=UserRequestState.city_name)
def city_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.chat.id, f'Введите максимальное количество отелей: ')
        bot.set_state(message.from_user.id, UserRequestState.max_count_hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city_name'] = message.text
    else:
        bot.send_message(message.chat.id, f'Название города может содержать в себе только бувы. Пожалуйста, повторите '
                                          f'попытку')


@bot.message_handler(state=UserRequestState.max_count_hotels)
def max_count_hotels(message: Message) -> None:
    if message.text.isdigit():
        if control.best_deal_func_check_in_test_handlers is True:
            bot.send_message(message.chat.id, f'Введите максимальную стоимость: ')
            bot.set_state(message.from_user.id, UserRequestState.max_price_hotels, message.chat.id)

        else:
            bot.send_message(message.chat.id, f'Хотите ли Вы увидеть фото отелей?',
                             reply_markup=request_photo_keyboard())
            bot.set_state(message.from_user.id, UserRequestState.check_photo, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_count_hotels'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Название города может содержать в себе только бувы. Пожалуйста, повторите '
                                          f'попытку')


@bot.message_handler(state=UserRequestState.max_price_hotels)
def max_price_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.chat.id, f'Введите минимальную стоимость: ')
        bot.set_state(message.from_user.id, UserRequestState.min_price_hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price_hotels'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Цифра не может содержать в себе буквы.')


@bot.message_handler(state=UserRequestState.min_price_hotels)
def min_price_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserRequestState.distance_to_center, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price_hotels'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Цифра не может содержать в себе буквы.')


@bot.message_handler(state=UserRequestState.distance_to_center)
def distance_to_center(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserRequestState.check_photo, message.chat.id)
        bot.send_message(message.chat.id, f'Хотите ли Вы увидеть фото отелей? ')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance_to_center'] = int(message.text)
    else:
        bot.send_message(message.chat.id, f'Цифра не может содержать в себе буквы.')


@bot.message_handler(func=lambda message: message.text.lower() == "да", state=UserRequestState.check_photo)
def show_user_picture(message) -> None:
    print("YES")
    bot.send_message(message.chat.id, "Введите желаемое количество фотографий: ")
    bot.set_state(message.from_user.id, UserRequestState.get_count_photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_photo'] = message.text


@bot.message_handler(func=lambda message: message.text.lower() == "нет", state=UserRequestState.check_photo)
def check_photo(message) -> None:
    print("NO")
    bot.send_message(message.chat.id, "Как пожелаете.\nВыберите дату поездки:")
    bot.set_state(message.from_user.id, UserRequestState.show_result, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_photo'] = message.text
        data['count_photo'] = 0


@bot.message_handler(state=UserRequestState.get_count_photo)
def get_count_photo(message: Message) -> None:
    bot.set_state(message.from_user.id, UserRequestState.show_result, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_photo'] = int(message.text)


@bot.message_handler(state=UserRequestState.show_result)
def show_result_func(message: Message) -> None:
    bot.set_state((message.from_user.id, UserRequestState.start, message.chat.id))
    print("show result")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if control.best_deal_func_check_in_test_handlers is True:
            control.best_deal_func_check_in_test_handlers = False
            best_price_execute(message, data['city_name'], data['min_price_hotels'], data['max_price_hotels'],
                               data['distance_to_center'], data['max_count_hotels'], start(message), start(message),
                               data['check_photo'], data['count_photo'])

        elif control.high_price_func_check_in_test_handlers is True:
            control.high_price_func_check_in_test_handlers = False
            max_price_execute(message, data['city_name'], data['max_count_hotels'], start(message), start(message),
                              data['check_photo'], data['count_photo'])

        elif control.min_price_func_check_in_test_handlers is True:
            control.min_price_func_check_in_test_handlers = False
            min_price_execute(message, data['city_name'], data['max_count_hotels'], start(message), start(message),
                              data['check_photo'], data['count_photo'])


