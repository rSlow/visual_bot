from aiogram import executor

from bot import dp, WEBHOOK_PATH
from orm import Base, Engine
from startup import on_startup, on_shutdown

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=5000,

    )
    # executor.start_polling(dispatcher=dp,
    #                        skip_updates=True,
    #                        on_startup=on_startup)
