import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import sqlite3
from buttons import confirm_change_status_buyout_markup
from .admin_hub import admin_menu

from loader import dp


async def new_status_buyouts(call: CallbackQuery, state: FSMContext, new_status: int):
    data = await state.get_data()
    confirm_change_BS_msg = data["confirm_change_BS_msg"]
    await confirm_change_BS_msg.delete()
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    cs.execute(f"UPDATE system SET buyout_status={new_status} WHERE name='admin'")
    connect.commit()
    await state.reset_state(with_data=True)
    msg = await call.message.answer("Готово!")
    await asyncio.sleep(0.7)
    await msg.delete()
    await admin_menu(call.message)


@dp.callback_query_handler(text="buyout_status")
async def confirm_change_status_buyout(call: CallbackQuery, state: FSMContext):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    status = cs.execute("SELECT buyout_status FROM system WHERE name='admin'")
    status = int(status.fetchone()[0])
    if status == 1:
        await state.set_state("change_confirm_zero")
        text = "Вы точно хотите приостановить выкупы?"
    else:
        await state.set_state("change_confirm_one")
        text = "Вы точно хотите включить выкупы?"

    msg = await call.message.edit_text(text, reply_markup=confirm_change_status_buyout_markup)
    await state.update_data(confirm_change_BS_msg=msg)
    await call.answer()


@dp.callback_query_handler(text="no_change_status_buyout", state="change_confirm_one")
@dp.callback_query_handler(text="no_change_status_buyout", state="change_confirm_zero")
async def cancel_change_buyout_status(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await call.message.delete()
    await admin_menu(call.message)
    await call.answer()


@dp.callback_query_handler(text="yes_change_status_buyout", state="change_confirm_zero")
async def new_status_buyouts_zero(call: CallbackQuery, state: FSMContext):
    await new_status_buyouts(call, state, 0)
    await call.answer()


@dp.callback_query_handler(text="yes_change_status_buyout", state="change_confirm_one")
async def new_status_buyouts_one(call: CallbackQuery, state: FSMContext):
    await new_status_buyouts(call, state, 1)
    await call.answer()
