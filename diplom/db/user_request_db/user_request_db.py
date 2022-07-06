import sqlite3

db = sqlite3.connect("show_user_request.db", check_same_thread=False)
sql = db.cursor()


def sql_create_and_check_table(table_name) -> None:
    """
    Функция для создания стола в БД
    """
    sql.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                hotel_name TEXT,
                price_in_date INT,
                price_in_all_time BIGINT,
                distance_to_center INT,
                address TEXT,
                link_to_the_hotel STRING)""")

    db.commit()


def sql_data_check(table_name, hotel_name, price_in_date, price_in_all_time, distance_to_center, address,
                   link_to_the_hotel) -> None:
    """
    Наполнение стола данными и проверка есть ли там уже эти данные или нет, если таких данных там еще нет,
    то они добавляются, если есть, то игнорируются
    """
    sql.execute(f"SELECT * FROM {table_name} WHERE hotel_name = '{hotel_name}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?)", (
            hotel_name, price_in_date, price_in_all_time, distance_to_center, address, link_to_the_hotel
        ))
    else:
        pass


def get_data_in_db(table_name, message, bot) -> None:
    """
    Цикл проходится по всему столу и возвращает кортежи в которых находится информация по отелям в данной
    категории. Затем проходит циклом по каждому кортежу и выводит пользователю информацию из них.
    """

    list_with_tuples_where_are_located_all_hotels_request_info = []
    sql_table = sql.execute(f"SELECT * FROM {table_name}")

    bot.send_message(message.from_user.id, f"По запросу /{table_name} были найдены результаты:")
    for value in sql_table:
        list_with_tuples_where_are_located_all_hotels_request_info.append(value)
        bot.send_message(message.from_user.id, f"Название отеля: {value[0]}"
                                               f"{value[1]}"
                                               f"{value[2]}"
                                               f"{value[3]}"
                                               f"{value[4]}"
                                               f"{value[5]}"
                         )
