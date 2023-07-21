import time

from telebot.types import Message, CallbackQuery

from config_data import config
from core.api import MoviesApi
from database.functions import save_byfilters_request, save_movies
from filters.byfilters_factories import movie_type_factory, movie_genre_factory, movie_rating_factory, \
    movie_amount_factory, movie_pagination_factory
from keyboards.inline.byfilters import types_keyboard, genres_keyboard, rating_keyboard
from keyboards.inline.common import amount_keyboard, pagination_keyboard
from loader import bot
from parsers.common import parse_year_range
from states.search_film_byfilters import SearchFilmByFiltersState
from utils.senders import send_movie_message


@bot.message_handler(commands=['byfilters'])
def by_filters(message: Message) -> None:
    """
    Handles the '/byfilters' command and initiates the process of searching films by filters.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    bot.delete_state(message.from_user.id)
    bot.set_state(message.from_user.id, SearchFilmByFiltersState.type)
    movies_api = MoviesApi(config.API_KEY, config.API_HOST)
    bot.send_message(message.chat.id,
                     text=f'{message.from_user.first_name}, что хотите найти:',
                     reply_markup=types_keyboard(movies_api.get_types()))


@bot.callback_query_handler(func=None, query=movie_type_factory.filter())
def movie_type_handler(query: CallbackQuery) -> None:
    """
    Handles the user selection for the movie type.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    callback_data = movie_type_factory.parse(query.data)
    bot.set_state(query.from_user.id, SearchFilmByFiltersState.genre)
    with bot.retrieve_data(query.from_user.id) as data:
        data['display_type'] = callback_data['display']
        if callback_data['value'] == 'any':
            data['type'] = None
        else:
            data['type'] = callback_data['value']

    bot.edit_message_text(f'Выбранный тип - {callback_data["display"]}. Отличный выбор!',
                          query.message.chat.id,
                          query.message.id)
    movies_api = MoviesApi(config.API_KEY, config.API_HOST)
    bot.send_message(query.message.chat.id,
                     text=f'Выберите жанр: ',
                     reply_markup=genres_keyboard(movies_api.get_genres()))


@bot.callback_query_handler(func=None, query=movie_genre_factory.filter())
def movie_genre_handler(query: CallbackQuery) -> None:
    """
    Handles the user selection for the movie genre.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    callback_data = movie_genre_factory.parse(query.data)
    bot.set_state(query.from_user.id, SearchFilmByFiltersState.rating)
    with bot.retrieve_data(query.from_user.id) as data:
        data['display_genre'] = callback_data['display']
        if callback_data['value'] == 'any':
            data['genre'] = None
        else:
            data['genre'] = callback_data['value']
    bot.edit_message_text(f'Выбранный жанр - {callback_data["display"]}', query.message.chat.id, query.message.id)
    bot.send_message(query.message.chat.id,
                     text=f'Теперь укажите минимальный желаемый рейтинг',
                     reply_markup=rating_keyboard(is_minimum_input=True))


@bot.callback_query_handler(func=None, query=movie_rating_factory.filter())
def movie_rating_handler(query: CallbackQuery) -> None:
    """
    Handles the user selection for the movie rating.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    next_state = False
    callback_data = movie_rating_factory.parse(query.data)

    min_, max_ = 1, 10
    with bot.retrieve_data(query.from_user.id) as data:
        if callback_data['value'] == 'any':
            data['rating'] = (1, 10)
            next_state = True
        elif 'rating' in data:
            data['rating'] += (int(callback_data['value']), )
            min_, max_ = data['rating']
            next_state = True
        else:
            data['rating'] = (int(callback_data['value']), )
            min_, = data['rating']

    if next_state:
        bot.set_state(query.from_user.id, SearchFilmByFiltersState.year)

        bot.edit_message_text(f'Выбранный рейтинг: {min_}-{max_}', query.message.chat.id, query.message.id)
        bot.send_message(query.message.chat.id,
                         text=f'Теперь введите желаемый диапазон лет через "пробел".\nПример: 2010 2020')
    else:
        bot.edit_message_text(f'Вы выбрали минимальный рейтинг - {min_}. Теперь укажите максимальный: ',
                              query.message.chat.id,
                              query.message.id,
                              reply_markup=rating_keyboard(min_+1))


@bot.message_handler(state=SearchFilmByFiltersState.year)
def movie_year_handler(message: Message) -> None:
    """
    Handles the user input for the movie year.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    result, error = parse_year_range(message.text)
    if error:
        bot.send_message(message.chat.id, error)
        return
    bot.set_state(message.from_user.id, SearchFilmByFiltersState.amount)
    with bot.retrieve_data(message.from_user.id) as data:
        data['year'] = result
    bot.send_message(message.chat.id,
                     text=f'Сколько фильмов показать?',
                     reply_markup=amount_keyboard())


@bot.callback_query_handler(func=None, query=movie_amount_factory.filter())
def movie_amount_handler(query: CallbackQuery) -> None:
    """
    Handles the user selection for the number of movies to display.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    callback_data = movie_amount_factory.parse(query.data)
    bot.set_state(query.from_user.id, SearchFilmByFiltersState.pagination)
    with bot.retrieve_data(query.from_user.id) as data:
        data['amount'] = int(callback_data['value'])
        data['page'] = 0
        data['request'] = save_byfilters_request(user_id=query.from_user.id,
                                                 type=data['display_type'],
                                                 genre=data['display_genre'],
                                                 years=data['year'],
                                                 ratings=data['rating'],
                                                 amount=data['amount'])
    pagination_next(query)


@bot.callback_query_handler(func=None, query=movie_pagination_factory.filter(value='next'))
def pagination_next(query: CallbackQuery) -> None:
    """
    Handles the pagination for displaying the next page of movies.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    delete_state = False
    bot.delete_message(query.message.chat.id, query.message.id)
    with bot.retrieve_data(query.from_user.id) as data:
        data['page'] += 1
        movies_api = MoviesApi(config.API_KEY, config.API_HOST)
        response = movies_api.byfilters(
            data['type'],
            data['genre'],
            data['rating'],
            data['year'],
            data['amount'],
            data['page'],
        )
        save_movies(response.movies, data['request'])
        if not response.movies:
            bot.send_message(query.message.chat.id,
                             text=f'Ничего не нашлось. Попробуйте изменить запрос.')
        else:
            for movie in response.movies:
                send_movie_message(query.message.chat.id, movie)
                time.sleep(0.3)

        if response.total_pages <= response.current_page:
            delete_state = True
        else:
            bot.send_message(query.message.chat.id,
                             text='Нажмите "Далее", чтобы найти ещё фильмы по вашему запросу.'
                                  'Нажмите "Хватит", чтобы остановить поиск',
                             reply_markup=pagination_keyboard())

    if delete_state:
        bot.delete_state(query.from_user.id)
        if response.total_pages != 0:
            bot.delete_message(query.message.chat.id, query.message.id)
            bot.send_message(query.message.chat.id, f'По данному запросу больше ничего нет')


@bot.callback_query_handler(func=None, query=movie_pagination_factory.filter(value='stop'))
def pagination_stop(query: CallbackQuery) -> None:
    """
    Handles the user input to stop the pagination and search process.

    Args:
        query (CallbackQuery): The callback query object received by the bot.

    Returns:
        None
    """
    bot.delete_state(query.from_user.id)
    bot.edit_message_text(f'Хорошо, можете попробовать другой запрос', query.message.chat.id, query.message.id)

