from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_change_status_buyout_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_change_status_buyout")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_change_status_buyout")
    ]
])
