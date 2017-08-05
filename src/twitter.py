import tweepy
from settings import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth)


def get_recent_tweets_with_search_term(term):
    tweets = api.search(q=term, rpp=100)
    return tweets
