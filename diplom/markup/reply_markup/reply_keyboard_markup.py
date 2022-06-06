from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_photo_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Нет'))
    return keyboard
