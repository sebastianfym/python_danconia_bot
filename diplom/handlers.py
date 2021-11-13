from reqapi import ReqApi
import loader

bot = loader.bot


class ControlBot:
    def __init__(self):
        self.check_low = False
        self.check_max = False
        self.check_best_deal = False
        self.check_picture = False
        self.check_date = False
        self.property_list = list()

        self.count_hostels = False
        self.city_name = None
        self.max_price = False
        self.min_price = False
        self.length_to_center = False

        self.first_func = False
        self.second_func = False
        self.third_func = False


control = ControlBot()
unique_dict_result = loader.unique_dict_result
user_dict_results = loader.user_dict_results


def watch_result(message):
    # for result_elem in user_dict_results.keys():
    #     if len(user_dict_results[result_elem]) != 0:
    #         bot.send_message(message.chat.id, f"По запросу команды {result_elem} вы смотрели варианты:")
    #         for results_show in user_dict_results[result_elem]:
    #             bot.send_message(message.chat.id, results_show)
    #     else:
    #         bot.send_message(message.chat.id, f"Вы еще не делали запроса по команде {result_elem}.")
    # unique_dict_result[message.chat.id] = user_dict_results
    # return unique_dict_result

    # user_dict_results[message.from_user.id] = {}
    # user_dict_results[message.from_user.id]['/lowprice'] = []

    if message.from_user.id not in user_dict_results:
        bot.send_message(message.chat.id, 'Вы пока-еще не делали запросов. Попробуйте попозже.')
        return None
    else:
        for result_elem in user_dict_results[message.from_user.id].keys():
            if len(user_dict_results[message.from_user.id][result_elem]) >= 1:
                bot.send_message(message.chat.id, f"По запросу команды {result_elem} вы смотрели варианты:")
                for show_result in user_dict_results[message.from_user.id][result_elem]:
                    bot.send_message(message.chat.id, show_result)
            else:
                bot.send_message(message.chat.id, f'Вы еще не делали запросов по {result_elem}')


def description_commands(message):
    bot.send_message(message.chat.id, "/lowprice - демонстрирует вашему вниманию отели с самой минимальной платой за "
                                      "ночь. "
                                      "\n/highprice - демонстрирует вашему вниманию отели с самой максимальной платой "
                                      "за ночь. "
                                      "\n/bestdeal  - демонстрирует вашему вниманию отели учитывая все ваши пожелания."
                                      "\n/my_request - с помощью данной команды вы можете ознакомиться с запросами, "
                                      "которые делали раньше")


def min_price_execute(message, city_name, count_hotels):
    control.check_low = False
    max_hotels = count_hotels

    body_req = ReqApi()
    body_req.city_found = city_name

    body_req.start_date = loader.start(message)
    body_req.finish_date = loader.start(message)

    city_exists = body_req.get_site_response(body_req.city_found, body_req.start_date,
                                             body_req.finish_date)
    if city_exists is None:
        bot.send_message(message.chat.id, "В моем списке нет такого города , попробуйте заново.")
        return None
    elif city_exists is not None:
        returned_all_hotels_list = body_req.hotels_list_ret(city_exists)
        if message.from_user.id not in user_dict_results:
            user_dict_results[message.from_user.id] = {}
        for low_elem in body_req.low_price(returned_all_hotels_list, max_hotels):
            # if isinstance(low_elem, list):
            # if "/lowprice" in user_dict_results:
            #     bot.send_message(message.chat.id,
            #                      f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #                      f"руб/сутки")
            #     user_dict_results["/lowprice"].append(
            #         f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #         f"руб/сутки")
            # else:
            #     user_dict_results["/lowprice"] = list()
            #     bot.send_message(message.chat.id,
            #                      f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #                      f"руб/сутки")
            #     user_dict_results["/lowprice"].append(
            #         f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #         f"руб/сутки")

            # if message.from_user.id not in user_dict_results:
            #     user_dict_results[message.from_user.id] = {}
            #     user_dict_results[message.from_user.id]['/lowprice'] = []
            #     bot.send_message(message.chat.id,
            #                      f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #                      f"руб/сутки")
            #     user_dict_results[message.from_user.id]['/lowprice'].append(
            #         f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #         f"руб/сутки")
            # else:
            #     # user_dict_results[message.from_user.id]['/lowprice'] = []
            #     bot.send_message(message.chat.id,
            #                      f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #                      f"руб/сутки")
            #     user_dict_results[message.from_user.id]['/lowprice'].append(
            #         f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
            #         f"руб/сутки")

            if '/lowprice' not in user_dict_results[message.from_user.id]:
                user_dict_results[message.from_user.id]['/lowprice'] = []
                bot.send_message(message.chat.id,
                                 f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
                                 f"руб/сутки")
                user_dict_results[message.from_user.id]['/lowprice'].append(
                    f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
                    f"руб/сутки")
            else:
                bot.send_message(message.chat.id,
                                 f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
                                 f"руб/сутки")
                user_dict_results[message.from_user.id]['/lowprice'].append(
                    f"Название отеля: {str(low_elem[0])}.\nЦена: {str(low_elem[1]['price'])} "
                    f"руб/сутки")



