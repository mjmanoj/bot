"""
config  works with environment variables
"""
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv = join(dirname(__file__), '../.env')
load_dotenv(dotenv)

# telegram bot
telegram_token = environ.get("bot_api_token")
telegram_chat = environ.get("telegram_chat")

# bittrex api
rex_api_key = environ.get("bittrex_api_key")
rex_api_secret = environ.get("bittrex_api_secret")

# twitter
twitter_consumer_key = environ.get('twitter_consumer_key')
twitter_consumer_secret = environ.get('twitter_consumer_secret')
twitter_access_token = environ.get('twitter_access_token')
twitter_access_secret = environ.get('twitter_access_secret')

# btc
tip_jar = environ.get('tip_jar')
