from telebot.handler_backends import State, StatesGroup


class SearchFilmByFiltersState(StatesGroup):
    """
    This class extends the StatesGroup class from the telebot library.
    Each attribute of the class is an instance of the State class,
    representing the unique state of the user inside the script
    Attributes
    ----------
        type:
            Represents a state where the bot is expecting the user to provide the type of the film.
        genre:
            Represents a state where the bot is expecting the user to provide the genre of the film.
        rating:
            Represents a state where the bot is expecting the user to provide the rating of the film.
        year:
            Represents a state where the bot is expecting the user to provide the release year of the film.
        amount:
            Represents a state where the bot is expecting the user to provide the amount of films to display.
        pagination:
            Represents a state where the bot is managing pagination of the displayed films.
    """
    type = State()
    genre = State()
    rating = State()
    year = State()
    amount = State()
    pagination = State()
