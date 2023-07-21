from core.mappers import dict_to_movie, dict_to_movie_byname
from core.models import Movie, MovieCountPages
import requests


class MoviesApi:
    """A class used to interact with a movie database API.

        ...

        Attributes
        ----------
        key : str
            The API key used to authenticate requests to the movie database API.
        host : str
            The host address of the movie database API.

        Methods
        -------
        byid(id_: int) -> Movie
            Fetches a movie by its ID from the movie database API.
        random() -> Movie
            Fetches a random movie from the movie database API.
        byname(page: int, amount: int, query: str) -> MovieCountPages
            Searches for movies by name and returns a paginated response.
        byfilters(
        type_: str,
        genre: str,
        rating_kp:
        tuple[int, int],
        year: tuple[int, int],
        amount: int,
        page: int
        ) -> MovieCountPages
            Fetches movies by applying multiple filters and returns a paginated response.
        """
    def __init__(self, key: str, host: str):
        """
        Parameters
        ----------
        key : str
            The API key used to authenticate requests to the movie database API.
        host : str
            The host address of the movie database API.
        """
        self.key = key
        self.host = host

    @property
    def headers(self) -> dict:
        """Generates the headers to be used in the API requests.

        Returns
        -------
        dict
            The headers dictionary.
        """
        return {'X-API-KEY': self.key}

    def byid(self, id_: int) -> Movie:
        """Fetches a movie by its ID from the movie database API.

        Parameters
        ----------
        id_ : int
            The ID of the movie.

        Returns
        -------
        Movie
            The movie object.
        """
        url = f'https://{self.host}/v1.3/movie/{id_}'
        response = requests.get(url, headers=self.headers)
        return dict_to_movie(response.json())

    def random(self) -> Movie:
        """Fetches a random movie from the movie database API.

        Returns
        -------
        Movie
            The movie object.
        """
        url = f'https://{self.host}/v1.3/movie/random'
        response = requests.get(url, headers=self.headers)
        return dict_to_movie(response.json())

    def byname(self, page: int, amount: int, query: str) -> MovieCountPages:
        """Searches for movies by name and returns a paginated response.

        Parameters
        ----------
        page : int
            The page number.
        amount : int
            The number of movies per page.
        query : str
            The name or part of the name of the movie.

        Returns
        -------
        MovieCountPages
            The paginated response containing the movies.
        """
        url = f'https://{self.host}/v1.2/movie/search'
        response = requests.get(url, params={
            'page': page,
            'limit': amount,
            'query': query
        }, headers=self.headers)
        movies = response.json()

        return MovieCountPages(
            current_page=movies['page'],
            total_pages=movies['pages'],
            total_movies=movies['total'],
            movies=[dict_to_movie_byname(movie) for movie in movies['docs']]
        )

    def byfilters(self,
                  type_: str,
                  genre: str,
                  rating_kp: tuple[int, int],
                  year: tuple[int, int],
                  amount: int,
                  page: int) -> MovieCountPages:
        """Fetches movies by applying multiple filters and returns a paginated response.

        Parameters
        ----------
        type_ : str
            The type of the movie (e.g. "movie", "series").
        genre : str
            The genre of the movie.
        rating_kp : tuple[int, int]
            The Kinopoisk rating range.
        year : tuple[int, int]
            The release year range.
        amount : int
            The number of movies per page.
        page : int
            The page number.

        Returns
        -------
        MovieCountPages
            The paginated response containing the movies.
        """
        url = f'https://{self.host}/v1.3/movie'
        response = requests.get(url, params={
            'page': page,
            'limit': amount,
            'type': type_,
            'genres.name': genre,
            'rating.kp': f'{rating_kp[0]}-{rating_kp[1]}',
            'year': f'{year[0]}-{year[1]}'
        }, headers=self.headers)
        movies = response.json()

        return MovieCountPages(
            current_page=movies['page'],
            total_pages=movies['pages'],
            total_movies=movies['total'],
            movies=[dict_to_movie(movie) for movie in movies['docs']]
        )

    def get_types(self) -> list[str]:
        """
        This method retrieves all possible movie types from the API.

        Returns:
            list[str]: A list of strings representing all possible movie types.
        """
        return self.__get_values_by_field('type')

    def get_genres(self) -> list[str]:
        """
        This method retrieves all possible movie genres from the API.

        Returns:
            list[str]: A list of strings representing all possible movie genres.
        """
        return self.__get_values_by_field('genres.name')

    def __get_values_by_field(self, field: str) -> list[str]:
        """
        This private method retrieves all possible values for a given field from the API.

        Args:
            field (str): The field for which to retrieve possible values.

        Returns:
            list[str]: A list of strings representing all possible values for the given field.
        """
        url = f'https://{self.host}/v1/movie/possible-values-by-field'
        response = requests.get(url, params={
            'field': field,
        }, headers=self.headers)
        return [g['name'] for g in response.json()]
