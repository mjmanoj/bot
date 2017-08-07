"""
main runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
import constants
import rex
import twitter
import logician
import db
import config
from telegram import bot
from helpers import set_interval


# call hot shots on market symbols
def moon_call():
    symbols = rex.get_market_symbols()
    scores = {}

    # get and score relevant tweets per symbol.
    for symbol in symbols:
        modified = "$" + symbol
        tweets = twitter.search(modified)
        relevant_tweets = logician.strip_irrelevant(tweets)
        score = logician.judge(relevant_tweets)
        db.add(modified, score)
        scores[modified] = score

    get_peripherals()

    # sort and find hottest trends
    sorted_scores = sorted(scores.items(), key=lambda x: x[1])
    hot_five = {k: sorted_scores[k] for k in sorted_scores.keys()[:5]}

    # prepare message for telegram
    message = "<h1>Hot Coin Ratings</h1>"
    message += "<ul>"

    for symbol in hot_five:
        message += "<li>" + symbol + " score: " + hot_five[symbol] + "</li>"

    message += "</ul>"
    message += "<p>Like this message? BTC tips @ <code>" + \
        config.tip_jar + "</code> are welcome!</p>"

    # send telegram message to moon room channel
    bot.send_message(chat_id=config.telegram_chat,
                     text=message, parse_mode="HTML")


# gets peripheral data
# - twitter trending per main tech countries
def get_peripherals():
    for country in constants.HOT_COUNTRIES:
        twitter.get_trends_for_woeid(country)
        # logician judge this.
        # write this to database


set_interval(moon_call, constants.DEFAULT_MINS)
