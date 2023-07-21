from typing import Iterable

import core.models
import utils.presenters
from database.mappers import request_to_presenter, movie_to_presenter
from database.models import Request, Movie


def save_byfilters_request(user_id: int,
                           type: str,
                           genre: str,
                           years: tuple[int, int],
                           ratings: tuple[int, int],
                           amount: int) -> Request:
    """
    Creates a new Request in the database to search for a movie with filters

    Args:
       user_id (int): Unique identifier of the user.
       type (str): Type of movie.
       genre (str): Genre of the movie.
       years (tuple): Tuple with minimal and maximal year of movie.
       ratings (tuple): Tuple with minimal and maximal movie rating.
       amount (int): Amount of results user wants to get.

    Returns:
       Request: The created Request object.
    """
    return Request.create(user_id=user_id,
                          command='byfilters',
                          type=type,
                          genre=genre,
                          year_min=years[0],
                          year_max=years[1],
                          rating_min=ratings[0],
                          rating_max=ratings[1],
                          amount=amount)


def save_byname_request(user_id: int,
                        title: str,
                        amount: int) -> Request:
    """
    Creates a new Request in the database to find movie by name.

    Args:
        user_id (int): Unique identifier of the user.
        title (str): Title of the movie to find.
        amount (int): Amount of results user wants to get.

    Returns:
        Request: The created Request object.
    """
    return Request.create(user_id=user_id,
                          command='byname',
                          title=title,
                          amount=amount)


def save_random_request(user_id: int) -> Request:
    """
    Creates a new Request in the database for getting random movies.

    Args:
        user_id (int): Unique identifier of the user.

    Returns:
        Request: The created Request object.
    """
    return Request.create(user_id=user_id,
                          command='random')


def save_movies(movies: list[core.models.Movie],
                request: Request) -> Movie:
    """
    Saves a list of movies into the database with relation to a specific request.

    Args:
        movies (list): List of movie objects to save.
        request (Request): Request instance to which the movies related.

    Returns:
        list[Movie]: The list of created Movie objects.
    """
    return Movie.bulk_create([
        Movie(id_kp=movie.id,
              title=utils.presenters.Movie.get_full_title(movie.original_title, movie.alternative_title),
              request=request)
        for movie in movies
    ])


def get_history(user_id: int, amount: int) -> list[utils.presenters.Request]:
    """
    Retrieves a list of requests and their associated movies for a specific user.

    Args:
        user_id (int): Unique identifier of the user.
        amount (int): Amount of recent requests to get.

    Returns:
        list[Request]: A list of requests with related movies.
    """
    requests = __get_requests(user_id, amount)
    requests_movies = [
        [movie_to_presenter(movie) for movie in __request_movies(request)]
        for request in requests
    ]
    return [
        request_to_presenter(request, movies)
        for request, movies in zip(requests, requests_movies)
    ]


def __request_movies(request: Movie) -> Iterable[Movie]:
    """Retrieves the last page of movies from database associated with specific request.

     Args:
         request (Request): A Request instance for which to retrieve movies.

     Returns:
         Iterable[Movie]: A Iterable[Movie] of movies associated with the request.
     """
    return request.movies.order_by(Movie.id.desc()).limit(request.amount)


def __get_requests(user_id: int, amount: int) -> Iterable[Movie]:
    """
    Retrieves the requests made by a specific user.

    Args:
        user_id (int): An ID of the user for which to retrieve the requests.
        amount (int): The maximum number of requests to retrieve.

    Returns:
        Iterable[Request]: A Iterable[Request] of requests made by the user.
    """
    return Request.select().where(Request.user_id == user_id).order_by(Request.created_at.desc()).limit(
        amount)


