from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

start_registration_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Регистрация", callback_data="start_registration")
    ]
])

get_number_markup = ReplyKeyboardMarkup(resize_keyboard=True)
get_number_markup.add(KeyboardButton(text="Дать номер", request_contact=True))
