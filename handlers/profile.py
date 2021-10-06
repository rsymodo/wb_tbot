from aiogram.types import Message, CallbackQuery
import sqlite3
from loader import dp
from buttons import close_profile_markup


@dp.message_handler(text=["Профиль"])
async def profile_text(message: Message):
    text = """
Имя: {name}
Номер телефона: {phone_number}
Email: {email}
Кол-во выкупов: {buyouts}
Общая сумма выкупов: {TA_buyouts}

    """
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    info_user = cs.execute(f"SELECT * FROM users WHERE id={message.from_user.id}")
    info_user = info_user.fetchone()
    name = message.from_user.first_name
    phone = info_user[1]
    email = info_user[2]
    buyouts = info_user[3]
    ta_buyouts = info_user[4]
    text = text.format(name=name, phone_number=phone, email=email, buyouts=buyouts, TA_buyouts=ta_buyouts)
    await message.answer(text, reply_markup=close_profile_markup)


@dp.callback_query_handler(text="close_profile")
async def close_profile_text(call: CallbackQuery):
    await call.message.delete()
    await call.answer()
