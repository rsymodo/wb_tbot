from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

hub_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Профиль"),
        KeyboardButton(text="Выкупы")
    ],
    [
        KeyboardButton(text="Финансы"),
        KeyboardButton(text="Корзина")
    ],
    [
        KeyboardButton(text="Тарифы"),
        KeyboardButton(text="FAQ")
    ],
    [
        KeyboardButton(text="Контакты")
    ]
], resize_keyboard=True)
