from aiogram.dispatcher.filters.state import StatesGroup, State


class AddPost(StatesGroup):
    photo = State()
    device = State()
    photo_editing = State()
    place = State()
    confirm = State()


class Admin(StatesGroup):
    start = State()
    edit = State()
    edit_device = State()
    edit_place = State()
    edit_method = State()
