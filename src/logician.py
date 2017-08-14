"""
the logician makes all the calls, he"s about as smart as he can be.
"""
import db
from helpers import get_time_now
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta
from operator import itemgetter
from constants import VIP_PLAYERS


# strip_irrelevant takes tweets and sniffs everything for crypto mentions.
def strip_irrelevant(tweets):
    relevant_tweets = []
    for tweet in tweets:

        # ignore stale tweets.
        if parse_date(tweet.created_at) < get_time_now() - timedelta(minutes=30):
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
        followers = user.followers_count
        user_date_created = parse_date(user.created_at)
        account_age = int(get_time_now().strftime('%s')) - \
            int(user_date_created.strftime('%s'))

        score += followers
        score += account_age
        if user.verified:
            score *= 2

        # judge tweet quality
        tweet_created_date = parse_date(user.created_at)
        tweet_age = int(get_time_now().strftime('%s')) - \
            int(tweet_created_date.strftime('%s'))
        favs = tweet.favorite_count

        score -= tweet_age
        if favs:
            score += favs * 4
        score += tweet.retweet_count * 4

        # vips get bumps.
        if user.screen_name in VIP_PLAYERS:
            score *= 2

        # TODO: add sentiment analysis here!
        # - take the polarity of the text and simply multiply the score by that

        scores.append(score)

    if not score:
        return 0

    return sum(scores) / float(len(scores))
