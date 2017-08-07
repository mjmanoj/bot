"""
tweepy adapter
"""
import tweepy
from config import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

twitter = tweepy.API(auth)


# get_recent_tweets_with_search_term returns 100 search results per term
def search(term):
    return twitter.search(q=term, rpp=100)


# gets a twitter user, aka tweep.
def get_tweep(tweep):
    return twitter.get_user(tweep)


# gets top trending hash tags of the moment
def get_trends_for_woeid(place):
    return twitter.trends_place(place)
