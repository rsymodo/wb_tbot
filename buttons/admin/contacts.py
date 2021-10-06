from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

faq_contacts_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")
    ]
])

confirm_contacts_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_new_contacts")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_new_contacts")
    ]
])
