""" the bot package servers as a telegram adapter """
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, env, kirby_bot_channel
TELLIE = telegram.Bot(token=telegram_token)

PROD_CHANNELS = [telegram_chat_prod, kirby_bot_channel]
TEST_CHANNELS = [telegram_chat_dev]


def send_message(text):
    """ send_message sends a text message to the environment variable chat id, in markdown """

    channels = PROD_CHANNELS

    if env == "test":
        channels = TEST_CHANNELS

    for channel in channels:
        TELLIE.send_message(chat_id=channel, text=text,
                            parse_mode="Markdown", disable_web_page_preview=True)


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
            "](https://twitter.com/search?f=tweets&vertical=default&q=%24" + \
            symbol + ") Score => " + lit_meter

        if "name" in market:
            message += " ::: [Research](https://coinmarketcap.com/currencies/" + \
                market["name"] + ")"

        message += " | [Analyize](https://www.tradingview.com/chart/?symbol=BITTREX:" + \
            market["symbol"] + "BTC)"

        message += " | [Trade](https://bittrex.com/Market/Index?MarketName=BTC-" + \
            market["symbol"] + ")"

        message += "\n"

    return message
