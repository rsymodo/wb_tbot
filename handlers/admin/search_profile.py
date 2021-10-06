import asyncio

from aiogram.dispatcher import FSMContext
from buttons import type_search_profile, faq_edit_markup, back_to_category_TSP
from loader import dp
from aiogram.types import CallbackQuery, Message
import sqlite3

profile_text = """
ID: {user_id}
Номер телефона: {phone_number}
Email: {email}
Кол-во выкупов: {buyouts}
Общая сумма выкупов: {TA_buyouts}

"""


@dp.callback_query_handler(text="search_profile")
async def search_profile(call: CallbackQuery, state: FSMContext):
    text = "Поиск пользователей"
    await state.set_state("choose_type_search_profile")
    await call.message.edit_text(text, reply_markup=type_search_profile)
    await call.answer()


@dp.callback_query_handler(text="search_with_email", state="choose_type_search_profile")
async def search_profile_with_email(call: CallbackQuery, state: FSMContext):
    text = "Введите email пользователя:"
    await state.set_state("search_profile_with_email")
    msg = await call.message.edit_text(text, reply_markup=back_to_category_TSP)
    await state.update_data(write_email_user_msg=msg)
    await call.answer()


@dp.callback_query_handler(text="search_with_id", state="choose_type_search_profile")
async def search_profile_with_id(call: CallbackQuery, state: FSMContext):
    text = "Введите ID пользователя:"
    await state.set_state("search_profile_with_id")
    msg = await call.message.edit_text(text, reply_markup=back_to_category_TSP)
    await state.update_data(write_id_user_msg=msg)
    await call.answer()


@dp.callback_query_handler(text="search_with_number", state="choose_type_search_profile")
async def search_profile_with_number(call: CallbackQuery, state: FSMContext):
    text = """
Введите номер телефона пользователя без "+"
Пример(РФ): 79998125678
    """
    await state.set_state("search_profile_with_number")
    msg = await call.message.edit_text(text, reply_markup=back_to_category_TSP)
    await state.update_data(write_number_user_msg=msg)
    await call.answer()


@dp.callback_query_handler(text="back_to_TSP", state="search_profile_with_number")
@dp.callback_query_handler(text="back_to_TSP", state="search_profile_with_id")
@dp.callback_query_handler(text="back_to_TSP", state="search_profile_with_email")
async def back_to_TSP_func(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await search_profile(call, state)


@dp.message_handler(content_types=["text"], state="search_profile_with_email")
async def result_search_with_email(message: Message, state: FSMContext):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    profile_info = cs.execute(f"SELECT * FROM users WHERE email='{message.text}'")
    profile_info = profile_info.fetchone()
    if profile_info is None:
        msg = await message.answer("Пользователь не найден!Повторите попытку:")
        await asyncio.sleep(1)
        await msg.delete()
        return
    text = profile_text
    text = text.format(user_id=profile_info[0], phone_number=profile_info[1], email=message.text,
                       buyouts=profile_info[3], TA_buyouts=profile_info[4])

    data = await state.get_data()
    write_email_user_msg = data["write_email_user_msg"]
    await write_email_user_msg.delete()
    await message.answer(text, reply_markup=faq_edit_markup)


@dp.message_handler(content_types=["text"], state="search_profile_with_id")
async def result_search_with_id(message: Message, state: FSMContext):
    try:
        int(message.text)
    except Exception:
        msg = await message.answer("Некорректный ID!Повторите попытку.")
        await asyncio.sleep(0.8)
        await msg.delete()
        return
    else:
        connect = sqlite3.connect("./database.sqlite3")
        cs = connect.cursor()
        profile_info = cs.execute(f"SELECT * FROM users WHERE id={int(message.text)}")
        profile_info = profile_info.fetchone()
        if profile_info is None:
            msg = await message.answer("Пользователь не найден!Повторите попытку:")
            await asyncio.sleep(1)
            await msg.delete()
            return
        text = profile_text
        text = text.format(user_id=message.text, phone_number=profile_info[1], email=profile_info[2],
                           buyouts=profile_info[3], TA_buyouts=profile_info[4])

        data = await state.get_data()
        write_id_user_msg = data["write_id_user_msg"]
        await write_id_user_msg.delete()
        await message.answer(text, reply_markup=faq_edit_markup)


@dp.message_handler(content_types=["text"], state="search_profile_with_number")
async def result_search_with_number(message: Message, state: FSMContext):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    profile_info = cs.execute(f"SELECT * FROM users WHERE number='{message.text}'")
    profile_info = profile_info.fetchone()
    if profile_info is None:
        msg = await message.answer("Пользователь не найден!Повторите попытку:")
        await asyncio.sleep(1)
        await msg.delete()
        return
    text = profile_text
    text = text.format(user_id=profile_info[0], phone_number=profile_info[1], email=profile_info[2],
                       buyouts=profile_info[3], TA_buyouts=profile_info[4])

    data = await state.get_data()
    write_number_user_msg = data["write_number_user_msg"]
    await write_number_user_msg.delete()
    await message.answer(text, reply_markup=faq_edit_markup)
