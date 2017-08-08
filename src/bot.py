"""
moonbot is a telegram adapter
"""
import telegram
from config import telegram_token, telegram_chat

bot = telegram.Bot(token=telegram_token)


def send_message(chat_id, text, parse_mode="HTML"):
    bot.send_message(chat_id, text, parse_mode)
