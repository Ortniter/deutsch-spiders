import asyncio
import logging

from telegram.ext import Application, CommandHandler, CallbackQueryHandler

import config
from bot import handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()


def start():
    APP.add_handler(CommandHandler('start', handlers.start))
    APP.add_handler(CommandHandler('scrapers', handlers.scrapers))
    APP.add_handler(CommandHandler('scrapers', handlers.scrapers))
    APP.add_handler(CallbackQueryHandler(handlers.Button()))
    APP.add_handler(CommandHandler('ausbildung', handlers.ausbildung))
    APP.run_polling()


def send_message(chat_id: int, text: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(APP.bot.send_message(chat_id=chat_id, text=text))


if __name__ == '__main__':
    start()
