import twitter
import db

# sniff_tweets takes tweets and sniffs everything for crypto mentions.


def strip_irrelevant(tweets):
    for tweet in tweets:
        user = tweet.get('twitter_users')

        # fuck potential bots.
        if user.get('default_profile') == False:
            exists = db.find_by_id('user', user.get('id'))
            if exists == False:
                db.add('twitter_users', user)

        # check relevant terms (https://textblob.readthedocs.io/en/dev/) for each tweet
        # return only tweets that are relevant


def judge(tweets):
    # sentiment analysis
    # how many likes, how "liked" is this tweeter, etc.
    # return score card and general recommendation
