#!/usr/bin/python
"""
the main package runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
import operator
import archivist
import helpers
import bot
import twit
import rex
import logician
import postgres


def moon_call():
    """ call hot shots on market symbols """

    operations_log = {}
    operations_log["main_start"] = helpers.get_time_now(stringify=True)

    print("[JOB] Starting moon_call at " + operations_log["main_start"])

    summaries = rex.get_market_summaries()
    scores = []

    print("[JOB] Searching Twitter for BTRX symbol high volume list...")
    operations_log["twitter_search_start"] = helpers.get_time_now(
        stringify=True)

    avg_res = archivist.get_moon_call_res_duration()

    print("[JOB] Scoring " + str(len(summaries)) + " coins...")
    # get and score relevant tweets per symbol.
    for summary in summaries:
        entry = summary
        entry["created"] = helpers.get_time_now(stringify=True)

        coin_symbol = "$" + summary["symbol"]

        # search twitter
        tweets = twit.search(coin_symbol)
        score = logician.judge(tweets, stale_break=avg_res + 3200)

        # if score sucks, go to next symbol
        if not score:
            continue

        entry["score"] = int(score)
        postgres.add_twitter_score(entry)
        scores.append(entry)

    operations_log["twitter_search_end"] = helpers.get_time_now(stringify=True)

    # sort and find hottest trends
    sorted_scores = sorted(
        scores, key=operator.itemgetter("score"), reverse=True)
    hourly_top_scores = sorted_scores[:5]

    print("[JOB] Preparing message templates...")

    daily_top_scores = archivist.get_score_history(tf="day")
    weekly_top_scores = archivist.get_score_history(tf="week")

    # ensure that we are not unneecessarily sending daily/weekly block
    # if the daily/weekly has not changed.
    operations_log["daily_coins"] = []
    operations_log["weekly_coins"] = []

    for coin in daily_top_scores:
        operations_log["daily_coins"].append(coin["symbol"])

    for coin in weekly_top_scores:
        operations_log["weekly_coins"].append(coin["symbol"])

    last_daily = archivist.get_last_scores("day")
    last_weekly = archivist.get_last_scores("week")

    # day_match = 0
    # if last_daily is not None:
    #     print "DAILY"
    #     for i in range(0, len(daily_top_scores)):
    #         if daily_top_scores[i]["symbol"] == last_daily[i]:
    #             day_match += 1

    # week_match = 0
    # if last_weekly != None:
    #     print "WEEKLY"
    #     for i in range(0, len(weekly_top_scores)):
    #         if weekly_top_scores[i]["symbol"] == last_weekly[i]:
    #             week_match += 1

    # if day_match > 0:
    #     daily_top_scores = []

    # if week_match > 0:
    #     weekly_top_scores = []

    # prepare message for telegram
    operations_log["send_message_start"] = helpers.get_time_now(stringify=True)

    bot.generate_and_post_message(
        hourly_top_scores, daily_top_scores, weekly_top_scores)

    operations_log["send_message_end"] = helpers.get_time_now(stringify=True)

    print("[JOB] Moon call complete, message sent at " +
          helpers.get_time_now(stringify=True))
    print("[JOB] Sleeping now for one hour...\n\n")

    operations_log["main_end"] = helpers.get_time_now(stringify=True)
    postgres.add_operations_log(operations_log)


moon_call()
