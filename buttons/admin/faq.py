from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

faq_edit_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")  # Общая кнопка возврата в АП
    ]
])

confirm_new_text_faq_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_new_faq")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_new_faq")
    ]
])
