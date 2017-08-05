import telegram
from telegram.ext import Updater

from settings import telegram_token

bot = telegram.Bot(token=telegram_token)
updater = Updater(token=telegram_token)

print(bot.get_me())
