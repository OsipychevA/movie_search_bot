from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    """
    A class to respresent a movie.

    ...

    Attributes
    ----------
    id : str
        a string representing unique movie id
    original_title : str
        a string representing the original title of the movie
    year : int
        an integer representing the release year of the movie
    rating_kp : float
        a float representing the kinopoisk rating of the movie
    rating_imdb : float
        a float representing the IMDB rating of the movie
    genres : List[str]
        a list representing the genres of the movie
    description : str, optional
        a string representing the description of the movie
    poster_url : str, optional
        a string representing the URL of the movie poster
    alternative_title : str, optional
        a string representing the alternative title of the movie

    Methods
    -------
    def url():
        returns a string which is a URL to the movie's page on kinopoisk.ru
    """
    id: str
    original_title: str
    year: int
    rating_kp: float
    rating_imdb: float
    genres: list[str]
    description: Optional[str]
    poster_url: Optional[str]
    alternative_title: Optional[str]

    @property
    def url(self):
        """Property Method for create URL

        Returns
        -------
        str
            a string which is a URL to the movie's page on kinopoisk.ru

        """
        return f'https://www.kinopoisk.ru/film/{self.id}/'


@dataclass
class MovieCountPages:
    """
    A class to respresent a page of movies.

    ...

    Attributes
    ----------
    current_page : int
        an integer representing the current page number
    total_pages : int
        an integer representing the total number of pages
    total_movies : int
        an integer representing the total number of movies on all pages
    movies : List[Movie]
        a list containing the 'Movie' objects corresponding to that page
    """
    current_page: int
    total_pages: int
    total_movies: int
    movies: list[Movie]



