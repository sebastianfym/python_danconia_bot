import sqlite3


def sql_create_and_check_table(table_name) -> None:
    """
    Функция для создания стола в БД
    """
    with sqlite3.connect('user_requests.db') as connect:
        sql = connect.cursor()

        sql.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                    hotel_name TEXT,
                    price_in_date INT,
                    price_in_all_time BIGINT,
                    distance_to_center INT,
                    address TEXT,
                    link_to_the_hotel STRING,
                    user_id INT)""")

        connect.commit()


def sql_data_check(table_name, hotel_name, price_in_date, price_in_all_time, distance_to_center, address,
                   link_to_the_hotel, user_id) -> None:
    """
    Наполнение стола данными и проверка есть ли там уже эти данные или нет, если таких данных там еще нет,
    то они добавляются, если есть, то игнорируются
    """
    with sqlite3.connect('user_requests.db') as connect:
        sql = connect.cursor()

        sql.execute(f"SELECT * FROM {table_name} WHERE hotel_name = '{hotel_name}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (hotel_name, price_in_date, price_in_all_time, distance_to_center, address,
                         link_to_the_hotel, user_id)
                        )


def get_data_in_db(table_name, message, bot) -> None:
    """
    Цикл проходится по всему столу и возвращает кортежи в которых находится информация по отелям в данной
    категории. Затем проходит циклом по каждому кортежу и выводит пользователю информацию из них.
    """
    with sqlite3.connect('user_requests.db') as connect:
        sql = connect.cursor()

        sql_table = sql.execute(f"SELECT * FROM {table_name}")

        bot.send_message(message.from_user.id, f"По запросу /{table_name} были найдены результаты:")
        for value in sql_table:
            if message.from_user.id == value[6]:
                bot.send_message(message.from_user.id, f"Название отеля: {value[0]}\n"
                                                       f"Цена за сутки: {value[1]}р.\n"
                                                       f"Цена за всё время: {value[2]}р.\n"
                                                       f"Расстояние к центру: {value[3]}км.\n"
                                                       f"Адрес: {value[4]}\n"
                                                       f"Ссылка на отель: {value[5]}\n"
                                 )
