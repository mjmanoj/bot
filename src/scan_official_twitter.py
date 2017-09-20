#!/usr/bin/python
"""
this script gets the top 40 coins of bittrex and then calls twitter accounts every couple of minutes with these coins
to find if they have posted anything of relevance.
"""

import rex
import postgres
import helpers
import twit
import archivist
import bot

# TODO: how do we can and make meaning of well known exchanges twitter account posts?


def scan():
    print("[JOB] Official Twitter Accounts Scan starting...")

    scan_log = {}
    scan_log["start"] = helpers.get_time_now()

    last_duration = archivist.get_last_twitter_scan_duration()
    cutoff = 600 + last_duration

    summaries = rex.get_market_summaries()
    database_entries = postgres.get_coin_infos()

    # empty prefill for currencies info for inserting new coin_infos
    currencies = []
    all_statuses = []

    for summary in summaries:

        # TODO
        # only take coins based on their market summaries
        # - golden range of - 4% decrease and +4 % encrase

        coin_info = helpers.find(database_entries, "symbol", summary["symbol"])
        all_statuses[summary["symbol"]] = []

        if coin_info and "twitter" in coin_info:
            statuses = twit.check_account_for_new_posts(
                coin_info["twitter"], cutoff)

            if statuses != None:
                for status in statuses:
                    # - check if tweet has specific criteria (how do we define?)
                    # date = helpers.find_date_in_string(status.text)

                    # if date:
                    #     url = "https://twitter.com/statuses/" + status.id_str
                    #     postgres.add_calendar_event(
                    #         summary["symbol"], date, url)

                    # TODO
                    # - status.created_at receives a expontential multiplier based on how close it is to present
                    # - multiply against status.favorite_count,
                    # - also again status.retweet_count,
                    # - also if a date or time is referenced in the tweet
                    # - also for each of the constants.HOT_TAGS that are in the hashtags.
                    # - sentiment analysis
                    # - push tweet id_str and score to all_statuses[summary["symbol"]]

            else:
                bot.send_message(typ="private", user="azurikai",
                                 text="No twitter account found for " + summary["symbol"] + ", please add it!")

        else:
            if currencies != None:
                currencies = rex.Client.get_currencies()["result"]

            currency = helpers.find(currencies, "Currency", summary["symbol"])

            postgres.add_coin_info(summary, currency)
            bot.send_message(typ="private", user="azurikai",
                                 text="New entry added for " + summary["symbol"] + ", please update!")

        # TODO
        # take all statuses for each object
        # - store top scoring status for each coin into competition array
        # sort competition array to top 3 based on score
        # send message about the HOTTEST TWEETS OF TWITTER!

    scan_log["end"] = helpers.get_time_now()
    scan_log["duration"] = abs(scan_log["start"] - scan_log["end"])
    postgres.add_twitter_call_log(scan_log)
    print("[JOB] Official Twitter Accounts Scan finished in " +
          str(scan_log["duration"]) + " seconds.")


scan()
