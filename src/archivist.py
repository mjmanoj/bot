#!/usr/bin/python
""" the archivist deals with archived data in the databases """
import os
from datetime import datetime, date
from operator import itemgetter

import postgres
from rex import Rex
from helpers import get_time_now, find
from dateutil.parser import parse as parse_date
from datetime import timedelta, datetime
from config import env
CWD = os.getcwd()


def get_score_history(tf):
    """ gets the score history for all coins, returning top 3 for the respective tf """

    currencies = Rex.get_currencies()["result"]

    now = get_time_now(naive=False)
    day_delta = timedelta(hours=24)
    week_delta = timedelta(hours=168)

    cutoff = now - week_delta

    if tf is "daily":
        cutoff = now - day_delta

    rows = postgres.get_historical_twitter_scores(cutoff)
    scores = []

    if rows is None:
        return []

    for row in rows:
        found = False
        # check scores and add score to existing score if it exists
        for entry in scores:
            if entry["symbol"] == row["symbol"]:
                entry["score"] += row["score"]
                found = True
                break

        if not found:
            if "name" not in row:
                coin_info = find(currencies, "Currency", row["symbol"])
                if coin_info:
                    row["name"] = coin_info["CurrencyLong"].lower()

            scores.append(row)

    if scores is not None:
        scores = sorted(scores, key=itemgetter("score"), reverse=True)
        scores = scores[:5]

    return scores


def get_moon_call_res_duration():
    """ get_moon_call_res_duration returns the moon call duration"""

    last_op = postgres.get_moon_call_operations()

    moon_call_duration = 0

    if last_op is not None:
        start = int(last_op["main_start"])
        end = int(last_op["main_end"])
        duration = abs(start - end)
        moon_call_duration += duration
        print("[INFO] last moon_call duration was " +
              str(duration) + " seconds.")

    return moon_call_duration


def get_last_scores(tf):
    """ get_last_scores returns the last scores from the moon call based on the timeframe"""

    last_op = postgres.get_moon_call_operations()

    if last_op is not None:
        if tf == "daily":
            return last_op["daily_coins"]

        if tf == "weekly":
            return last_op["weekly_coins"]

    return []
