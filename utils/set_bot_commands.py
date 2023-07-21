from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    """
    Sets the default commands for the bot.

    Args:
        bot: The bot instance.

    Returns:
        None

    Example:
        set_default_commands(bot)

    Note: Make sure to import the required modules and define the `DEFAULT_COMMANDS` list before calling this function.

    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
