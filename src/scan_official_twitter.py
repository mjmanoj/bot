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
    scan_log["start"] = helpers.get_time_now(stringify=True)

    last_duration = archivist.get_last_twitter_scan_duration()
    cutoff = 600 + last_duration

    summaries = rex.get_market_summaries()
    database_entries = postgres.get_coin_infos(cutoff)

    for summary in summaries:
        coin_info = helpers.find(database_entries, "symbol", summary["symbol"])

        if "twitter" in coin_info:
            posts = twit.check_account_for_new_posts(
                coin_info["twitter"], cutoff)

            if posts != None:
                for post in posts:
                    # - check if tweet has specific criteria (how do we define?)
                    date = helpers.find_date_in_string(post.text)
                    text = "Official Twitter Announcement from " + \
                        summary["symbol"] + "! Rating... HOT!\n"

                    if date:
                        text += "Mark your calendars => " + date + ".\n"
                        postgres.add_calendar_event(
                            summary["symbol"], date, post.link)

                    text += post.text + "\n" + post.link

                    bot.send_message(text=text, disable_link_preview=False)

        else:
            bot.send_message(typ="private", user="azurikai",
                             text="No twitter account found for " + summary["symbol"] + ", please add it!")

    scan_log["end"] = helpers.get_time_now(stringify=True)
    scan_log["duration"] = abs(scan_log["start"] - scan_log["end"])
    postgres.add_twitter_call_log(scan_log)
    print("[JOB] Official Twitter Accounts Scan finished in " +
          str(scan_log["duration"]) + " seconds.")
