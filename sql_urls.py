import os

DATABASE_URL_ENV = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql+asyncpg" + DATABASE_URL_ENV[DATABASE_URL_ENV.find(":"):]
