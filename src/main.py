"""
the main package runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
from operator import itemgetter

import db
from config import env, tip_jar
from archivist import get_moon_call_res_duration, get_score_history
from twit import search, get_trends_for_woeid
from helpers import get_time_now
from bot import build_rating_template, send_message
from constants import HOT_COUNTRIES
import rex
import logician


def moon_call():
    """ call hot shots on market symbols """

    operations_log = {}
    operations_log["_init"] = get_time_now(stringify=True)

    print "[JOB] Starting moon_call at " + operations_log["_init"]

    symbols = rex.get_market_summaries()
    scores = []

    print "[JOB] Searching Twitter for BTRX symbol high volume list..."
    operations_log["twitter_search_start"] = get_time_now(stringify=True)
    # TODO: stale_break => use moon_call duration.
    avg_res = get_moon_call_res_duration()

    print "[JOB] Scoring " + str(len(symbols)) + " coins..."
    # get and score relevant tweets per symbol.
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
    print "[JOB] Symbols scored, tracking periphreals..."

    operations_log["track_periphreals_start"] = get_time_now(stringify=True)
    track_periphreals()
    operations_log["track_periphreals_end"] = get_time_now(stringify=True)

    # sort and find hottest trends
    sorted_scores = sorted(scores, key=itemgetter("score"), reverse=True)
    hot_hourly = sorted_scores[:3]

    print "[JOB] Preparing message templates..."

    hot_daily = get_score_history(tf="day")
    hot_weekly = get_score_history(tf="week")

    # prepare message for telegram
    operations_log["send_message_end"] = get_time_now(stringify=True)

    hourly_text = build_rating_template(hot_hourly, "Hourly Twitter Hype")
    daily_text = build_rating_template(hot_daily, "Daily Twitter Hype")
    weekly_text = build_rating_template(hot_weekly, "Weekly Twitter Hype")

    message_text = "_Analysis of credible #crypto social media for BTRX coins._\n"
    message_text += "_Disclaimer: These tweets are for RESERACH. Some are about dying coins, some about ones thriving with life! Make wise decisions on your own judgement._\n\n"
    message_text += hourly_text + "\n" + daily_text + "\n" + weekly_text
    message_text += "\nSupport development with BTC Tips @ `" + tip_jar + "`\n"

    send_message(text=message_text)

    operations_log["send_message_end"] = get_time_now(stringify=True)

    print "[JOB] Moon call complete, message sent at " + get_time_now(stringify=True)
    print "[JOB] Sleeping now for 30 minutes...\n\n"

    operations_log["_end"] = get_time_now(stringify=True)
    db.add(path="operations", file_name="moon_call", entry=operations_log)


def track_periphreals():
    """
    track_periphreals tracks secondary data such as
    - twitter trending per main tech countries
    - TODO: planetary movements
    """

    countries = HOT_COUNTRIES
    if env == "test":
        countries = countries[:2]

    for country in HOT_COUNTRIES:
        res = get_trends_for_woeid(country)

        for trend in res:
            entry = {}
            entry["topic"] = trend.name
            db.add(path="twitter/trends", file_name=str(country), entry=entry)


moon_call()