def max_price_execute(message, city_name, count_hotels):
    control.check_max = False
    max_hotels = count_hotels

    body_req = ReqApi()
    body_req.city_found = city_name

    body_req.start_date = loader.start(message)
    body_req.finish_date = loader.start(message)

    city_exists = body_req.get_site_response(body_req.city_found, body_req.start_date,
                                             body_req.finish_date)

    if city_exists is None:
        bot.send_message(message.chat.id, "В моем списке нет такого города , попробуйте заново.")
        return None
    elif city_exists is not None:
        returned_all_hotels_list = body_req.hotels_list_ret(city_exists)

        if message.from_user.id not in user_dict_results:
            user_dict_results[message.from_user.id] = {}
        for high_elem in body_req.high_price(returned_all_hotels_list, max_hotels):
            # if isinstance(high_elem, list):
            #     if "/highprice" in user_dict_results:
            #         bot.send_message(message.chat.id,
            #                          f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
            #                          f"руб/сутки")
            #         user_dict_results["/highprice"].append(
            #             f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
            #             f"руб/сутки")
            #     else:
            #         user_dict_results["/highprice"] = list()
            #         bot.send_message(message.chat.id,
            #                          f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
            #                          f"руб/сутки")
            #         user_dict_results["/highprice"].append(
            #             f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
            #             f"руб/сутки")

            # if message.from_user.id not in user_dict_results:
            #     user_dict_results[message.from_user.id] = {}
            if '/highprice' not in user_dict_results[message.from_user.id]:
                user_dict_results[message.from_user.id]['/highprice'] = []
                bot.send_message(message.chat.id,
                                 f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
                                 f"руб/сутки")
                user_dict_results[message.from_user.id]['/highprice'].append(
                    f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
                    f"руб/сутки")
            else:
                # user_dict_results[message.from_user.id]['/highprice'] = []
                bot.send_message(message.chat.id,
                                 f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
                                 f"руб/сутки")
                user_dict_results[message.from_user.id]['/highprice'].append(
                    f"Название отеля: {str(high_elem[0])}.\nЦена: {str(high_elem[1]['price'])} "
                    f"руб/сутки")


def best_price_execute(message, city_name, min_price, max_price, length_to_center, count_hotels):
    city, min_price, max_price, permissible_range, max_hotels = city_name, min_price, max_price, length_to_center, \
                                                                count_hotels

    control.check_best_deal = False

    body_req = ReqApi()
    body_req.city_found = city
    body_req.start_date, body_req.finish_date = loader.start(message), loader.start(message)
    city_exists = body_req.get_site_response(body_req.city_found, body_req.start_date, body_req.finish_date)
    returned_all_hotels_list = body_req.hotels_list_ret(city_exists)
    if city_exists is None or len(returned_all_hotels_list):
        bot.send_message(message.chat.id, "В моем списке нет подходящего варианта, попробуйте заново.")
        return None
    else:
        # returned_all_hotels_list = body_req.hotels_list_ret(city_exists)
        if message.from_user.id not in user_dict_results:
            user_dict_results[message.from_user.id] = {}

        for best_elem in body_req.best_deal(returned_all_hotels_list, max_hotels, min_price, max_price,
                                            permissible_range):
            if '/bestdeal' not in user_dict_results[message.from_user.id]:
                user_dict_results[message.from_user.id]['/bestdeal'] = []
                bot.send_message(message.chat.id, f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
                                                  f"\nРасстояние к центру {best_elem[2]} км.")
                user_dict_results[message.from_user.id]['/bestdeal'].append(f"Отель: {best_elem[0]}.\n"
                                                                            f"Цена: {best_elem[1]['price']} руб/сутки."
                                                                            f"\nРасстояние к центру {best_elem[2]} км.")
            else:
                bot.send_message(message.chat.id, f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
                                                  f"\nРасстояние к центру {best_elem[2]} км.")
                user_dict_results[message.from_user.id]['/bestdeal'].append(f"Отель: {best_elem[0]}.\n"
                                                                            f"Цена: {best_elem[1]['price']} руб/сутки."
                                                                            f"\nРасстояние к центру {best_elem[2]} км.")
            # if "/bestdeal" in user_dict_results:
            #     for best_elem in body_req.best_deal(returned_all_hotels_list, max_hotels, min_price, max_price,
            #                                         permissible_range):
            #         bot.send_message(message.chat.id, f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
            #                                           f"\nРасстояние к центру {best_elem[2]} км.")
            #         user_dict_results["/bestdeal"].append(
            #             f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
            #             f"\nРасстояние к центру {best_elem[2]} км.")
            # else:
            #     user_dict_results["/bestdeal"] = list()
            #     for best_elem in body_req.best_deal(returned_all_hotels_list, max_hotels, min_price, max_price,
            #                                         permissible_range):
            #         bot.send_message(message.chat.id, f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
            #                                           f"\nРасстояние к центру {best_elem[2]} км.")
            #         user_dict_results["/bestdeal"].append(
            #             f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
            #             f"\nРасстояние к центру {best_elem[2]} км.")


def send_picture(message, max_count_pic):
    body_req = ReqApi()
    counter = 0
    for picture_url in body_req.pars_picture_dict(body_req.data_pictures_in_json(body_req.picture_response)):
        bot.send_photo(message.chat.id, picture_url)
        counter += 1
        if counter == max_count_pic:
            break


def check_property(message, first_check, sec_check):
    # bot.send_message(message.chat.id, "Введите корректное число: ")
    first_check = False
    sec_check = True
    bot.send_message(message.chat.id, "Введите корректное число: ")
    return