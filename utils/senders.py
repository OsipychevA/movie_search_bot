from loader import bot
from core.models import Movie
from utils.presenters import movie_to_html


def send_movie_message(chat_id: int, movie: Movie) -> None:
    """
    Sends a movie message to the specified chat.

    Args:
        chat_id (int): The ID of the chat to send the message to.
        movie (Movie): The movie object to send.

    Returns:
        None

    Example:
        send_movie_message(chat_id=123456, movie=Movie(id_kp=123, title="Movie Title"))
    """
    no_poster = 'https://upload.wikimedia.org/wikipedia/commons/a/a1/Out_Of_Poster.jpg'
    poster_url = movie.poster_url if movie.poster_url else no_poster
    bot.send_photo(chat_id, poster_url, movie_to_html(movie), parse_mode='HTML')
