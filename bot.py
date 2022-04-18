import logging
import os
import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class CustomBot:
    def __init__(self):
        self.admins = [959148697, ]
        self.TZ = pytz.timezone("Asia/Vladivostok")


# token = os.getenv("tg_token")
token = "5378540697:AAGWsxYPguOQqB45jFwt3-scL0BPpzb1j-E"
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot=bot,
                storage=storage)
