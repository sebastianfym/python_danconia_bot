import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружена, т.к. отсутствует файл .env')
else:
    load_dotenv()

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
secret_key = os.getenv("key")
secret_key_api = os.getenv('key_api')
secret_key_pic = os.getenv('key_pic')

config = {
    "name": "DanconiaTravelBot",
    "token": secret_key
}

DEFAULT_COMMANDS = (
    ('help', 'Вывести справку'),
    ('lowprice', 'Сортировка отелей с найменьшей ценой'),
    ('highprice', 'Сортировка отелей с найвысшей ценой'),
    ('bestdeal', 'Сортировка отелей с вашими параметрами'),
    ('my_request', 'Выводии на экран все Ваши запросы')
)

