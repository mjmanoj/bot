import twitter
import db
from datetime import datetime
from textblob import TextBlob


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


# judge provides a score judging an array of tweets based on
# - user credibility
# - tweet quality, hype
def judge(tweets):
    scores = []
    for tweet in tweets:
        score = 0

        # judge user credibility
        # gather data
        user = tweet.get("user")
        followers = user.get('followers_count')
        user_date_created = tweet.get("created_at")
        account_age = datetime.now() - datetime(user_date_created)

        # score
        score += followers
        score += account_age
        if user.get("verified") == True:
            score *= 2

        # judge tweet quality
        # gather data
        tweet_date_created = tweet.get("created_at")
        tweet_age = datetime.now() - datetime(tweet_date_created)
        favs = tweet.get("favorite_count")
        retweets = tweet.get("retweet_count")
        text = tweet.get("text")
        content = TextBlob(text)

        # score
        score -= tweet_age
        if favs is not None:
            score += favs
        score += retweets

        score *= content.sentiment.polarity
        score *= content.sentiment.subjectivity

        scores.append(score)

    return sum(scores) / float(len(scores))
