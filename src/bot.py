"""
moonbot is a telegram adapter
"""
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, tip_jar, env

bot = telegram.Bot(token=telegram_token)


def send_message(text):
    chat_id = telegram_chat_prod
    if ev == "TEST":
        chat_id = telegram_chat_dev

    bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")


def send_hot_tweets(hot_tweets):
    message = emoji.emojize("*:fire: Hot Coins of Twitter :fire: *\n")
    message += "_Analysis of credible #crypto tweets for BTRX coins for last 30 minutes._\n\n"

    for market in hot_tweets:
        symbol = market["symbol"]

        fires = len(str(market["score"]))
        lit_meter = ""

        for _ in range(fires):
            lit_meter += emoji.emojize(":fire:")

        message += "- [$" + symbol + " is " + \
            lit_meter + "](https://twitter.com/search?q=%24" + symbol + ")\n"

    message += "\nSupport development with BTC Tips @ `" + tip_jar + "`"

    send_message(text=message)
