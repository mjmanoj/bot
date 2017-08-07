"""
the logician makes all the calls, he"s about as smart as he can be.
"""
import twitter
import db
from datetime import datetime, timedelta
from textblob import TextBlob
from operator import itemgetter


# strip_irrelevant takes tweets and sniffs everything for crypto mentions.
def strip_irrelevant(tweets):
    latest_tweets = sorted(tweets, key=itemgetter("created_at"))

    relevant_tweets = []
    for tweet in latest_tweets:
        if tweet["created_at"] < datetime.now() - timedelta(minutes=30):
            print("Encountering tweets already parsed... breaking")
            break

        user = tweet["user"]
        # fuck potential bots.
        if user["default_profile"] == True:
            continue

        # check if user in db, if not, add him.
        exists = db.find_by_id("twitter_users", user["id"])
        if exists == False:
            db.add("twitter_users", user)

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
        # gather data
        user = tweet["user"]
        followers = user["followers_count"]
        user_date_created = tweet["created_at"]
        account_age = datetime.now() - datetime(user_date_created)

        # score
        score += followers
        score += account_age
        if user["verified"]:
            score *= 2

        # judge tweet quality
        # gather data
        tweet_age = datetime.now() - datetime(tweet["created_at"])
        favs = tweet["favorite_count"]
        text = tweet["text"]
        content = TextBlob(text)

        # score
        score -= tweet_age
        if favs is not None:
            score += favs
        score += tweet["retweet_count"]

        score *= content.sentiment.polarity
        score *= content.sentiment.subjectivity

        scores.append(score)

    return sum(scores) / float(len(scores))
