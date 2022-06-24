from handlers.handlers_help_funcs import *
from reqapi import ReqApi
from loader.loader import *


class ControlBot:
    def __init__(self):
        self.check_low = False
        self.check_max = False
        self.check_best_deal = False
        self.check_picture = False

        self.count_hostels = False
        self.city_name = None
        self.max_price = False
        self.min_price = False
        self.length_to_center = False

        self.first_func = False
        self.second_func = False
        self.third_func = False

        self.counter_index_hotel_in_list = None

        self.max_count_pic = None

        self.destination_id_list = []

        self.min_price_func_check_in_test_handlers = False
        self.high_price_func_check_in_test_handlers = False
        self.best_deal_func_check_in_test_handlers = False


class Users:
    users = dict()

    def __init__(self, user_id):
        self.city = None
        self.check_in = None
        self.hotels_count = None
        self.command = None,
        Users.add_user(user_id, self)

    @staticmethod
    def get_user(user_id):
        if Users.users.get(user_id) is None:
            new_user = Users(user_id)
            return new_user
        return Users.users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.users[user_id] = user


bot = bot
control = ControlBot()
unique_dict_result = unique_dict_result
user_dict_results = user_dict_results


def min_price_execute(message, city_name, count_hotels, cal_star, cal_finish, check_picture, max_count_pic):
    control.check_low = False
    max_hotels = count_hotels
    check_picture = check_picture
    body_req = ReqApi()
    body_req.city_found = city_name

    body_req.start_date = cal_star
    body_req.finish_date = cal_finish

    city_exists = body_req.get_site_response(body_req.city_found)
    hotels_id_list = processing_name_handlers_id_list_func(city_name)

    min_max_funcs_body_work(message, city_exists, body_req, max_hotels, check_picture, max_count_pic, hotels_id_list,
                            'lowprice')


def max_price_execute(message, city_name, count_hotels, cal_star, cal_finish, check_picture, max_count_pic):
    control.check_max = False
    max_hotels = count_hotels

    body_req = ReqApi()
    body_req.city_found = city_name
    body_req.start_date = cal_star
    body_req.finish_date = cal_finish

    city_exists = body_req.get_site_response(body_req.city_found)
    hotels_id_list = processing_name_handlers_id_list_func(city_name)

    min_max_funcs_body_work(message, city_exists, body_req, max_hotels, check_picture, max_count_pic, hotels_id_list,
                            'highprice')


def best_price_execute(message, city_name, min_price, max_price, length_to_center, count_hotels, cal_star, cal_finish,
                       check_picture, max_count_pic):
    city, min_price, max_price, permissible_range, max_hotels = city_name, min_price, max_price, length_to_center, \
                                                                count_hotels

    control.check_best_deal = False
    check_picture = check_picture
    body_req = ReqApi()
    body_req.city_found = city
    body_req.start_date, body_req.finish_date = cal_star, cal_finish

    city_exists = body_req.get_site_response(body_req.city_found)
    hotels_id_list = processing_name_handlers_id_list_func(city_name)

    returned_all_hotels_list = body_req.hotels_list_ret(city_exists)

    bestdeal_funcs_body_work(city_exists, returned_all_hotels_list, message, body_req, max_hotels, min_price, max_price,
                             permissible_range, check_picture, max_count_pic, hotels_id_list)


def check_property(message):
    bot.send_message(message.chat.id, "Введите корректное число: ")
    return



