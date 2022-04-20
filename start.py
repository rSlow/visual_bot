from aiogram import executor

from bot import dp
from orm import Base, Engine
from startup import on_startup, on_shutdown
from webhook_settings import WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
    # executor.start_polling(dispatcher=dp,
    #                        skip_updates=True,
    #                        on_startup=on_startup)
