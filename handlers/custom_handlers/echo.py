from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """ This module contains a function for handling echo messages and providing a default response.
    """
    bot.send_message(message.chat.id, f'Если вы не знаете с чего начать - используйте команду /help')
