import asyncio
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from buttons import faq_contacts_markup, confirm_contacts_markup
from handlers.admin.admin_hub import admin_menu

from loader import dp


@dp.callback_query_handler(text="contacts_admin")
async def edit_contacts(call: CallbackQuery, state: FSMContext):
    text = 'Введите текст для "Контакты":'
    await state.set_state("edit_contacts")
    msg = await call.message.edit_text(text, reply_markup=faq_contacts_markup)
    await state.update_data(contacts_text=msg)
    await call.answer()


@dp.message_handler(content_types=["text"], state="edit_contacts")
async def confirm_menu_contacts(message: Message,
                                state: FSMContext):  # Если админ решил не принимать новый текст для "Контакты"
    text = 'Вы уверены,что хотите сохранить этот текст в "Контакты"?'
    data = await state.get_data()
    faq_text = data["contacts_text"]
    await faq_text.delete()
    msg = await message.answer(text, reply_markup=confirm_contacts_markup)
    await state.update_data(confirm_new_contacts_msg=msg, new_contacts=message.text)


@dp.callback_query_handler(text="no_new_contacts", state="edit_contacts")
async def new_contacts_no_confirmed(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del data["confirm_new_contacts_msg"]
    del data["new_contacts"]
    await state.reset_state(with_data=True)
    await state.update_data(data)
    await edit_contacts(call, state)
    await call.answer()


@dp.callback_query_handler(text="yes_new_contacts",
                           state="edit_contacts")  # Если админ принял новый текст для "Контакты"
async def new_contacts_confirmed(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_faq_text = data["new_contacts"]
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    cs.execute(f"UPDATE system SET contacts='{new_faq_text}' WHERE name='admin'")
    connect.commit()
    connect.close()
    await state.reset_state(with_data=True)
    await call.message.delete()
    dsp_msg = await call.message.answer("Готово!")
    await asyncio.sleep(1)
    await dsp_msg.delete()
    await admin_menu(call.message)
    await call.answer()
