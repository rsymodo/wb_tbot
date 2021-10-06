from aiogram.types import CallbackQuery
import sqlite3
from buttons import faq_edit_markup
from loader import dp


@dp.callback_query_handler(text="about_bot_admin")
async def info_about_bot(call: CallbackQuery):
    connect = sqlite3.connect("./database.sqlite3")
    cs = connect.cursor()
    info_bot = cs.execute(f"SELECT count_all_buyouts,balance_system FROM system WHERE name='admin'")
    info_bot = info_bot.fetchone()
    count_all_buyouts = info_bot[0]
    balance_system = info_bot[1]
    count_users = cs.execute(f"SELECT id FROM users")
    count_users = len(count_users.fetchall())
    text = f"""
Количество пользователей: {count_users}
Средств в системе: {balance_system}₽
Сделано выкупов: {count_all_buyouts}
    """
    await call.message.edit_text(text, reply_markup=faq_edit_markup)
