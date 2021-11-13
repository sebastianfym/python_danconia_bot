from dotenv import load_dotenv
from pathlib import Path
import os
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

##TODO сделать проверки входящих от пользователя чисел. Пример : "вопрос: сколько отелей?   ответ: -10" , минусовых значений быть не должно!!! и т.д.

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

pattern_city = r"\b\w{1,}\D\w{1,}\D\b"
patter_max_hotels = r'\b\d\b'
pattern_date = r'\d{4}[-]\d\d[-]\d\d'

bot = telebot.TeleBot(config['token'])

unique_dict_result = dict()
user_dict_results = dict()


@bot.message_handler(commands=['calendar'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
