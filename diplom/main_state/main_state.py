from telebot.handler_backends import State, StatesGroup


class UserRequestState(StatesGroup):
    help = State()
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

    my_request = State()

    user_dict_results = {}

    test_calendar_first_date = State()
    test_calendar_second_date = State()

    list_with_date = []
    test_variable = State()
