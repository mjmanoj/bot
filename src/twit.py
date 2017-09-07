#!/usr/bin/python
"""
the twit package is a bear python-twitter adapter
"""
import twitter
from config import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret

API = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)


def search(term):
    """ get_recent_tweets_with_search_term returns 100 search results per term """

    return API.GetSearch(term=term, count=100, result_type="recent")


def get_tweep(tweep):
    """ gets a twitter user, aka tweep. """
    return API.GetUser(tweep)
