from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text, CommandStart
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from FSM import AddPost
from bot import dp


@dp.message_handler(Text(contains="Отменить"), state="*")
@dp.message_handler(Text(contains="На главную"), state="*")
async def on_main(message: Message, state: FSMContext):
    await main_menu(message, state, text="Возвращаемся в главное меню...")


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, state: FSMContext):
    await main_menu(message, state, text="Добро пожаловать!")


async def main_menu(message: Message, state: FSMContext, text: str):
    if await state.get_state():
        await state.finish()
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    kb.add("Предложить фото 📷", "Редактировать посты ✏")
    return await message.answer(text, reply_markup=kb)
