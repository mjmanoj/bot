"""
main runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
import constants
import rex
import twit
import logician
import time
from operator import itemgetter
from helpers import get_time_now
import db
import config
from datetime import datetime
from bot import send_hot_tweets


# call hot shots on market symbols
def moon_call():
    print("Starting moon_call...")
    symbols = rex.get_market_summaries()
    scores = []

    print("Searching Twitter for BTRX symbol high volume list...")
    # get and score relevant tweets per symbol.
    for symbol in symbols:
        entry = {}
        entry["created"] = get_time_now().strftime('%s')
        coin_symbol = "$" + symbol
        entry["symbol"] = symbol

        # search twitter
        tweets = twit.search(coin_symbol)
        relevant_tweets = logician.strip_irrelevant(tweets)
        if len(relevant_tweets) == 0:
            continue

        score = logician.judge(relevant_tweets)
        if score == 0:
            continue

        entry["score"] = int(score)
        db.add(path="symbols", file_name=coin_symbol, entry=entry)
        scores.append(entry)

    print("Symbols analyzed, tracking periphreals...")
    # track_periphreals()

    # sort and find hottest trends
    sorted_scores = sorted(scores, key=itemgetter("score"), reverse=True)
    hot = sorted_scores[:5]

    print("Preparing hot five message...")

    # prepare message for telegram
    send_hot_tweets(hot)
    print("moon call complete, message sent.")
    print("sleeping now for 30 minutes...\n\n")


# tracks peripheral data
# - twitter trending per main tech countries
def track_periphreals():
    for country in constants.HOT_COUNTRIES:
        twit.get_trends_for_woeid(country)
        # logician judge this.
        # write this to database


moon_call()
