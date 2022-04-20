from aiogram import executor

from bot import dp
from orm import Base, Engine
from startup import on_startup

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
