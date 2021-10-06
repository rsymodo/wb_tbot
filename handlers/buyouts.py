import asyncio
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from buttons import cancel_search_product_markup
import requests
from fake_useragent import UserAgent
from .register import hello_user

from loader import dp


@dp.message_handler(text=["Выкупы"])
async def write_article_number(message: Message, state: FSMContext):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    status = cs.execute("SELECT buyout_status FROM system WHERE name='admin'")
    status = int(status.fetchone()[0])
    if status == 0:
        text = "Выкупы приостановлены!"
        msg = await message.answer(text)
        await asyncio.sleep(1)
        await msg.delete()
        return
    text = "Введите артикул:"
    await state.set_state("search_product")
    await message.answer(text, reply_markup=cancel_search_product_markup)


@dp.message_handler(text=["Отмена"], state="search_product")
async def cancel_search_product(message: Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await hello_user(message, state)


@dp.message_handler(content_types=["text"], state="search_product")
async def show_product(message: Message, state: FSMContext):
    HEADERS = {
        "user-agent": UserAgent().random
    }
    article_number = message.text
    url = f"https://www.wildberries.ru/catalog/{article_number}/detail.aspx?targetUrl=SP"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        msg = await message.answer("Товар не найден!Повторите попытку.")
        await asyncio.sleep(0.8)
        await msg.delete()
        return

