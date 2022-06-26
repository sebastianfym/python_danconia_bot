from handlers.handlers_help_funcs import *
from rapid_api.reqapi import ReqApi
from loader.loader import *


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
user_dict_results = user_dict_results


def min_price_execute(message, city_name, count_hotels, cal_star, cal_finish, check_picture, max_count_pic):
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

    check_picture = check_picture
    body_req = ReqApi()
    body_req.city_found = city
    body_req.start_date, body_req.finish_date = cal_star, cal_finish

    city_exists = body_req.get_site_response(body_req.city_found)
    hotels_id_list = processing_name_handlers_id_list_func(city_name)

    returned_all_hotels_list = body_req.hotels_list_ret(city_exists)

    bestdeal_funcs_body_work(city_exists, returned_all_hotels_list, message, body_req, max_hotels, min_price, max_price,
                             permissible_range, check_picture, max_count_pic, hotels_id_list)




