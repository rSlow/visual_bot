from aiogram import executor
from bot import dp
from statpup import on_startup

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
