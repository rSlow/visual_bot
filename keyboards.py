from aiogram.types import ReplyKeyboardMarkup

photo_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Далее ➡", "Отменить 🙅‍♂")
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Отменить 🙅‍♂")
photo_edit_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Фото без программы 🙅‍♀", "Отменить 🙅‍♂")
confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Да ✅", "Нет ❌")
