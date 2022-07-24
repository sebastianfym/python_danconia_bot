from telebot.custom_filters import StateFilter
from db.user_request_db.user_request_db import sql_create_and_check_table
from loader.loader import bot
from utils.set_bot_commands import set_default_commands
from handlers.custom_handlers import command_handlers

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    sql_create_and_check_table('lowprice')
    sql_create_and_check_table('highprice')
    sql_create_and_check_table('bestdeal')
    bot.infinity_polling(interval=0, timeout=10)
