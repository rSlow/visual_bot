import logging

async def on_startup(_):
    try:
        import handlers
    except ImportError as ex:
        logging.warn(msg="[IMPORT ERROR]", exc_info=ex)
