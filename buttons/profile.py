from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

close_profile_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Закрыть", callback_data="close_profile")
    ]
])
