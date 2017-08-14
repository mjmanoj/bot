"""
moonbot is a telegram adapter
"""
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, tip_jar, env

bot = telegram.Bot(token=telegram_token)


def send_message(text):
    chat_id = telegram_chat_prod
    if env == "test":
        chat_id = telegram_chat_dev

    bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")


def send_hot_tweets(hot_tweets):
    message = "_Analysis of credible #crypto social media for BTRX coins from the last 30 minutes._\n"
    message += "_Disclaimer: These tweets are for RESERACH. Some are about dying coins, some about ones thriving with life! Make wise decisions on your own judgement._\n\n"

    message += emoji.emojize("*:bird: Twitter Hype Coins :bird: *\n")
    for market in hot_tweets:
        symbol = market["symbol"]

        # TODO: sentiment analysis
        # - ensure length is minus one to account for negative symbol
        # - if negative use skulls.
        birds = len(str(market["score"]))
        lit_meter = ""

        for _ in range(birds):
            lit_meter += emoji.emojize(":bird:")

        message += "- [$" + symbol + " is " + \
            lit_meter + \
            "](https://twitter.com/search?f=tweets&vertical=default&q=%24" + symbol + ")\n"

    message += "\nSupport development with BTC Tips @ `" + tip_jar + "`"

    send_message(text=message)
