import time

from telebot.types import Message, ReplyKeyboardRemove

from database.functions import save_byname_request, save_movies
from loader import bot
from states.search_film_byname import SearchFilmState
from core.api import MoviesApi
from config_data import config
from utils.senders import send_movie_message
from keyboards.reply.common import pagination_keyboard


@bot.message_handler(commands=['byname'])
def byname(message: Message) -> None:
    """
    Handles the '/byname' command and initiates the process of searching films by name.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    bot.delete_state(message.from_user.id)
    bot.set_state(message.from_user.id, SearchFilmState.query)
    bot.send_message(message.from_user.id, f'{message.from_user.first_name}, введите название фильма для поиска:')


@bot.message_handler(state=SearchFilmState.query)
def get_query(message: Message) -> None:
    """
    Handles the user input for the film name query.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    bot.set_state(message.from_user.id, SearchFilmState.amount)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['query'] = message.text
    bot.send_message(message.from_user.id, f'{message.from_user.first_name}, сколько фильмов показать? (максимум 5) ')


@bot.message_handler(state=SearchFilmState.amount, is_digit=True)
def get_amount(message: Message) -> None:
    """
    Handles the user input for the amount of films to display.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    amount = int(message.text)
    if amount < 1 or amount > 5:
        bot.send_message(message.from_user.id, f'Можно ввести только число от 1 до 5\nПопробуйте ещё раз.')
        return
    bot.set_state(message.from_user.id, SearchFilmState.pagination)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['amount'] = amount
        data['page'] = 0
        data['request'] = save_byname_request(user_id=message.from_user.id,
                                              title=data['query'],
                                              amount=data['amount'])
    pagination_next(message)


@bot.message_handler(state=SearchFilmState.pagination, regexp='Далее')
def pagination_next(message: Message) -> None:
    """
    Handles the 'Далее' command to display the next page of search results.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    delete_state = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['page'] += 1
        movies_api = MoviesApi(config.API_KEY, config.API_HOST)
        response = movies_api.byname(data['page'], data['amount'], data['query'])
        save_movies(response.movies, data['request'])

        if not response.movies:
            bot.send_message(message.from_user.id,
                             f'Ничего не нашлось. Попробуйте изменить запрос.')
        else:
            for movie in response.movies:
                send_movie_message(message.chat.id, movie)
                time.sleep(0.3)
        if response.total_pages <= response.current_page:
            delete_state = True

    if delete_state:
        bot.delete_state(message.from_user.id)
        if response.total_pages != 0:
            bot.send_message(message.chat.id,
                             text='По данному запросу больше ничего нет',
                             reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         text='Чтобы найти ещё фильмы, нажмите "Далее" или '
                              'нажмите "Хватит", чтобы остановить поиск',
                         reply_markup=pagination_keyboard())


@bot.message_handler(state=SearchFilmState.pagination, regexp='Хватит')
def pagination_stop(message: Message) -> None:
    """
    Handles the 'Хватит' command to stop the pagination and search process.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    bot.delete_state(message.from_user.id)
    bot.send_message(message.chat.id,
                     text='Хорошо, можете попробовать другой запрос',
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=SearchFilmState.amount, is_digit=False)
def incorrect_amount(message: Message) -> None:
    """
    Handles incorrect input of amount and provides an error message.

    Args:
        message (Message): The message object received by the bot.

    Returns:
        None
    """
    bot.send_message(message.from_user.id,
                     text=f'Можно ввести только число от 1 до 5\nПопробуйте ещё раз.')
