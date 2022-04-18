from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text, CommandStart
from bot import dp


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, state: FSMContext):
    await message.answer("Привет")
