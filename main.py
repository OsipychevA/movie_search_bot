from database.helpers import initialize_db
from filters.callback_filter import CallbackFilter
from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter, IsDigitFilter

if __name__ == '__main__':
    initialize_db()

    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(IsDigitFilter())
    bot.add_custom_filter(CallbackFilter())
    set_default_commands(bot)

    bot.infinity_polling()

