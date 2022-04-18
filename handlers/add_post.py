from aiogram.types import Message, ContentType
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from FSM import AddPost
from bot import dp
from keyboards import cancel_kb, confirm_kb
from .mains import main_menu
from orm_sql.models import QueuePost
from schemas import PostSchema


@dp.message_handler(Text(contains="Предложить фото"))
async def add_photo(message: Message, state: FSMContext):
    await AddPost.next()
    await message.answer("Загрузите необходимое фото (не документом!) 🎑",
                         reply_markup=cancel_kb)
    async with state.proxy() as proxy:
        proxy["add_post"] = PostSchema(message.from_user.id)


@dp.message_handler(content_types=ContentType.PHOTO, state=AddPost.photo)
async def add_shooting_method(message: Message, state: FSMContext):
    await AddPost.next()
    async with state.proxy() as proxy:
        proxy["add_post"].image_id = message.photo[0].file_id
    await message.delete()
    await message.answer("Отлично! На что было сделано фото? 📷",
                         reply_markup=cancel_kb)


@dp.message_handler(state=AddPost.device)
async def add_shooting_method(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["add_post"].device = message.text.strip()
    await message.delete()
    await AddPost.next()
    await message.answer("Хороший выбор.\n"
                         "Если использовалась программа для обработки - "
                         "ждем ее название 😊\n"
                         "А если нет - кнопочка внизу...",
                         reply_markup=cancel_kb)


@dp.message_handler(state=AddPost.photo_editing)
async def add_photo_processing(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["add_post"].photo_editing = message.text.strip() or None
    await message.delete()
    await AddPost.next()
    await message.answer("В каком городе или месте был сделан сий кадр?",
                         reply_markup=cancel_kb)


@dp.message_handler(state=AddPost.place)
async def add_place(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["add_post"].place = message.text.strip()
        post = proxy["add_post"]
    await message.delete()
    if not message.text.strip():
        await message.answer("Ну нееет, город уже надо написать 😢",
                             reply_markup=cancel_kb)
    else:
        await AddPost.next()
        caption = f"{post.device} | {post.photo_editing}\n" \
                  f"Place - {post.place}"
        conf_1_m = await message.answer("Отлично. Пост будет выглядеть следующим образом:")
        conf_2_m = await message.answer_photo(photo=post.image_id,
                                              caption=caption)
        conf_3_m = await message.answer("Подтверждаем?",
                                        reply_markup=confirm_kb)
        async with state.proxy() as proxy:
            proxy["confirm_messages"] = [conf_1_m, conf_2_m, conf_3_m]


@dp.message_handler(Text(contains="Да"), state=AddPost.confirm)
@dp.message_handler(Text(contains="Нет"), state=AddPost.confirm)
async def confirm(message: Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as proxy:
        for message in proxy["confirm_messages"]:
            await message.delete()
        post: PostSchema = proxy["add_post"]

    if not ~message.text.find("Да"):
        text = "Пост предложен на публикацию."
        QueuePost.add_post(post)
        await main_menu(message=message, state=state, text=text + "\nЧто нибудь еще?")

    elif not ~message.text.find("Нет"):
        text = "Отменяем..."
        temp_message = await main_menu(message=message, state=state, text=text)
        temp_message.delete()
