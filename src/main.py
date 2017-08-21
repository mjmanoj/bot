"""
the main package runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
import constants
import rex
from twit import search, get_trends_for_woeid
import logician
from operator import itemgetter
from archivist.operations import get_avg_api_res
from helpers import get_time_now
import db
from bot import build_rating_template


# call hot shots on market symbols
def moon_call():
    operations_log = {}
    operations_log["_init"] = get_time_now(stringify=True)

    print "[JOB] Starting moon_call at " + operations_log["_init"]

    symbols = rex.get_market_summaries()
    scores = []

    print "[JOB] Searching Twitter for BTRX symbol high volume list..."
    # get and score relevant tweets per symbol.
    operations_log["twitter_search_start"] = get_time_now(stringify=True)

    # get average response time for twitter to use as stale_break for logician
    # note, this is the average for ALL calls during the moon_call duration
    avg_res = get_avg_api_res()

    for symbol in symbols:
        entry = {}
        entry["created"] = get_time_now(stringify=True)
        entry["symbol"] = symbol

        coin_symbol = "$" + symbol

        # search twitter
        tweets = search(coin_symbol)
        relevant_tweets = logician.strip_irrelevant(
            tweets, stale_break=avg_res + 3600
        )

        # if empty, go to next symbol
        if not relevant_tweets:
            continue

        score = logician.judge(relevant_tweets)
        # if score sucks, go to next symbol
        if not score:
            continue

        entry["score"] = int(score / 2)
        db.add(path="symbols", file_name=coin_symbol, entry=entry)
        scores.append(entry)

    operations_log["twitter_search_end"] = get_time_now(stringify=True)
    print "[JOB] Symbols analyzed, tracking periphreals..."

    operations_log["track_periphreals_start"] = get_time_now(stringify=True)
    track_periphreals()
    operations_log["track_periphreals_end"] = get_time_now(stringify=True)

    # sort and find hottest trends
    sorted_scores = sorted(scores, key=itemgetter("score"), reverse=True)
    hot_hourly = sorted_scores[:5]

    print "[JOB] Preparing message templates..."

    hot_daily = get_scores("daily")
    hot_weekly = get_scores("weekly")

    # prepare message for telegram
    operations_log["send_message_end"] = get_time_now(stringify=True)
    hot_hourly_text = build_rating_template(hot_hourly, "Hourly Twitter Hype")
    hot_daily_text = build_rating_template(hot_daily, "Daily Twitter Hype")
    hot_weekly_text = build_rating_template(hot_weekly, "Weekly Twitter Hype")
    operations_log["send_message_end"] = get_time_now(stringify=True)

    print "[JOB] Moon call complete, message sent at " + get_time_now(stringify=True)
    print "[JOB] Sleeping now for 30 minutes...\n\n"

    operations_log["_end"] = get_time_now(stringify=True)
    db.add(path="operations", file_name="moon_call", entry=operations_log)


# tracks peripheral data
# - twitter trending per main tech countries
# - TODO: planetary movements
def track_periphreals():
    for country in constants.HOT_COUNTRIES:
        res = get_trends_for_woeid(country)
        for trend in res:
            entry = {}
            entry["topic"] = trend.name
            db.add(path="twitter/trends", file_name=str(country), entry=entry)


moon_call()
