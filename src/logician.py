"""
the logician makes all the calls, he"s about as smart as he can be.
"""
import twitter
import db
from helpers import get_time_now
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta
from textblob import TextBlob
from operator import itemgetter


# strip_irrelevant takes tweets and sniffs everything for crypto mentions.
def strip_irrelevant(tweets):
    latest_tweets = sorted(tweets, key=itemgetter("created_at"))
    relevant_tweets = []

    for tweet in latest_tweets:

        # ignore stale tweets.
        if parse_date(tweet["created_at"]) < get_time_now() - timedelta(minutes=30):
            break

        user = tweet["user"]

        # fuck potential bots.
        if user["default_profile"] == True:
            continue

        # check if user in db, if not, add him.
        existing_user = db.find_by_id(
            path="users", file_name="twitter", identifier=user["id"])

        if not len(existing_user):
            db.add(path="users", file_name="twitter", entry=user)

        # confirm tweet is relevant
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
        user = tweet["user"]
        followers = user["followers_count"]
        user_date_created = parse_date(user["created_at"])
        account_age = int(get_time_now().strftime('%s')) - \
            int(user_date_created.strftime('%s'))

        score += followers
        score += account_age
        if user["verified"]:
            score *= 2

        # judge tweet quality
        tweet_created_date = parse_date(user["created_at"])
        tweet_age = int(get_time_now().strftime('%s')) - \
            int(tweet_created_date.strftime('%s'))
        favs = tweet["favorite_count"]
        text = tweet["text"]
        content = TextBlob(text)

        score -= tweet_age
        if favs is not None:
            score += favs  # TODO: functional MULTIPLIER
        score += tweet["retweet_count"]  # TODO: functional MULTIPLIER

        # TODO: fix -> score *= content.sentiment.polarity
        # TODO: fix -> score *= content.sentiment.subjectivity

        scores.append(score)

    if len(scores) == 0:
        return 0

    return sum(scores) / float(len(scores))
