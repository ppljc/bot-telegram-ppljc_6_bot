# <---------- Импорт функций Aiogram ---------->
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


# <---------- Импорт локальных функций ---------->
from config import MAIN_TOKEN


# <---------- Основные функции ---------->
storage = MemoryStorage()
exception_data = (0, 0, 0, 0, 0, 0, 0, 0, 0)


bot = Bot(token=MAIN_TOKEN, parse_mode='html', disable_web_page_preview=True)
dp = Dispatcher(storage=storage)
