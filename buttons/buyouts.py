from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_search_product_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена")
    ]
], resize_keyboard=True)
