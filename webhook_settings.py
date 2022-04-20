import os
from bot import TOKEN

APP_NAME = os.getenv('APP_NAME') or "aiogram-test-redslow"
WEBHOOK_HOST = f'https://{APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)
