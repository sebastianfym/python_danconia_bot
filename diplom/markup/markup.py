from telebot import types

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_yes = types.KeyboardButton("Да")
button_no = types.KeyboardButton("Нет")

markup.add(button_yes, button_no)