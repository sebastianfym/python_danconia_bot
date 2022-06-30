from telebot.handler_backends import State, StatesGroup


class UserRequestState(StatesGroup):
    low_price = False
    high_price = False
    best_deal = False

    city_name = State()
    max_count_hotels = State()
    min_price_hotels = State()
    max_price_hotels = State()
    distance_to_center = State()

    check_photo = State()
    show_result = State()
    get_count_photo = State()

    user_dict_results = {}

    list_with_date = []


class DateRangeState(StatesGroup):
    check_in = State()
