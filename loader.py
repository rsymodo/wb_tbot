from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

# 2033363273:AAGuGa7HEzNo0JVYkZDWFjcnD4ON6Siw3UY
TOKEN = "2033363273:AAGuGa7HEzNo0JVYkZDWFjcnD4ON6Siw3UY"
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ADMINS = [
    2040691054,
    164704762
]

# 2026087442:AAGr8dIR39YE1WARF4sMfvxNDCTKgpOhGdE
