from handlers.handlers_help_funcs import min_max_funcs_body_work, processing_name_handlers_id_list_func, bestdeal_funcs_body_work
from rapid_api.reqapi import ReqApi


def min_price_execute(message, city_name, count_hotels, cal_star, cal_finish, check_picture, max_count_pic, days_between_dates):
    max_hotels = count_hotels
    check_picture = check_picture
    body_req = ReqApi()
    body_req.city_found = city_name

    body_req.start_date = cal_star
    body_req.finish_date = cal_finish

    city_exists = body_req.get_site_response(body_req.city_found)
    min_max_funcs_body_work(message, city_exists, body_req, max_hotels, check_picture, max_count_pic, 'lowprice', days_between_dates)


def max_price_execute(message, city_name, count_hotels, cal_star, cal_finish, check_picture, max_count_pic, days_between_dates):
    max_hotels = count_hotels

    body_req = ReqApi()
    body_req.city_found = city_name
    body_req.start_date = cal_star
    body_req.finish_date = cal_finish

    city_exists = body_req.get_site_response(body_req.city_found)
    min_max_funcs_body_work(message, city_exists, body_req, max_hotels, check_picture, max_count_pic, 'highprice', days_between_dates)


def best_price_execute(message, city_name, min_price, max_price, length_to_center, count_hotels, cal_star, cal_finish,
                       check_picture, max_count_pic, days_between_dates):
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
                             permissible_range, check_picture, max_count_pic, hotels_id_list, days_between_dates)


