#!/usr/bin/python
""" the bot package servers as a telegram adapter """
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, env, kirby_bot_channel, btc_tip_jar, rain_tip_jar
TELLIE = telegram.Bot(token=telegram_token)

PROD_CHANNELS = [telegram_chat_prod, kirby_bot_channel]
TEST_CHANNELS = [telegram_chat_dev]


def build_info_template():
    return open('./msg_temps/info.txt').read()


def build_ad_template():
    text = open('./msg_temps/ad.txt').read()
    return text % (btc_tip_jar, rain_tip_jar)


def generate_and_post_message(hourly, daily, weekly):
    """
    generates and posts a message using the build template and send message functions
    accepts hourly, daily, weekly scores
    - scores currently are expected to be of shape [{ symbol: string, score: int }]
    - scores will evolve to coins array => [{ symbol: string, scores: { medium: int }}]
    -- medium being "twitter", "reddit", "google", etc.
    """

    if not hourly and not daily and not weekly:
        print("[INFO] all scores were same as last posting, skipping")
        send_message("Scores remain same for twitter data in the last hour...")
        return

    text = ""

    if hourly:
        text += build_rating_template(hourly,
                                      "Twitter Hourly Scoreboard") + "\n"

    if daily:
        daily_text = build_rating_template(daily, "Twitter Daily Scoreboard")
        text += daily_text + "\n"

    if weekly:
        weekly_text = build_rating_template(
            weekly, "Twitter Weekly Scoreboard")
        text += weekly_text + "\n"

    print "DEBUG"
    print len(text)

    if text:
        send_message(text=text)


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

    message = emoji.emojize("*:bird:" + title + " :bird: *\n")
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

        message += "\nResearch on "

        if "name" in market:
            message += "[Coin Market Cap](https://coinmarketcap.com/currencies/" + \
                market["name"] + ")"

        message += ", Analyze on[Trading View](https://www.tradingview.com/chart/?symbol=BITTREX:" + \
            market["symbol"] + "BTC)"

        message += ", Trade on[Bittrex](https://bittrex.com/Market/Index?MarketName=BTC-" + \
            market["symbol"] + ")"

        message += ".\n"

    return message
