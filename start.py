from aiogram import executor

from bot import dp, WEBHOOK_PATH
from orm import Base, Engine
from startup import on_startup

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)
    executor.start_webhook(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           webhook_path=WEBHOOK_PATH,
                           port=5000)

    # executor.start_polling(dispatcher=dp,
    #                        skip_updates=True,
    #                        on_startup=on_startup)
