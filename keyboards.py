from aiogram.types import ReplyKeyboardMarkup

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Отменить 🙅‍♂")
confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Да ✅", "Нет ❌")
