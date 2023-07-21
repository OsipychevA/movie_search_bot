from telebot import AdvancedCustomFilter
from telebot.callback_data import CallbackDataFilter
from telebot.types import CallbackQuery


class CallbackFilter(AdvancedCustomFilter):
    """
    Custom filter for handling callback queries.

    Attributes:
        key (str): The key used to identify the filter.

    Methods:
        check(query: CallbackQuery, config: CallbackDataFilter) -> bool:
            Checks if the callback query matches the filter configuration.

    Example:
        filter = CallbackFilter()
        if filter.check(query, config):
            # Handle the callback query
    """
    key = 'query'

    def check(self, query: CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Checks if the callback query matches the filter configuration.

        Args:
            query (CallbackQuery): The callback query to be checked.
            config (CallbackDataFilter): The filter configuration.

        Returns:
            bool: True if the callback query matches the filter configuration, False otherwise.
        """
        return config.check(query=query)
