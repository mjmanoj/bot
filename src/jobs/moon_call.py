#!/usr/bin/python
"""
the main package runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
from operator import itemgetter

import postgres
from config import env
from archivist import get_moon_call_res_duration, get_score_history
from helpers import get_time_now
from bot import generate_and_post_message
from twit import search, get_trends_for_woeid
from constants import HOT_COUNTRIES
import rex
import logician


def moon_call():
    """ call hot shots on market symbols """

    operations_log = {}
    operations_log["init"] = get_time_now(stringify=True)

    print("[JOB] Starting moon_call at " + operations_log["init"])

    summaries = rex.get_market_summaries()
    scores = []

    print("[JOB] Searching Twitter for BTRX symbol high volume list...")
    operations_log["twitter_search_start"] = get_time_now(stringify=True)

    avg_res = get_moon_call_res_duration()

    print("[JOB] Scoring " + str(len(summaries)) + " coins...")
    # get and score relevant tweets per symbol.
    for summary in summaries:
        entry = summary
        entry["created"] = get_time_now(stringify=True)

        coin_symbol = "$" + summary["symbol"]

        # search twitter
        tweets = search(coin_symbol)
        score = logician.judge(tweets, stale_break=avg_res + 3200)

        # if score sucks, go to next symbol
        if not score:
            continue

        entry["score"] = int(score)
        postgres.add_coin_symbol(entry)
        scores.append(entry)

    operations_log["twitter_search_end"] = get_time_now(stringify=True)

    # sort and find hottest trends
    sorted_scores = sorted(scores, key=itemgetter("score"), reverse=True)
    hourly_top_scores = sorted_scores[:3]

    print("[JOB] Preparing message templates...")

    daily_top_scores = get_score_history(tf="day")
    weekly_top_scores = get_score_history(tf="week")

    # prepare message for telegram
    operations_log["send_message_end"] = get_time_now(stringify=True)

    generate_and_post_message(
        hourly_top_scores, daily_top_scores, weekly_top_scores)

    operations_log["send_message_end"] = get_time_now(stringify=True)

    print("[JOB] Moon call complete, message sent at " +
          get_time_now(stringify=True))
    print("[JOB] Sleeping now for one hour...\n\n")

    operations_log["end"] = get_time_now(stringify=True)
    postgres.add_operations_log(operations_log)


moon_call()
