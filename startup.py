import logging
from bot import bot
from webhook_settings import WEBHOOK_URL
from orm import Engine, Base


async def on_startup(_):
    async with Engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    try:
        import handlers
    except ImportError as ex:
        logging.warn(msg="[IMPORT ERROR]", exc_info=ex)


async def on_shutdown(_):
    await bot.delete_webhook()
