from dotenv import load_dotenv
from pathlib import Path
import os
import telebot
from telebot import types


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_yes = types.KeyboardButton("Да")
button_no = types.KeyboardButton("Нет")

markup.add(button_yes, button_no)


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


bot = telebot.TeleBot(config['token'])

unique_dict_result = dict()
user_dict_results = dict()


