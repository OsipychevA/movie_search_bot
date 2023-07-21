from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.delete_state(message.from_user.id)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}! '
                                      f'Это бот для поиска информации о фильмах. '
                                      f'Подробная информация - /help')
