from typing import Optional

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from bot import dp, bot
from functools import wraps
from FSM import Admin
from schemas import Queue
from keyboards import cancel_kb


def admin_required(func):
    @wraps(func)
    def inner(message, *args, **kwargs):
        if message.from_user.id not in bot.admins:
            from .z_delete import delete
            return delete(message=message)
        else:
            return func(message, *args, **kwargs)

    return inner


@dp.message_handler(Text(contains="Просмотреть очередь"))
@admin_required
async def get_queue_element(message: Message, state: FSMContext):
    bot.queue = Queue.from_database()
    await Admin.start.set()
    post_id, post = bot.queue.get_first()
    if post_id:
        post = bot.queue.get_post_by_id(post_id=post_id)
        async with state.proxy() as proxy:
            proxy["current_post_id"] = post_id
            proxy["post_backup"] = post
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add("Опубликовать", "Отклонить", "Редактировать")
        await bot.send_post_for_confirm(post, chat_id=message.from_user.id, reply_markup=kb)
    else:
        from handlers.mains import main_menu
        await main_menu(message=message, state=state, text="Постов в очереди нет.")


@dp.message_handler(Text(contains="Опубликовать"), state=Admin.start)
async def post_confirm(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    post = bot.queue.get_post_by_id(post_id)
    await bot.publish_post(post)
    bot.queue.delete_by_id(post_id=post_id)
    await message.answer("Опубликовано.")
    await get_queue_element(message=message, state=state)


@dp.message_handler(Text(contains="Отклонить"), state=Admin.start)
async def post_decline(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    bot.queue.delete_by_id(post_id=post_id)
    await message.answer("Отклонено.")
    await get_queue_element(message=message, state=state)


@dp.message_handler(Text(contains="Редактировать"), state=Admin.start)
async def edit_post(message: Message, state: FSMContext, text: Optional[str] = None):
    if not text:
        text = "Что редактируем?"

    await Admin.edit.set()
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]

    post = bot.queue.get_post_by_id(post_id=post_id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add("Камера", "Место", "Обработка")
    kb.add(*[f"Фото №{i + 1} 🗑" for i in range(len(post.image_ids))])
    kb.add("Сохранить 💾", "Не сохранять ⛔")
    await message.answer(text, reply_markup=kb)


@dp.message_handler(Text(contains="Сохранить"), state=Admin.edit)
async def save_post(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    post = bot.queue.get_post_by_id(post_id=post_id)
    post.update()
    await message.answer("Изменения сохранены.")
    await get_queue_element(message=message, state=state)


@dp.message_handler(Text(contains="Не сохранять"), state=Admin.edit)
async def decline_edits_post(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
        backup_post = proxy["post_backup"]
        bot.queue[post_id] = backup_post
    await get_queue_element(message=message, state=state)


@dp.message_handler(Text(contains="Отменить"), state=(Admin.edit_method, Admin.edit_place, Admin.edit_device))
async def cancel_edit_fields(message: Message, state: FSMContext):
    await edit_post(message=message, state=state, text="Изменения отменены.")


@dp.message_handler(Text(contains="Камера"), state=Admin.edit)
async def edit_post_device(message: Message):
    await Admin.edit_device.set()
    await message.answer("Новая камера:",
                         reply_markup=cancel_kb)


@dp.message_handler(state=Admin.edit_device)
async def edit_post_device_confirm(message: Message, state: FSMContext):
    device = message.text.strip()
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    post = bot.queue.get_post_by_id(post_id=post_id)
    post.device = device
    await edit_post(message=message, state=state, text="Новая камера установлена.")


@dp.message_handler(Text(contains="Место"), state=Admin.edit)
async def edit_post_device(message: Message):
    await Admin.edit_place.set()
    await message.answer("Новое место съемки:",
                         reply_markup=cancel_kb)


@dp.message_handler(state=Admin.edit_place)
async def edit_post_device_confirm(message: Message, state: FSMContext):
    place = message.text.strip()
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    post = bot.queue.get_post_by_id(post_id=post_id)
    post.place = place
    await edit_post(message=message, state=state, text="Новое место съемки сохранено.")


@dp.message_handler(Text(contains="Обработка"), state=Admin.edit)
async def edit_post_device(message: Message):
    await Admin.edit_method.set()
    await message.answer("Новая программа для обработки:",
                         reply_markup=cancel_kb)


@dp.message_handler(state=Admin.edit_method)
async def edit_post_device_confirm(message: Message, state: FSMContext):
    photo_editing = message.text.strip()
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    post = bot.queue.get_post_by_id(post_id=post_id)
    post.photo_editing = photo_editing
    await edit_post(message=message, state=state, text="Программа для обработки изменена.")


@dp.message_handler(regexp=r"Фото №\d{1,2}.*", state=Admin.edit)
async def delete_photo(message: Message, state: FSMContext):
    photo_num = int(message.text.split()[1].replace("№", "").strip())
    async with state.proxy() as proxy:
        post_id = proxy["current_post_id"]
    post = bot.queue.get_post_by_id(post_id=post_id)
    if len(post.image_ids) == 1:
        return await edit_post(message=message, state=state, text="Невозможно удалить единственную фотографию.")
    post.delete_photo(photo_num)
    await edit_post(message=message, state=state, text=f"Фото №{photo_num} удалено.")
