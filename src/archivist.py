import os
import db
from datetime import datetime, date
from helpers import get_time_now
from config import env
from operator import itemgetter
cwd = os.getcwd()


def get_score_history(interval):
    score_files = cwd + "/db/" + env + "/symbols/"
    symbol_score_dbs = os.listdir(score_files)

    now = datetime.fromtimestamp(get_time_now())

    scores = []

    for symbol_db_file in symbol_score_dbs:
        entry = {}
        symbol = symbol_db_file.split(".")[0]
        entry["symbol"] = symbol

        interval_entries = 0
        interval_score = 0

        symbol_db = db.get(path="symbols", file_name=symbol)

        for entry in symbol_db:
            if interval == "day":
                today = now
                score_day = datetime.fromtimestamp(symbol["created"])

                if today == score_day:
                    interval_score += symbol["score"]
                    interval_entries += interval_entries

            if interval == "week":
                cal_week = date.fromtimestamp(now).isocalendar()
                score_week = date.fromtimestamp(
                    symbol["created"]).isocalendar()

                if cal_week == score_week:
                    interval_score += symbol["score"]
                    interval_entries += interval_entries

        entry["score"] = interval_score / interval_entries
        scores.append(entry)

    sorted_scores = sorted(scores, key=itemgetter("score"))

    return sorted_scores[:3]


# get_twitter_res_time returns the logged average api response time for twitter
def get_twitter_res_time(time_range):
    moon_call_ops = db.get(path="operations", file_name="moon_call")
    sorted_ops = sorted(moon_call_ops, key=itemgetter("_init"), reverse=True)

    res_time = 0

    if time_range == "last":
        last_op = sorted_ops[0]

        if last_op:
            start = int(last_op["twitter_search_start"])
            end = int(last_op["twitter_search_end"])
            last_twitter_call_seconds = abs(start - end)
            res_time += last_twitter_call_seconds
            print "[INFO] last twitter response time was " + str(last_twitter_call_seconds) + " seconds."

    if time_range == "average" and sorted_ops is not None:
        durations = 0

        for operation in sorted_ops:
            start = int(operation["twitter_search_start"])
            end = int(operation["twitter_search_end"])
            durations += abs(start - end)

        res_time += durations / len(sorted_ops)
        print "[INFO] average twitter response time " + res_time + " seconds."

    return res_time
