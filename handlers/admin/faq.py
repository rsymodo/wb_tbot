import sqlite3
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from buttons import faq_edit_markup, confirm_new_text_faq_markup
from loader import dp
from .admin_hub import admin_menu


@dp.callback_query_handler(text="FAQ_admin")
async def edit_faq(call: CallbackQuery, state: FSMContext):
    text = "Введите текст для FAQ:"
    await state.set_state("edit_faq")
    msg = await call.message.edit_text(text, reply_markup=faq_edit_markup)
    await state.update_data(faq_text=msg)
    await call.answer()


@dp.message_handler(content_types=["text"], state="edit_faq")
async def confirm_menu_faq(message: Message, state: FSMContext):  # Если админ решил не принимать новый текст для faq
    text = "Вы уверены,что хотите сохранить этот текст в FAQ?"
    data = await state.get_data()
    faq_text = data["faq_text"]
    await faq_text.delete()
    msg = await message.answer(text, reply_markup=confirm_new_text_faq_markup)
    await state.update_data(confirm_new_faq_msg=msg, new_faq=message.text)


@dp.callback_query_handler(text="no_new_faq", state="edit_faq")
async def new_faq_no_confirmed(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del data["confirm_new_faq_msg"]
    del data["new_faq"]
    await state.reset_state(with_data=True)
    await state.update_data(data)
    await edit_faq(call, state)
    await call.answer()


@dp.callback_query_handler(text="yes_new_faq", state="edit_faq")  # Если админ принял новый текст для faq
async def new_faq_confirmed(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_faq_text = data["new_faq"]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    cs.execute(f"UPDATE system SET faq='{new_faq_text}' WHERE name='admin'")
    connect.commit()
    connect.close()
    await state.reset_state(with_data=True)
    await call.message.delete()
    dsp_msg = await call.message.answer("Готово!")
    await asyncio.sleep(1)
    await dsp_msg.delete()
    await admin_menu(call.message)
    await call.answer()
