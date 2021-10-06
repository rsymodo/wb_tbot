import asyncio
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from buttons import faq_edit_markup

from loader import dp


@dp.callback_query_handler(text="search_buyout")
async def write_id_payment(call: CallbackQuery, state: FSMContext):
    text = "Введите ID платежа:"
    await state.set_state("write_id_payment")
    msg = await call.message.edit_text(text, reply_markup=faq_edit_markup)
    await state.update_data(search_buyout_msg=msg)
    await call.answer()


@dp.message_handler(content_types=["text"], state="write_id_payment")
async def show_result_search_buyout(message: Message, state: FSMContext):
    try:
        int(message.text)
    except Exception:
        msg = await message.answer("Неверный формат ID платежа!Повторите попытку.")
        await asyncio.sleep(0.8)
        await msg.delete()
        return
    else:
        connect = sqlite3.connect("./database.sqlite3")
        cs = connect.cursor()
        payment_info = cs.execute(f"SELECT * FROM finance WHERE id={int(message.text)}")
        payment_info = payment_info.fetchone()
        if payment_info is None:
            msg = await message.answer("Несуществующий ID платежа!Повторите попытку.")
            await asyncio.sleep(0.8)
            await msg.delete()
            return
        text = """
🆔: {id_payment}
💰Сумма: {summa} ₽
📜Описание: {description}
🎁Тип: {type_payment}
🛠Статус: {status}
⏱Время: {time_payment}
👨ID пользователя: {user_id} """.format(id_payment=payment_info[0], summa=payment_info[1], description=payment_info[2],
                                        type_payment=payment_info[3], status=payment_info[4],
                                        time_payment=payment_info[5], user_id=payment_info[-1])
        data = await state.get_data()
        search_buyout_msg = data["search_buyout_msg"]
        await search_buyout_msg.delete()
        await message.answer(text, reply_markup=faq_edit_markup)
