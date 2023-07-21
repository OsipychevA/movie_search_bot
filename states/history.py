from telebot.handler_backends import State, StatesGroup


class HistoryState(StatesGroup):
    """
    This class extends the StatesGroup class from the telebot library.
    Each attribute of the class is an instance of the State class,
    representing the unique state of the user inside the script
    Attributes
    ----------
        amount:
            Represents a state where the bot is expecting the user to provide the amount of films to display.
    """
    amount = State()
