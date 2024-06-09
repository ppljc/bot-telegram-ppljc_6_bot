# <---------- Импорт функций Aiogram ---------->
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


# <---------- Импорт локальных функций ---------->
from config import MAIN_TOKEN
from database.sqlite_db import Database


# <---------- Основные функции ---------->
db = Database()
bot = Bot(token=MAIN_TOKEN, default=DefaultBotProperties(parse_mode='html', link_preview_is_disabled=True))
dp = Dispatcher(storage=MemoryStorage())
