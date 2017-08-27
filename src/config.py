""" the config package works with environment variables """
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

env = join(dirname(__file__), "../.env")
load_dotenv(env)

# telegram bot
telegram_token = environ["bot_api_token"]
telegram_chat_prod = environ["telegram_chat_prod"]
telegram_chat_dev = environ["telegram_chat_dev"]
kirby_bot_channel = environ["kirby_bot_channel"]

# bittrex api
rex_api_key = environ["bittrex_api_key"]
rex_api_secret = environ["bittrex_api_secret"]

# twitter
twitter_consumer_key = environ["twitter_consumer_key"]
twitter_consumer_secret = environ["twitter_consumer_secret"]
twitter_access_token = environ["twitter_access_token"]
twitter_access_secret = environ["twitter_access_secret"]

# tips
btc_tip_jar = environ["btc_tip_jar"]
ltc_tip_jar = environ["ltc_tip_jar"]
rain_tip_jar = environ["rain_tip_jar"]

# environment
env = environ["ENV"]
