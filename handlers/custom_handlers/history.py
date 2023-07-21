import time

from telebot.types import Message, CallbackQuery

from config_data import config
from core.api import MoviesApi
from database.functions import get_history
from filters.history_factories import history_factory, history_amount_factory
from keyboards.inline.history import history_amount_keyboard, history_movie_keyboard
from states.history import HistoryState
from loader import bot
from utils.senders import send_movie_message


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """
    Handles the '/history' command and initiates the process of displaying the user's request history.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    bot.delete_state(message.from_user.id)
    bot.set_state(message.from_user.id, HistoryState.amount)
    bot.send_message(message.chat.id, f'Сколько последних запросов показать?', reply_markup=history_amount_keyboard())


@bot.callback_query_handler(func=None, query=history_amount_factory.filter())
def get_amount(query: CallbackQuery) -> None:
    """
    Retrieves the specified amount of history requests and displays them to the user.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    callback_data = history_amount_factory.parse(query.data)
    history_list = get_history(user_id=query.from_user.id, amount=int(callback_data['value']))
    for request in history_list:
        bot.send_message(query.message.chat.id, request.to_html(),
                         reply_markup=history_movie_keyboard(request.movies),
                         parse_mode='HTML')
        time.sleep(0.2)


@bot.callback_query_handler(func=None, query=history_factory.filter())
def show_movie_from_history(query: CallbackQuery) -> None:
    """
    Displays detailed information about a movie from the user's request history.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    callback_data = history_factory.parse(query.data)
    movies_api = MoviesApi(config.API_KEY, config.API_HOST)
    movie = movies_api.byid(int(callback_data['id_kp']))
    send_movie_message(query.message.chat.id, movie)




