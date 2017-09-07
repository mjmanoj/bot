#!/usr/bin/python
""" the bot package servers as a telegram adapter """
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, env, kirby_bot_channel, btc_tip_jar, ltc_tip_jar, rain_tip_jar
TELLIE = telegram.Bot(token=telegram_token)

PROD_CHANNELS = [telegram_chat_prod, kirby_bot_channel]
TEST_CHANNELS = [telegram_chat_dev]


def generate_and_post_message(hourly, daily, weekly):
    """
    generates and posts a message using the build template and send message functions
    accepts hourly, daily, weekly scores
    - scores currently are expected to be of shape [{ symbol: string, score: int }]
    - scores will evolve to coins array => [{ symbol: string, scores: { medium: int }}]
    -- medium being "twitter", "reddit", "google", etc.
    """
    hourly_text = build_rating_template(hourly, "Hourly Twitter Hype")
    daily_text = build_rating_template(daily, "Daily Twitter Hype")
    weekly_text = build_rating_template(weekly, "Weekly Twitter Hype")

    pray_symbol = emoji.emojize(":folded_hands:")
    moon_symbol = emoji.emojize(":full_moon:")
    crystal_ball_symbol = emoji.emojize(":crystal_ball:")

    message_text = moon_symbol + " MOON ROOM HOURLY REPORT " + moon_symbol + "\n"
    message_text += "_Analysis of credible #crypto social media for BTRX coins._\n"
    message_text += "Please read the USER GUIDE at bit.ly/2vFCM5W for bot trading pro tips. Always DYOR!\n"
    message_text += "Check the roadmap and other goodies on the main site at bit.ly/2wmfMLz \n\n"
    message_text += hourly_text + "\n" + daily_text + "\n" + weekly_text
    message_text += emoji.emojize(
        "\n" + pray_symbol + " This bot takes effort to tune and develop. Badass features incoming! If you're making good profit, a 2.5% cut is recommended for development continuation. " + pray_symbol + "\n")
    message_text += "BTC: `" + btc_tip_jar + "`\n"
    message_text += "RAIN: `" + rain_tip_jar + "`\n"
    message_text += crystal_ball_symbol + \
        " Questions, tips, feedback, need a programmer? write @azurikai, will make your dreams come true " + \
        crystal_ball_symbol + "\n"

    send_message(text=message_text)


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

        message += " | [Analyze](https://www.tradingview.com/chart/?symbol=BITTREX:" + \
            market["symbol"] + "BTC)"

        message += " | [Trade](https://bittrex.com/Market/Index?MarketName=BTC-" + \
            market["symbol"] + ")"

        message += "\n"

    return message
