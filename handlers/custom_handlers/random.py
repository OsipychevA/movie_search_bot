from telebot.types import Message

from database.functions import save_random_request, save_movies
from loader import bot
from core.api import MoviesApi
from config_data import config
from utils.senders import send_movie_message


@bot.message_handler(commands=['random'])
def random(message: Message) -> None:
    """
    Handles the '/random' command and sends a message with random movie to the chat.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    movies = MoviesApi(config.API_KEY, config.API_HOST)
    result = movies.random()
    save_movies(movies=[result],
                request=save_random_request(message.from_user.id))
    send_movie_message(message.chat.id, result)
