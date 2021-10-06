import asyncio

from aiogram.types import Message
import sqlite3
from loader import dp


@dp.message_handler(text=["FAQ"])
async def faq_menu(message: Message):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    faq_info = cs.execute(f"SELECT faq FROM system WHERE name='admin'")
    if faq_info is None:
        msg = await message.answer("Пусто!")
        await asyncio.sleep(1)
        await msg.delete()
        return
    faq_info = faq_info.fetchone()
    if faq_info[0] == str():
        msg = await message.answer("Пусто!")
        await asyncio.sleep(1)
        await msg.delete()
        return
    await message.answer(faq_info[0])



