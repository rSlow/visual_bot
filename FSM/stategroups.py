from aiogram.dispatcher.filters.state import StatesGroup, State


class AddPost(StatesGroup):
    photo = State()
    device = State()
    photo_editing = State()
    place = State()
    confirm = State()
