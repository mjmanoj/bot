""" the bot package servers as a telegram adapter """
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, env
TELLIE = telegram.Bot(token=telegram_token)


def send_message(text):
    """ send_message sends a text message to the environment variable chat id, in markdown """

    chat_id = telegram_chat_prod
    if env == "test":
        chat_id = telegram_chat_dev

    TELLIE.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")


def build_rating_template(scores, title):
    """ build_rating_template builds and returns a text message for twitter based coin score ratings """

    message = emoji.emojize("*:bird:" + title + ":bird: *\n")
    for market in scores:
        symbol = market["symbol"]

        # TODO: sentiment analysis
        # - ensure length is minus one to account for negative symbol
        # - if negative use skulls.
        birds = len(str(market["score"]))
        lit_meter = ""

        for _ in range(birds):
            lit_meter += emoji.emojize(":bird:")

        message += "- [$" + symbol + \
            lit_meter + \
            "](https://twitter.com/search?f=tweets&vertical=default&q=%24" + symbol + ")\n"

    return message
