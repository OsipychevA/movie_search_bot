import database.models
import utils.presenters


def movie_to_presenter(movie: database.models.Movie) -> utils.presenters.Movie:
    """
    Converts a Movie database model to a Movie presenter.

    Args:
        movie (database.models.Movie): The Movie model to be converted.

    Returns:
        utils.presenters.Movie: The converted Movie presenter.
    """
    return utils.presenters.Movie(movie.id_kp, movie.title)


def request_to_presenter(request: database.models.Request,
                         movies: list[utils.presenters.Movie]) -> utils.presenters.Request:
    """
    Converts a Request model to a Request presenter based on the command type.

    Args:
        request (database.models.Request): The Request model to be converted.
        movies (list[utils.presenters.Movie]): A list of Movie presenters.

    Returns:
        utils.presenters.Request: The converted Request presenter.
    """
    mappers = {
        'random': __request_random_to_presenter,
        'byfilters': __request_by_filters_to_presenter,
        'byname': __request_by_name_to_presenter,
    }

    return mappers[request.command](request, movies)


def __request_random_to_presenter(request: database.models.Request,
                                  movies: list[utils.presenters.Movie]) -> utils.presenters.RequestRandom:
    """
    Converts a Request model to a RequestRandom presenter.

    Args:
        request (database.models.Request): The Request model to be converted.
        movies (list[utils.presenters.Movie]): A list of Movie presenters.

    Returns:
        utils.presenters.RequestRandom: The converted RequestRandom presenter.
    """
    return utils.presenters.RequestRandom(request.created_at,
                                          movies)


def __request_by_filters_to_presenter(request: database.models.Request,
                                      movies: list[utils.presenters.Movie]) -> utils.presenters.RequestByFilter:
    """
    Converts a Request model to a RequestByFilter presenter.

    Args:
        request (database.models.Request): The Request model to be converted.
        movies (list[utils.presenters.Movie]): A list of Movie presenters.

    Returns:
        utils.presenters.RequestByFilter: The converted RequestByFilter presenter.
    """
    return utils.presenters.RequestByFilter(request.created_at,
                                            movies,
                                            request.type,
                                            request.genre,
                                            request.year_min,
                                            request.year_max,
                                            request.rating_min,
                                            request.rating_max)


def __request_by_name_to_presenter(request: database.models.Request,
                                   movies: list[utils.presenters.Movie]) -> utils.presenters.RequestByName:
    """
    Converts a Request model to a RequestByName presenter.

    Args:
        request (database.models.Request): The Request model to be converted.
        movies (list[utils.presenters.Movie]): A list of Movie presenters.

    Returns:
        utils.presenters.RequestByName: The converted RequestByName presenter.
    """
    return utils.presenters.RequestByName(request.created_at,
                                          movies,
                                          request.title)
