from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# FAQ
# Контакты
# Отключить бота
# Приостановить выкупы
# Информация о боте
# Поиск профиля
# Рассылка
# Поиск выкупов
# Платежные системы

admin_hub_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="FAQ", callback_data="FAQ_admin"),
        InlineKeyboardButton(text="Контакты", callback_data="contacts_admin")
    ],
    [
        InlineKeyboardButton(text="Отключить бота", callback_data="disable_bot"),
        InlineKeyboardButton(text="Тарифы", callback_data="management_tariff")
    ],
    [
        InlineKeyboardButton(text="Приостановить выкупы", callback_data="buyout_status")
    ],
    [
        InlineKeyboardButton(text="О боте", callback_data="about_bot_admin"),
        InlineKeyboardButton(text="Поиск профиля", callback_data="search_profile")
    ],
    [
        InlineKeyboardButton(text="Рассылка", callback_data="mailing"),
        InlineKeyboardButton(text="Поиск выкупов", callback_data="search_buyout")
    ],
    [
        InlineKeyboardButton(text="Платежные системы", callback_data="payment_system"),
        InlineKeyboardButton(text="Закрыть", callback_data="close_admin_panel")
    ]
])
