from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from core.models import Movie as __Movie


@dataclass(frozen=True)
class Movie:
    """
    Represents a movie.

    Args:
        id_kp (int): The ID of the movie in Kinopoisk database.
        title (str): The title of the movie.

    Example:
        movie = Movie(id_kp=123, title="Movie Title")
    """
    id_kp: int
    title: str

    @classmethod
    def get_full_title(cls, original, alternative):
        """
        Generates the full title of the movie by combining the original and alternative titles.

        Args:
            original (str): The original title of the movie.
            alternative (str): The alternative title of the movie.

        Returns:
            str: The full title of the movie.

        Example:
            full_title = Movie.get_full_title("Original Title", "Alternative Title")
        """
        if alternative:
            original += f' ({alternative})'
        return original

    def __str__(self):
        """
        Returns a string representation of the movie.

        Returns:
            str: The string representation of the movie.

        Example:
            string_representation = str(movie)
        """
        return self.title


@dataclass(frozen=True)
class Request:
    """
    Represents a request for movie information.

    Args:
        created_at (datetime): The date and time when the request was created.
        movies (list[Movie]): The list of movies related to the request.

    Attributes:
        DTFORMAT (ClassVar[str]): The date and time format used for formatting the created_at attribute.

    Example:
        request = Request(created_at=datetime.now(), movies=[Movie(id_kp=123, title="Movie Title")])
    """
    created_at: datetime
    movies: list[Movie]
    DTFORMAT: ClassVar[str] = '%d.%m.%Y %H:%M'

    def to_html(self) -> str:
        """
        Converts the request information to an HTML format.

        Returns:
            str: The HTML representation of the request.

        Example:
            html_representation = request.to_html()
        """
        pass


@dataclass(frozen=True)
class RequestByFilter(Request):
    """
    Represents a request for movie information with filters.

    Args:
        type (str): The type of movie.
        genre (str): The genre of movie.
        year_min (int): The minimum year of release.
        year_max (int): The maximum year of release.
        rating_min (int): The minimum rating on KinoPoisk.
        rating_max (int): The maximum rating on KinoPoisk.

    Example:
        request = RequestByFilter(created_at=datetime.now(), movies=[Movie(id_kp=123, title="Movie Title")],
                                 type="Action", genre="Thriller", year_min=2000, year_max=2020,
                                 rating_min=6, rating_max=9)
    """
    type: str
    genre: str
    year_min: int
    year_max: int
    rating_min: int
    rating_max: int

    def to_html(self) -> str:
        """
        Converts the request with filters information to an HTML format.

        Returns:
            str: The HTML representation of the request with filters.

        Example:
            html_representation = request.to_html()
        """
        date = self.created_at.strftime(self.DTFORMAT)
        last_movies = 'Последние найденные фильмы:' if self.movies else 'По этому запросу нет фильмов'
        return '\n'.join((f'<b>Поиск c фильтрами</b> - /byfilters (<i>{date}</i>):',
                          f'<b>Тип:</b> <i>{self.type}</i>',
                          f'<b>Жанр:</b> <i>{self.genre}</i>',
                          f'<b>Год выхода:</b> <i>{self.year_min}-{self.year_max}</i>',
                          f'<b>Рейтинг Кинопоиска:</b> <i>{self.rating_min}-{self.rating_max}</i>',
                          last_movies))


@dataclass(frozen=True)
class RequestByName(Request):
    """
    Represents a request for movie information by name.

    Args:
        title (str): The title of the movie.

    Example:
        request = RequestByName(created_at=datetime.now(), movies=[Movie(id_kp=123, title="Movie Title")],
                                title="Movie Title")
    """
    title: str

    def to_html(self) -> str:
        """
        Converts the request by name information to an HTML format.

        Returns:
            str: The HTML representation of the request by name.

        Example:
            html_representation = request.to_html()
        """
        date = self.created_at.strftime(self.DTFORMAT)
        last_movies = 'Последние найденные фильмы:' if self.movies else 'По этому запросу нет фильмов\n'
        return '\n'.join((f'<b>Поиск по названию</b> - /byname (<i>{date}</i>):',
                          f'<b>Название:</b> <i>{self.title}</i>',
                          last_movies))


@dataclass(frozen=True)
class RequestRandom(Request):
    """
    Represents a request for a random movie.

    Example:
        request = RequestRandom(created_at=datetime.now(), movies=[Movie(id_kp=123, title="Movie Title")])
    """
    def to_html(self) -> str:
        """
        Converts the request for a random movie information to an HTML format.

        Returns:
            str: The HTML representation of the request for a random movie.

        Example:
            html_representation = request.to_html()
        """
        date = self.created_at.strftime(self.DTFORMAT)
        return f'<b>Случайный фильм</b> - /random (<i>{date}</i>):'


def movie_to_html(movie: __Movie) -> str:
    """
    Converts a Movie object to an HTML format.

    Args:
        movie (__Movie): The movie object to be converted.

    Returns:
        str: The HTML representation of the movie.

    Example:
        html_representation = movie_to_html(movie)
    """
    alt_title = f'({movie.alternative_title})' if movie.alternative_title else ''
    rating_kp = movie.rating_kp if movie.rating_kp else 'нет оценки'
    rating_imdb = movie.rating_imdb if movie.rating_imdb else 'нет оценки'
    description = f'\n{movie.description}' if movie.description else 'отсутствует'
    if len(description) > 800:
        description = description[:797] + '...'

    return '\n'.join([
        f'<a href="{movie.url}"><b>{movie.original_title}</b> {alt_title}</a>',
        '',
        f'<b>Год выхода:</b> <i>{movie.year}</i>',
        f'<b>Рейтинг Кинопоиска/IMDB:</b> <i>{rating_kp} / {rating_imdb}</i>',
        f'<b>Жанр(ы):</b> <i>{", ".join(movie.genres)}</i>',
        '',
        f'<b>Описание:</b> <i>{description}</i>'
    ])
