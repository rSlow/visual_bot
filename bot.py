import logging
import os

import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode, Message, MediaGroup, ReplyKeyboardMarkup

from schemas import Post, PostMediaGroup, Queue
from typing import Optional, Union


class CustomBot(Bot):
    def __init__(self, *args, **kwargs):
        super(CustomBot, self).__init__(*args, **kwargs)
        self.admins = [
            633760553,
            959148697
        ]
        self.TZ = pytz.timezone("Asia/Vladivostok")
        self.queue = Queue()
        # self.channel_id = -1001768034794  # test
        self.channel_id = -1001566129579  # main

    async def send_post(self, post: Post, chat_id: Union[int, str]) -> list[Message]:
        post_media = PostMediaGroup()
        post_media.attach_media_group(image_ids=post.image_ids, group_caption=post.text)
        return await self.send_media_group(chat_id=chat_id, media=post_media)

    async def send_post_for_confirm(self,
                                    post: Post,
                                    chat_id=None,
                                    reply_markup: Optional[ReplyKeyboardMarkup] = None):
        if chat_id is None:
            chat_id = self.channel_id
        media = MediaGroup()
        for image_id in post.image_ids:
            media.attach_photo(image_id)
        media_block = await self.send_media_group(chat_id=chat_id, media=media)
        caption_block = await self.send_message(chat_id=chat_id, text=post.text, reply_markup=reply_markup)
        return [media_block, caption_block]

    async def publish_post(self, post: Post):
        return await self.send_post(post=post, chat_id=self.channel_id)


token = os.getenv("SOHABOT_TOKEN")
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = CustomBot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)
