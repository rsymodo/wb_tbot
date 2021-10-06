import asyncio

from aiogram.types import Message
import sqlite3
from loader import dp


@dp.message_handler(text=["Контакты"])
async def contacts_menu(message: Message):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    con_info = cs.execute(f"SELECT contacts FROM system WHERE name='admin'")
    if con_info is None:
        msg = await message.answer("Пусто!")
        await asyncio.sleep(1)
        await msg.delete()
        return
    con_info = con_info.fetchone()
    if con_info[0] == str():
        msg = await message.answer("Пусто!")
        await asyncio.sleep(1)
        await msg.delete()
        return
    await message.answer(con_info[0])
