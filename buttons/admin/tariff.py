from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

management_tariff_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить тариф", callback_data="add_tariff")
    ],
    [
        InlineKeyboardButton(text="Удалить тариф", callback_data="del_tariff")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")
    ]
])

back_to_management_tariff_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Закрыть", callback_data="back_to_management_tariff")
    ]
])

confirm_add_tariff_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_add_tariff")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_add_tariff")
    ]
])

confirm_del_tariff_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes_del_tariff")
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no_del_tariff")
    ]
])
