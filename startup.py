import logging
from bot import bot, WEBHOOK_URL


async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL)
    try:
        import handlers
    except ImportError as ex:
        logging.warn(msg="[IMPORT ERROR]", exc_info=ex)


async def on_shutdown(_):
    await bot.delete_webhook()
