from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters.byfilters_factories import movie_type_factory, movie_genre_factory, movie_rating_factory


def types_keyboard(types: list[str]) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting movie types.

    Args:
        types (list[str]): The list of movie types.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        types = ['movie', 'tv-series']
        keyboard = types_keyboard(types)
    """
    keyboard = InlineKeyboardMarkup()
    formatted: dict[str, str] = __format_types(types)
    keyboard.add(*(
        InlineKeyboardButton(
            text=display,
            callback_data=movie_type_factory.new(
                display=display,
                value=value
            )
        )
        for value, display in formatted.items()
    ))
    __add_button_any(keyboard, movie_type_factory)
    return keyboard


def genres_keyboard(genres: list[str]) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting movie genres.

    Args:
        genres (list[str]): The list of movie genres.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        genres = ['action', 'comedy', 'drama']
        keyboard = genres_keyboard(genres)
    """
    keyboard = InlineKeyboardMarkup()
    formatted: dict[str, str] = __format_genres(__filter_genres(genres))
    keyboard.add(*(
        InlineKeyboardButton(
            text=display,
            callback_data=movie_genre_factory.new(
                display=display,
                value=value
            )
        )
        for value, display in formatted.items()
    ))
    __add_button_any(keyboard, movie_genre_factory)
    return keyboard


def rating_keyboard(min_rating: int = 1, is_minimum_input: bool = False) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting movie ratings.

    Args:
        min_rating (int, optional): The minimum rating value (default is 1).
        is_minimum_input (bool, optional): Flag indicating if minimum rating input is enabled (default is False).

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        keyboard = rating_keyboard(5, True)
    """
    count_button = 11 - min_rating
    max_rating = 9 if is_minimum_input else 10
    if count_button <= 8:
        row = count_button
    else:
        row = 5
    keyboard = InlineKeyboardMarkup(row_width=row)
    keyboard.add(*(
        InlineKeyboardButton(
            text=num,
            callback_data=movie_rating_factory.new(
                display=num,
                value=num
            )
        )
        for num in range(min_rating, max_rating+1)
    ))
    if is_minimum_input:
        __add_button_any(keyboard, movie_rating_factory)
    return keyboard


def __add_button_any(keyboard: InlineKeyboardMarkup, data_factory: CallbackData) -> None:
    """
    Adds an 'Any' button to the inline keyboard.

    Args:
        keyboard (InlineKeyboardMarkup): The inline keyboard markup.
        data_factory (CallbackData): The callback data factory.

    Returns:
        None

    Example:
        __add_button_any(keyboard, movie_type_factory)
    """
    keyboard.add(InlineKeyboardButton(
        'Любой',
        callback_data=data_factory.new(
            display='Любой',
            value='any',
        ))
    )


def __filter_genres(genres: list[str]) -> list[str]:
    """
    Filters out unwanted genres from the list.

    Args:
        genres (list[str]): The list of movie genres.

    Returns:
        list[str]: The filtered list of movie genres.

    Example:
        genres = ['action', 'comedy', 'drama']
        filtered_genres = __filter_genres(genres)
    """
    genres_to_remove = {'аниме', 'мультфильм', 'для взрослых', 'игра',
                        'концерт', 'новости', 'реальное ТВ', 'ток-шоу',
                        'церемония'}
    return [g for g in genres if g not in genres_to_remove]


def __format_genres(genres: list[str]) -> dict[str, str]:
    """
    Formats the list of genres.

    Args:
        genres (list[str]): The list of movie genres.

    Returns:
        dict[str, str]: The dictionary with formatted genres.

    Example:
        genres = ['action', 'comedy', 'drama']
        formatted_genres = __format_genres(genres)
    """
    return {genre: genre.capitalize() for genre in genres}


def __format_types(types: list[str]) -> dict[str, str]:
    """
    Formats the list of types.

    Args:
        types (list[str]): The list of movie types.

    Returns:
        dict[str, str]: The dictionary with formatted types.

    Example:
        types = ['movie', 'tv-series']
        formatted_types = __format_types(types)
    """
    display_by_value = {type: type for type in types}
    display_types = {'animated-series': 'Анимационный сериал',
                     'anime': 'Аниме',
                     'cartoon': 'Мультфильм',
                     'movie': 'Фильм',
                     'tv-series': 'Сериал',
                     }

    for value, display in display_types.items():
        if value in display_by_value:
            display_by_value[value] = display
    return display_by_value
