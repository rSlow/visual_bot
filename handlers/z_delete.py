from aiogram.types import Message, ContentType
from bot import dp
from asyncio import sleep


@dp.message_handler(content_types=ContentType.ANY, state="*")
async def delete(message: Message):
    await message.delete()
    msg = await message.answer("Читаем инструкцию и не спамим!")
    await sleep(2)
    await msg.delete()
