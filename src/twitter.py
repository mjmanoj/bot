import tweepy
from settings import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth)


# get_recent_tweets_with_search_term returns 100 search results per term
# TODO: expand for more results, have to do multiple pages to support that
# could do an iterate over count while >= page, then page +
def search(term):
    return api.search(q=term, rpp=100)


def get_tweep(tweep):
    return api.get_user(tweep)
