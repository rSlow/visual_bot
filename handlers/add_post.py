from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ContentType

from FSM import AddPost
from bot import bot
from bot import dp
from keyboards import cancel_kb, confirm_kb, photo_edit_kb, photo_kb
from orm import QueuePost
from schemas import Post
from .mains import main_menu


@dp.message_handler(Text(contains="Предложить фото"))
async def add_photos(message: Message, state: FSMContext):
    await AddPost.photo.set()
    await message.answer("Загрузите необходимые фото (<u>не документом!</u>) 🎑\n"
                         "Успешно загруженные фотографии будет удалены из чата.\n"
                         "Как загрузите все - <u>нажимаем внизу кнопочку <b>Далее</b></u> "
                         "(она может скрыться - тогда нажми 🎛 внизу...)",
                         reply_markup=photo_kb)
    async with state.proxy() as proxy:
        proxy["post_schema"] = Post(message.from_user.id, message.from_user.mention)


@dp.message_handler(content_types=ContentType.PHOTO, state=AddPost.photo)
async def append_photo(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["post_schema"].image_ids.append(message.photo[-1].file_id)
    await message.delete()


@dp.message_handler(Text(contains="Далее"), state=AddPost.photo)
async def confirm_photos_download(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        count_photos = len(proxy['post_schema'].image_ids)
        if not count_photos:
            await message.answer(text="Не было загружено ни одного фото! Давай еще разок 😌")
            await add_photos(message, state)
        else:
            await AddPost.next()
            await message.delete()
            await message.answer(f"Отлично, было загружено {count_photos} фото!\n"
                                 "На что было сделано фото? 📷",
                                 reply_markup=cancel_kb)


@dp.message_handler(state=AddPost.device)
async def add_shooting_method(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["post_schema"].device = message.text.strip()
    await message.delete()
    await AddPost.next()
    await message.answer("Хороший выбор.\n"
                         "Если использовалась программа для обработки - "
                         "ждем ее название 😊\n"
                         "А если нет - кнопочка внизу...",
                         reply_markup=photo_edit_kb)


@dp.message_handler(state=AddPost.photo_editing)
async def add_photo_processing(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        if ~message.text.find("Фото без обработки"):
            proxy["post_schema"].photo_editing = None
        else:
            proxy["post_schema"].photo_editing = message.text.strip()
    await message.delete()
    await AddPost.next()
    await message.answer("В каком городе или месте был сделан сий кадр?",
                         reply_markup=cancel_kb)


@dp.message_handler(state=AddPost.place)
async def add_place(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["post_schema"].place = message.text.strip()
        post: Post = proxy["post_schema"]
    await message.delete()
    if not message.text.strip():
        await message.answer("Ну нееет, город уже надо написать 😢",
                             reply_markup=cancel_kb)
    else:
        await AddPost.next()
        desc_message = await message.answer("Отлично. Пост будет выглядеть следующим образом:")
        media_messages = await bot.send_post(post=post, chat_id=message.from_user.id)
        confirm_message = await message.answer("Подтверждаем?",
                                               reply_markup=confirm_kb)
        async with state.proxy() as proxy:
            proxy["confirm_messages"] = [desc_message, *media_messages, confirm_message]


@dp.message_handler(Text(contains="Да"), state=AddPost.confirm)
@dp.message_handler(Text(contains="Нет"), state=AddPost.confirm)
async def confirm(message: Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as proxy:
        for confirm_message in proxy["confirm_messages"]:
            await confirm_message.delete()
        post: Post = proxy["post_schema"]
    if ~message.text.find("Да"):
        text = "Пост предложен на публикацию."
        await QueuePost.add_post(post)
        await main_menu(message=message, state=state, text=text + "\nЧто нибудь еще?")
        await bot.send_message(chat_id=bot.admins[0], text="В предложку был добавлен пост...")
    elif ~message.text.find("Нет"):
        await main_menu(message=message, state=state, text="Отменяем...")
    else:
        from handlers.z_delete import delete
        await delete(message)
