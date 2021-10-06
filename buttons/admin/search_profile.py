from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

type_search_profile = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Поиск по email", callback_data="search_with_email")
    ],
    [
        InlineKeyboardButton(text="Поиск по ID", callback_data="search_with_id")
    ],
    [
        InlineKeyboardButton(text="Поиск по номеру", callback_data="search_with_number")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")
    ]
])

back_to_category_TSP = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_TSP")
    ]
])
