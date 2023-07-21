from datetime import datetime

from peewee import Model, DateTimeField, SqliteDatabase, ForeignKeyField
from peewee import IntegerField, TextField


database = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    """
    Base model class for all models.

    Attributes:
        Meta:
            database (SqliteDatabase): The database connection.
    """
    class Meta:
        database = database


class Request(BaseModel):
    """
    Represents a request made by a user.

    Attributes:
        user_id (int): The ID of the user making the request.
        command (str): The command type of the request.
        title (str, optional): The title for the request (default is None).
        type (str, optional): The type of the movie for the request (default is None).
        genre (str, optional): The genre of the movie for the request (default is None).
        year_min (int, optional): The minimum year of the movie for the request (default is None).
        year_max (int, optional): The maximum year of the movie for the request (default is None).
        rating_min (int, optional): The minimum rating of the movie for the request (default is None).
        rating_max (int, optional): The maximum rating of the movie for the request (default is None).
        amount (int, default=1): The number of movies to request (default is 1).
        created_at (datetime, default=datetime.now): The date and time when the request was created.
    """
    user_id = IntegerField()
    command = TextField()
    title = TextField(null=True)
    type = TextField(null=True)
    genre = TextField(null=True)
    year_min = IntegerField(null=True)
    year_max = IntegerField(null=True)
    rating_min = IntegerField(null=True)
    rating_max = IntegerField(null=True)
    amount = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.now)


class Movie(BaseModel):
    """
    Represents a movie.

    Attributes:
        id_kp (int): The ID of the movie.
        title (str): The title of the movie.
        request (Request): The request associated with the movie.
    """
    id_kp = IntegerField()
    title = TextField()
    request = ForeignKeyField(Request, backref='movies')
