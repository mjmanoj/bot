from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# telegram bot
telegram_token = environ.get("bot_api_token")

# bittrex api
rex_api_key = environ.get("bittrex_api_key")
rex_api_secret = environ.get("bittrex_api_secret")
