import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('random', 'Вывести случайный фильм'),
    ('byname', 'Поиск фильма по названию'),
    ('byfilters', 'Поиск фильма с фильтрами'),
    ('history', 'История поисковых запросов')
)
