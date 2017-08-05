from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

telegram_token = environ.get("bot_api_token")
