# Телеграм-бот для поиска фильмов и сериалов
Этот телеграм-бот позволяет быстро находить информацию о фильмах по заданным параметрам используя [api.kinopoisk.dev](https://kinopoisk.dev/)

## Возможности бота

### Основные команды

* `/start` — запуск бота
* `/help` — помощь по командам бота
* `/random` — поиск случайного фильма
* `/byname` — поиск фильмов по названию
* `/byfilters` — поиск фильмов и сериалов, наиболее подходящих по жанру, рейтингу и дипапзону лет
* `/history` — вывод истории поиска фильмов

### Дополнительные возможности

* Все данные, введенные пользователем, проверяются на корректность.

## Быстрый старт

### Создание Telegram бота

1. Найти в телеграме бота [@BotFather](https://t.me/BotFather)
2. Выбрать команду `/newbot` в меню бота
3. Придумайте и напишите название вашего бота
4. Придумайте и напишите username, который заканчивается на 'bot'
5. Скопируйте и сохраните токен (ключ). Он понадобится в дальнейшем.
6. Также в сообщении есть ссылка, по которой вы можете сразу перейти к боту

### Установка (Windows)

1. Склонировать репозиторий
2. Создать файл .env со следующим содержимым(используйте шаблон .env.template):

    ```shell
    BOT_TOKEN = 'токен для бота, полученный от @BotFather'
    API_KEY = 'ключ API полученный от бота @kinopoiskdev_bot'
    API_HOST = 'api.kinopoisk.dev'
    ```

3. Создать виртуальное окружение с помощью команды в терминале: `python -m venv venv`
4. Активировать виртуальное окружение: `./venv/scripts/activate`
5. Установить зависимости: `pip install -r requirements.txt`
6. Запустить: `python main.py`