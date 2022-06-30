import telebot
from config_data.config import config

bot = telebot.TeleBot(config['token'])
ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
