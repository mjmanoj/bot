"""
the twit package is a bear python-twitter adapter
"""
import json
import twitter
from config import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret

api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)


# get_recent_tweets_with_search_term returns 100 search results per term
def search(term):
    return api.GetSearch(term=term, count=100, result_type="recent")


# gets a twitter user, aka tweep.
def get_tweep(tweep):
    return api.GetUser(tweep)


# gets top trending hash tags of the moment
def get_trends_for_woeid(place):
    return api.GetTrendsWoeid(place)
