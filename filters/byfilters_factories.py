from telebot.callback_data import CallbackData

movie_type_factory = CallbackData('display', 'value', prefix='t')
movie_genre_factory = CallbackData('display', 'value', prefix='g')
movie_rating_factory = CallbackData('display', 'value', prefix='r')
movie_amount_factory = CallbackData('value', prefix='a')
movie_pagination_factory = CallbackData('value', prefix='p')
