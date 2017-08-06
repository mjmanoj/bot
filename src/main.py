import constants
import rex
import twitter
import logician
from helpers import set_interval


# call hot shots on market symbols
def moon_call():
    symbols = rex.get_market_symbols()

    for symbol in symbols:
        modified = "$" + symbol

        tweets = twitter.search(modified)
        relevant_tweets = logician.strip_irrelevant(tweets)
        score = logician.judge(relevant_tweets)
        # TODO: store score to symbol_score database
        get_peripherals()

    # telegram results over a certain threshold.


# gets peripheral data
# - twitter trending per main tech countries
def get_peripherals():
    for country in constants.HOT_COUNTRIES:
        twitter.get_trends_for_woeid(country)
        # logician judge this.
        # write this to database


set_interval(moon_call, constants.DEFAULT_MINS)
