from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters.byfilters_factories import movie_amount_factory, movie_pagination_factory


def amount_keyboard() -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting the amount of movies.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        keyboard = amount_keyboard()
    """
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(*(
        InlineKeyboardButton(
            text=num,
            callback_data=movie_amount_factory.new(
                value=num
            )
        )
        for num in range(1, 5+1)
    ))
    return keyboard


def pagination_keyboard() -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for pagination.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup.

    Example:
        keyboard = pagination_keyboard()
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Хватит',
            callback_data=movie_pagination_factory.new(value='stop')),
        InlineKeyboardButton(
            text='Далее',
            callback_data=movie_pagination_factory.new(value='next'))
    )

    return keyboard
