import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import dp
from buttons import start_registration_markup, hub_markup, get_number_markup
import asyncio


@dp.message_handler(CommandStart())
async def hello_user(message: Message, state: FSMContext):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    user = cs.execute(f"SELECT id FROM users WHERE id={message.from_user.id}")
    user = user.fetchone()
    if user is None:
        text = """ТЕКСТ ПРИВЕТСТВИЯ"""
        msg = await message.answer(text, reply_markup=start_registration_markup)
        await state.update_data(first_msg=msg)
        return
    del user
    connect.close()
    text = "МЕНЮ"
    await message.answer(text, reply_markup=hub_markup)


@dp.callback_query_handler(text="start_registration")
async def get_number(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = data["first_msg"]
    await msg.delete()
    text = "Предоставьте нам ваш номер телефона:"
    await state.set_state("get_number")
    msg = await call.message.answer(text, reply_markup=get_number_markup)
    await state.update_data(get_number_msg=msg)
    await call.answer()


@dp.message_handler(state="get_number", content_types=["contact"])
async def get_email(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = data["get_number_msg"]
    await msg.delete()
    text = "Предоставьте нам ваш email:"
    await state.update_data(phone_number_reg=message.contact.phone_number)
    await state.set_state("get_email")
    msg = await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await state.update_data(get_email_msg=msg)


@dp.message_handler(state="get_email", content_types=["text"],
                    regexp="^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$")
async def end_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = data["get_email_msg"]
    phone_number = data["phone_number_reg"]
    if "+" in phone_number:
        phone_number = phone_number[1:]
    email = message.text
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    email_check = cs.execute(f"SELECT email FROM users WHERE email='{email}'").fetchone()
    if email_check is not None:
        msg = await message.answer("Данный email уже зарегистрирован!Повторите попытку.")
        await asyncio.sleep(1)
        await msg.delete()
        return
    cs.execute(
        f"INSERT INTO users(id,number,email,buyouts,TA_buyouts) VALUES({int(message.from_user.id)},'{phone_number}','{email}',{0},{0})")
    connect.commit()
    connect.close()
    await msg.delete()
    await state.reset_state(with_data=True)
    await hello_user(message, state)


@dp.message_handler(state="get_email", content_types=["text"])
async def invalid_email(message: Message, state: FSMContext):
    msg = await message.answer("Некорректный адрес электронной почты!Повторите попытку.")
    await asyncio.sleep(1)
    await msg.delete()
