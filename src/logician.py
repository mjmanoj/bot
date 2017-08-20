"""
the logician package makes all the calls, based on human logic.
"""
import db
from helpers import get_time_now
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta
from operator import itemgetter
from constants import VIP_PLAYERS, SHILLS


# strip_irrelevant takes tweets and sniffs everything for crypto mentions.
def strip_irrelevant(tweets, stale_break):
    relevant_tweets = []

    for tweet in tweets:

        # ignore stale tweets.
        if parse_date(tweet.created_at) < get_time_now() - timedelta(seconds=stale_break):
            break

        user = tweet.user

        # fuck potential bots.
        # - default profile means they have not modified at all.
        if user.default_profile is True:
            continue

        # TODO: ensure profile/tweet is in fact about crypto currency.

        # check if user in db, if not, add him.
        existing_user = db.find_by_id(
            path="users", file_name="twitter", identifier=user.id)

        if not existing_user:
            db.add(path="users", file_name="twitter", entry=user.AsDict())

        relevant_tweets.append(tweet)

    return relevant_tweets


# judge provides a score judging an array of tweets based on
# - user credibility
# - tweet quality, hype
def judge(tweets):
    scores = []
    for tweet in tweets:
        score = 0

        # judge user credibility
        user = tweet.user
        twitter_handle = user.screen_name
        followers = user.followers_count

        # fuck shills and spammers.
        if twitter_handle in SHILLS:
            continue

        score += followers
        if user.verified:
            score *= 2

        # judge tweet quality
        favs = tweet.favorite_count
        retweets = tweet.retweet_count
        text = tweet.text

        # TODO: check tweet.entities
        # https://dev.twitter.com/overview/api/entities
        # if these entities are in CRYPTO_TERMS yeahhh

        if favs:
            score += favs * 4

        if retweets:
            score += retweets * 4

        # vips get bumps.
        if twitter_handle in VIP_PLAYERS:
            score *= 2

        # deduct points for coin spamming
        if text.count("$") > 5:
            score *= 0.5

        # TODO: add sentiment analysis here!
        # - take the polarity of the text and simply multiply the score by that

        scores.append(score)

    if not score:
        return 0

    return sum(scores) / float(len(scores))
