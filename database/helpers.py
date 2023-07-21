from database.models import database, Movie, Request


def initialize_db() -> None:
    """Initializes the database by creating required tables.

    Returns:
        None: This function doesn't return anything.
    """
    database.create_tables([Request, Movie])
