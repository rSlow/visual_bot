import logging
import os

import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode


class CustomBot:
    def __init__(self):
        self.admins = [959148697, 633760553]
        self.TZ = pytz.timezone("Asia/Vladivostok")


token = os.getenv("SOHABOT_TOKEN")
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)
