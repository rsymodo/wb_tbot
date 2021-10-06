from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


confirm_contacts_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_new_contacts")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_new_contacts")
    ]
])

