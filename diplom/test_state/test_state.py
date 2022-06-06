from telebot.handler_backends import State, StatesGroup

"""
    low_price/high_price
        1. получение названия города
        2. получение максимального количества отелей
        3. фото - да/нет
    
    best_deal
        1. получение названия города
        2. получение минимальной цены
        3. получение максимальнной цены
        4. полечение допустимого расстояния к центру
        5. получение максимального количества отелей
        6. фото - да/нет
"""


class UserRequestState(StatesGroup):
    start = State()

    help = State()
    low_price = State()
    high_price = State()
    best_deal = State()

    city_name = State()
    max_count_hotels = State()
    min_price_hotels = State()
    max_price_hotels = State()
    distance_to_center = State()

    check_photo = State()
    show_result = State()
    get_count_photo = State()
