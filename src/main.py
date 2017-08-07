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
        coin_symbol = "$" + symbol

        # search twitter
        tweets = twitter.search(coin_symbol)
        relevant_tweets = logician.strip_irrelevant(tweets)
        if len(relevant_tweets) is None:
            print("No new updates for " + coin_symbol + " found.")
            continue

        score = logician.judge(relevant_tweets)
        db.add(coin_symbol, score)
        scores[coin_symbol] = score

    track_periphreals()

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


# tracks peripheral data
# - twitter trending per main tech countries
def track_periphreals():
    for country in constants.HOT_COUNTRIES:
        twitter.get_trends_for_woeid(country)
        # logician judge this.
        # write this to database


set_interval(moon_call, constants.DEFAULT_MINS)
