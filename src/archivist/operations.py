'''
the operations package handles all operations related tasks
'''
import db
from operator import itemgetter


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
