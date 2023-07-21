from telebot.types import ReplyKeyboardMarkup


def pagination_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates a reply keyboard markup for pagination.

    Returns:
        ReplyKeyboardMarkup: The reply keyboard markup.

    Example:
        markup = pagination_keyboard()
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Хватит', 'Далее')
    return markup

