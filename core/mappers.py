from core.models import Movie


def dict_to_movie(raw_movie: dict) -> Movie:
    """Returns an instance of the Movie class with the necessary parameters

    This function extracts various movie details from the input dictionary,
    including the title, alternative title, id, year, ratings from Kinopoisk and IMDb,
    genres, description, and poster URL.
    It then creates and returns a Movie object with these details.
    Args:
        raw_movie: dict
            Raw movie information from the api

    Returns:
    -------
    Movie
        The movie object.

    """
    title = raw_movie['name']
    alt_title = raw_movie['alternativeName']
    id_ = raw_movie['id']
    year = raw_movie['year']
    rating_kp = raw_movie['rating']['kp']
    rating_imdb = raw_movie['rating']['imdb']
    genres = [g['name'] for g in raw_movie['genres']]
    description = raw_movie['description']
    poster_url = raw_movie['poster'] and raw_movie['poster']['previewUrl']

    return Movie(
        original_title=title,
        alternative_title=alt_title,
        id=id_,
        year=year,
        rating_kp=rating_kp,
        rating_imdb=rating_imdb,
        genres=genres,
        description=description,
        poster_url=poster_url
    )


def dict_to_movie_byname(raw_movie: dict) -> Movie:
    """Returns an instance of the Movie class with the necessary parameters

    This function extracts various movie details from the input dictionary,
    including the title, alternative title, id, year, ratings from Kinopoisk
    and sets the IMDb rating to 0, genres, description, and poster URL.
    It then creates and returns a Movie object with these details.

    Args:
        raw_movie: dict
            Raw movie information from the api

    Returns:
    -------
    Movie
        The movie object.

    """
    title = raw_movie['name']
    alt_title = raw_movie['alternativeName']
    id_ = raw_movie['id']
    year = raw_movie['year']
    rating_kp = raw_movie['rating']
    genres = raw_movie['genres']
    description = raw_movie['description']
    poster_url = raw_movie['poster']

    return Movie(
        original_title=title,
        alternative_title=alt_title,
        id=id_,
        year=year,
        rating_kp=rating_kp,
        rating_imdb=0,
        genres=genres,
        description=description,
        poster_url=poster_url
    )

