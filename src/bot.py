import telegram

from settings import telegram_token

bot = telegram.Bot(token=telegram_token)

print(bot.get_me())
