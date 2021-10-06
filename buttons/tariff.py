from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

method_payment_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="QIWI", callback_data="qiwi_payment")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_choose_tarif")
    ]
])

