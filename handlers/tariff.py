import asyncio
import sqlite3
from buttons import method_payment_markup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp


@dp.message_handler(text=["Тарифы"])
async def tariff_menu(message: Message):
    text = "Активные тарифы:"
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    all_tariff = cs.execute("SELECT * FROM tariff")
    all_tariff = all_tariff.fetchall()
    if all_tariff == list():
        msg = await message.answer("На данный момент тарифов нет!")
        await asyncio.sleep(0.7)
        await msg.delete()
        return
    all_tariff_markup = InlineKeyboardMarkup()
    for tariff in all_tariff:
        name = tariff[1]
        price = tariff[3]
        count = tariff[-1]
        all_tariff_markup.add(InlineKeyboardButton(text=f"{name} | {price + '₽'} | Кол-во выкупов: {count} шт.",
                                                   callback_data=f"tariff_{tariff[0]}"))
    all_tariff_markup.add(InlineKeyboardButton(text="Закрыть", callback_data="close_tariff"))
    await message.answer(text, reply_markup=all_tariff_markup)


@dp.callback_query_handler(text="cancel_payment")
@dp.callback_query_handler(text="close_tariff")
async def close_tariff_func(call: CallbackQuery):
    await call.message.delete()
    await call.answer()


@dp.callback_query_handler(text="back_to_choose_tarif")
async def back_to_active_tariff(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.reset_state(with_data=True)
    await tariff_menu(call.message)
    await call.answer()


# -----------------------------------------
# ----------ЭТАПЫ ПОКУПКИ ТАРИФА-----------


@dp.callback_query_handler(lambda x: "tariff_" in x.data)
async def choose_payment_method(call: CallbackQuery, state: FSMContext):
    text = "Выберете способ оплаты:"
    tariff_id = call.data.split("_")[1]
    await state.update_data(tariff_id=tariff_id)
    await call.message.edit_text(text, reply_markup=method_payment_markup)
    await call.answer()


@dp.callback_query_handler(text="qiwi_payment")
async def qiwi_payment_menu(call: CallbackQuery, state: FSMContext):
    text = """
📃 <b>Тариф:</b>  {name}
💰 <b>Цена:</b> {price} ₽  
📃 <b>Описание</b>: ->
{description}
➖➖➖➖➖➖➖➖➖➖➖➖

<b>Кол-во выкупов</b>: {count_buyout}
Выбран способ оплаты через QIWI
"""
    data = await state.get_data()
    tariff_id = data["tariff_id"]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    tariff_info = cs.execute(f"SELECT * FROM tariff WHERE id={int(tariff_id)}")
    tariff_info = tariff_info.fetchone()
    name = tariff_info[1]
    description = tariff_info[2]
    price = tariff_info[3]
    count_buyout = tariff_info[-1]
    text = text.format(name=name, description=description, price=price, count_buyout=count_buyout)
    qiwi_payment_markup = InlineKeyboardMarkup()
    qiwi_payment_markup.add(
        InlineKeyboardButton(text="Перейти к оплате", url="https://www.google.com"))  # ССЫЛКА НА ОПЛАТУ
    qiwi_payment_markup.add(InlineKeyboardButton(text="Проверить оплату", callback_data="check_payment_qiwi"))
    qiwi_payment_markup.add(InlineKeyboardButton(text="Отмена", callback_data="cancel_payment"))
    await call.message.edit_text(text, reply_markup=qiwi_payment_markup)
    await call.answer()
