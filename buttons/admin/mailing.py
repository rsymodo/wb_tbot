from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_mailing_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_mailing")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_mailing")
    ]
])
