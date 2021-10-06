import asyncio
import sqlite3

from aiogram.types import Message

from loader import dp


@dp.message_handler(text=["Корзина"])
async def show_basket(message: Message):
    text = str()
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    email_user = cs.execute(f"SELECT email FROM users WHERE id={message.from_user.id}").fetchone()[0]
    products_in_basket = cs.execute(f"SELECT * FROM basket WHERE user_email='{email_user}'")
    products_in_basket = products_in_basket.fetchall()
    if products_in_basket == list():
        msg = await message.answer("Пусто!")
        await asyncio.sleep(1)
        await msg.delete()
        return

    for product in products_in_basket:
        part_text = """
📜Артикул: <code>{article_number}</code>
➖➖➖➖➖➖➖➖➖➖➖➖
"""
        article_number = product[1]
        part_text = part_text.format(article_number=article_number)
        text = text + part_text

    await message.answer(text)

