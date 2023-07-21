from telebot.types import Message

from loader import bot


@bot.message_handler(regexp='Привет')
def bot_hello(message: Message):
    """ This module contains a function for handling the 'Привет' message and replying with a greeting.

    Functions: bot_hello: Handles the 'Привет' message and replies with a greeting.

    """
    bot.reply_to(
        message, f'И тебе привет, {message.from_user.first_name}! '
                 f'Список моих команд можно посмотреть здесь - /help'
    )