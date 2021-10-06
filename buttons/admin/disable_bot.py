from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_disable_system_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_DS")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_DS")
    ]
])
