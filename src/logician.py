import twitter
import db
from datetime import datetime


# strip_irrelevant takes tweets and sniffs everything for crypto mentions.
def strip_irrelevant(tweets):
    relevant_tweets = []
    for tweet in tweets:
        user = tweet.get("user")

        # fuck potential bots.
        if user.get("default_profile") == True:
            return

        # check if user in db, if not, add him.
        exists = db.find_by_id("twitter_users", user.get('id'))
        if exists == False:
            db.add("twitter_users", user)

        # TODO: check relevant terms (https://textblob.readthedocs.io/en/dev/) for each tweet
        # TODO: return only tweets that are relevant

        # confirm tweet is relevant
        relevant_tweets.append(tweet)

    return relevant_tweets


def judge(tweets):
    scores = []
    for tweet in tweets:
        score_card = {}

        # judge tweet quality
        date_created = tweet.get("created_at")
        score_card["age"] = datetime.now() - datetime(date_created)

        # judge user quality
        user = tweet.get("user")

        score_card["verified"] = user.get("verified")

    # how many likes, how "liked" is this tweeter, etc.
    # return score card and general recommendation
