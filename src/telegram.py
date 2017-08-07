"""
telergam is a telegram adapter
"""

import telegram
from config import telegram_token


bot = telegram.Bot(token=telegram_token)
