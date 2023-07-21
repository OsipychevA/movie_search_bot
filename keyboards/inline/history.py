from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters.history_factories import history_factory, history_amount_factory
from utils.presenters import Movie


def history_amount_keyboard() -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting the amount of history items.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        keyboard = history_amount_keyboard()
    """
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(*(
        InlineKeyboardButton(
            text=num,
            callback_data=history_amount_factory.new(
                value=num
            )
        )
        for num in range(1, 10+1)
    ))
    return keyboard


def history_movie_keyboard(movies: list[Movie]) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting a movie from the history.

    Args:
        movies (list[Movie]): The list of movies in the history.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        movies = [Movie(title='Movie 1', id_kp='123'), Movie(title='Movie 2', id_kp='456')]
        keyboard = history_movie_keyboard(movies)
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*(
        InlineKeyboardButton(
            text=movie.title,
            callback_data=history_factory.new(
                id_kp=movie.id_kp
            )
        )
        for movie in movies
    ))
    return keyboard

