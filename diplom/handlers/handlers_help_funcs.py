from reqapi import ReqApi
from loader.loader import *
from config_data.config import secret_key_pic
bot = bot
unique_dict_result = unique_dict_result
user_dict_results = user_dict_results


def processing_name_handlers_id_list_func(city_name):
    body_req = ReqApi()
    city_exists = body_req.is_city_exists(city_name)
    if city_exists:
        destination_id_list = body_req.destination_id_founder_func(body_req.data_in_json(city_exists))
        return destination_id_list


def watch_result(message):
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


def send_picture(message, max_count_pic, counter_index_hotel_in_list, hotels_id_list):
    body_req = ReqApi()
    counter = 0
    hotel_id = hotels_id_list[counter_index_hotel_in_list]

    if body_req.data_pictures_in_json(
            requests.request("GET", "https://hotels4.p.rapidapi.com/properties/get-hotel-photos",
                             headers={'x-rapidapi-host': "hotels4.p.rapidapi.com",
                                      'x-rapidapi-key': secret_key_pic}, params={"id": hotel_id})) is not None:
        hotels_photo = body_req.pars_picture_dict(body_req.data_pictures_in_json(requests.request("GET",
                                                                                                  "https://hotels4.p"
                                                                                                  ".rapidapi.com"
                                                                                                  "/properties/get"
                                                                                                  "-hotel-photos",
                                                                                                  headers={
                                                                                                      'x-rapidapi-host': "hotels4.p.rapidapi.com",
                                                                                                      'x-rapidapi-key': secret_key_pic},
                                                                                                  params={
                                                                                                      "id": hotel_id})))
        for picture_url in hotels_photo:
            bot.send_photo(message.chat.id, picture_url)
            counter += 1
            if counter == max_count_pic:
                break
    else:
        bot.send_message(message.chat.id, 'Для этого отеля я фотографий не нашел :C')


def check_and_append(message, price_condition, user_dict, cycle_elem, counter_index_hotel_in_list, check_picture,
                     max_count_pic, hotels_id_list):
    check_picture = check_picture
    if price_condition not in user_dict_results[message.from_user.id]:
        user_dict_results[message.from_user.id][price_condition] = []

    bot.send_message(message.chat.id,
                     f"Название отеля: {str(cycle_elem[0])}.\nЦена: {str(cycle_elem[1]['price'])} "
                     f"руб/сутки")

    if check_picture is True:
        send_picture(message, max_count_pic, counter_index_hotel_in_list, hotels_id_list)

    user_dict_results[message.from_user.id][price_condition].append(
        f"Название отеля: {str(cycle_elem[0])}.\nЦена: {str(cycle_elem[1]['price'])} "
        f"руб/сутки")
    return user_dict


def min_max_funcs_body_work(message, city_exists, body_req, max_hotels, check_picture, max_count_pic, hotels_id_list,
                            search_price_condition):
    if city_exists is None:
        bot.send_message(message.chat.id, "В моем списке нет такого города , попробуйте заново.")
        return None
    elif city_exists is not None:
        returned_all_hotels_list = body_req.hotels_list_ret(city_exists)
        if message.from_user.id not in user_dict_results:
            user_dict_results[message.from_user.id] = {}

        counter = 0
        for low_elem in body_req.low_price(returned_all_hotels_list, max_hotels):
            check_and_append(message, f"/{search_price_condition}", user_dict_results, low_elem, counter, check_picture, max_count_pic,
                             hotels_id_list)
            counter += 1


def bestdeal_funcs_body_work(city_exists, returned_all_hotels_list, message, body_req, max_hotels, min_price, max_price,
                            permissible_range, check_picture, max_count_pic, hotels_id_list):
    if city_exists is None or len(returned_all_hotels_list) == 0:
        bot.send_message(message.chat.id, "В моем списке нет подходящего варианта, попробуйте заново.")
        return None
    else:
        if message.from_user.id not in user_dict_results:
            user_dict_results[message.from_user.id] = {}

        if len(body_req.best_deal(returned_all_hotels_list, max_hotels, min_price, max_price, permissible_range)) == 0:
            bot.send_message(message.chat.id, 'К сожалению по вашему запросу ничего не найдено.')

        counter = 0
        for best_elem in body_req.best_deal(returned_all_hotels_list, max_hotels, min_price, max_price,
                                            permissible_range):
            if '/bestdeal' not in user_dict_results[message.from_user.id]:
                user_dict_results[message.from_user.id]['/bestdeal'] = []

            if check_picture is True:
                send_picture(message, max_count_pic, counter, hotels_id_list)

            bot.send_message(message.chat.id, f"Отель: {best_elem[0]}.\nЦена: {best_elem[1]['price']} руб/сутки."
                                              f"\nРасстояние к центру {best_elem[2]} км.")
            user_dict_results[message.from_user.id]['/bestdeal'].append(f"Отель: {best_elem[0]}.\n"
                                                                        f"Цена: {best_elem[1]['price']} руб/сутки."
                                                                        f"\nРасстояние к центру {best_elem[2]} км.")
            counter += 1


