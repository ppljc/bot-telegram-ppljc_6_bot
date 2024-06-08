# <---------- Импорт сторонних функций  ---------->
import asyncio


# <---------- Импорт локальных функций ---------->
from create_bot import dp, bot


# <---------- Переменные ---------->
filename = 'main.py'


# <---------- Функции on_startup и on_shutdown ---------->
async def on_startup():
	"""
	Initializing all connections.
	"""
	print('\n- - - HomeWorker is online - - -')
	print()


async def on_shutdown():
	print()
	print('Goodbye...')


# <---------- Основные функции ---------->


# <---------- Запуск бота ---------->
async def main():
	dp.startup.register(on_startup)
	dp.shutdown.register(on_shutdown)
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)

if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
