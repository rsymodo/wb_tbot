import asyncio
import sqlite3

from aiogram.types import Message

from loader import dp


@dp.message_handler(text=["Финансы"])
async def show_finance(message: Message):
    text = str()
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    finance_info = cs.execute(f"SELECT * FROM finance WHERE user_id={message.from_user.id}")
    finance_info = finance_info.fetchall()
    if finance_info == list():
        msg = await message.answer("Пусто!")
        await asyncio.sleep(1)
        await msg.delete()
        return

    for payment in finance_info:
        part_text = """
🆔: {id_payment}
💰Сумма: {summa} ₽
📜Описание: {description}
🎁Тип: {type_payment}
🛠Статус: {status}
⏱Время: {time_payment}

➖➖➖➖➖➖➖➖➖➖➖➖

        """
        id_payment = payment[0]
        description = payment[2]
        summa = payment[1]
        type_payment = payment[3]
        status = payment[4]
        time_payment = payment[5]
        part_text = part_text.format(id_payment=id_payment, description=description, summa=summa,
                                     type_payment=type_payment,
                                     status=status, time_payment=time_payment)

        text = text + part_text

    await message.answer(text)
