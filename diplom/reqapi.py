import requests
from loader import *


class ReqApi:

    def __init__(self):
        self.city_found = None
        self.start_date = None
        self.finish_date = None


    def is_city_exists(self, city_name):
        """
        Метод для проверки существования города где делается соответствующий запрос.
        Если проверка проходит, то выполняется запрос по городу , если нет, то выводится соответствующее сообщение.
        """
        url = "https://hotels4.p.rapidapi.com/locations/search"
        query_string = {"query": city_name.lower(), "locale": "ru_RU"}
        response_for_destination_id = requests.request("GET", url, headers=
                                                        {
                                                            'x-rapidapi-host': "hotels4.p.rapidapi.com",
                                                            'x-rapidapi-key': secret_key_api
                                                        },
                                                        params=query_string, timeout=10)

        if int(response_for_destination_id.status_code) == 200:
            return response_for_destination_id

        elif int(response_for_destination_id.status_code) >= 400:
            raise "Ошибка клиента"

        elif int(response_for_destination_id.status_code) >= 500:
            raise "Ошибка сервера"

    def get_site_response(self, city_name):

        url_for_hotels_list = "https://hotels4.p.rapidapi.com/properties/list"
        querystring_for_hotels_list = {
            "destinationId": self.destination_id_founder(self.data_in_json(ReqApi.is_city_exists(self, city_name))),
            "pageNumber": "1",
            "pageSize": "25",
            "checkIn": self.start_date, "checkOut": self.finish_date,
            "adults1": "1",
            "sortOrder": "PRICE",
            "locale": "ru_RU", "currency": "RUB"}
        return ReqApi.data_in_json(requests.request("GET", url_for_hotels_list, headers=
                                {
                                    'x-rapidapi-host': "hotels4.p.rapidapi.com",
                                    'x-rapidapi-key': secret_key_api
                                },
                                params=querystring_for_hotels_list, timeout=10))

    @staticmethod
    def data_pictures_in_json(response):
        """
        Данная функция открывает файл и засписывает в него json с картинками, получаемый при создании запроса.
        Затем происходит открытие созданного файла в режиме "чтения" и происходит выгрузка данных
        из файла в словарь
        """
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    def pars_picture_dict(self, data_pictures_in_json):
        """
        Данная функция служит для поиска URL изображений в полученном json-файле
        и возращает их в виде списка.
        """
        list_for_url = list()
        list_with_picture = list()
        if "hotelImages" in data_pictures_in_json:
            for dict_with_url_picture in data_pictures_in_json["hotelImages"]:
                if "baseUrl" in dict_with_url_picture:
                    list_for_url.append(dict_with_url_picture["baseUrl"])

        for refactor_url in list_for_url:
            if "_{size}" in refactor_url:
                url = refactor_url.replace("_{size}", "")
                list_with_picture.append(url)

        return list_with_picture

    @staticmethod
    def data_in_json(response):
        """
        Данная функция открывает файл и засписывает в него json получаемый при создании запроса.
        Затем происходит открытие созданного файла в режиме "чтения" и происходит выгрузка данных
        из файла в словарь
        """
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    def destination_id_founder(self, param: dict) -> str:
        """
        Данная функция служит для поиска параметра: "destinationId".
        Который отвечает за идентификаицю города, в котором будет проходить подбор лучшего варинанта.
        """

        for key_def, value_def in param.items():
            if isinstance(value_def, list):
                for list_elem in value_def:
                    if isinstance(list_elem, dict):
                        return self.destination_id_founder(list_elem)

            if key_def == "type" and value_def == "CITY":
                return param.get('destinationId')

    def hotels_list_ret(self, param: dict) -> list:
        """
        Данная функция служит для получения и возвращения полного списка отелей со всеми их показателями и т.д. в
        пределах города.
        """
        stack = list(param.items())
        while stack:
            key, value = stack.pop()
            if isinstance(value, dict):
                stack.extend(value.items())
            elif isinstance(value, list) and key == "results":
                return value

    def found_price(self, param: dict) -> list:
        """
            Данная функция является вспомогательной , её работа заключается в формировании списка ,
            в который входят имя отеля и его цена
        """
        hotel_list = list()
        for key, value in param.items():
            if key == "name":
                name = value
            elif key == "landmarks":
                cycle = value[0]["distance"]
                landmark = str()
                for int_becoming in cycle:
                    if int_becoming == ',':
                        landmark += "."
                    elif int_becoming != ' ':
                        landmark += int_becoming
                    elif int_becoming == " ":
                        break
                landmark = float(landmark)

            elif key == "ratePlan":
                hotel_list.append(name)
                price_dict = dict()
                price_dict['price'] = int(value['price']['exactCurrent'])
                hotel_list.append(price_dict)
                hotel_list.append(landmark)
                return hotel_list

    def low_price(self, param: list, max_hotels_count) -> list:
        """
            Данная функция служит для нахождения указанного количества отелей с минимальной стоимостью за ночь в
            пределах города
        """

        max_hotels = max_hotels_count
        sort_low_price_list = list()
        for elem in param:
            if isinstance(elem, dict):
                sort_low_price_list.append(self.found_price(elem))

        sort_low_price_list = sort_low_price_list[: int(max_hotels)][:]
        return sort_low_price_list

    def high_price(self, param: list, max_hotels_count) -> list:
        """
            Данная функция служит для нахождения указанного количества отелей с максимальной стоимостью за ночь в пределах города
        """
        max_hotels = max_hotels_count
        sort_high_price_list = list()
        for elem in param:
            if isinstance(elem, dict):
                sort_high_price_list.append(self.found_price(elem))

        sort_high_price_list = sort_high_price_list[-1:(len(sort_high_price_list) - (int(max_hotels) + 1)):-1][:]
        return sort_high_price_list

    def best_deal(self, param: list, max_hotels, min_price, max_price, permissible_range) -> list:
        """
            Данная функция возвращает проходится по основному списку с отелями и возвращает список тех отелей,
            который подходят под запросы клиента
        """
        max_hotels = int(max_hotels)
        min_price = int(min_price)
        max_price = int(max_price)
        permissible_range = float(permissible_range)
        sort_suitable_price_list = list()
        test_list = list()

        for elem in param:
            if isinstance(elem, dict):
                test_list.append(self.found_price(elem))

        locale_check = False

        for elem_list in test_list:
            if max_price >= elem_list[1]["price"] >= min_price and elem_list[2] <= permissible_range and len(
                    sort_suitable_price_list) <= max_hotels:
                sort_suitable_price_list.append(elem_list)
                locale_check = True

        if locale_check is False:
            return list()
        else:
            return sort_suitable_price_list
