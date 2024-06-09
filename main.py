# <---------- Импорт функций ---------->
import asyncio


# <---------- Импорт локальных функций ---------->
from create_bot import dp, bot, db
from utilities import ut_logger
from handlers.routers import *
from handlers import commands


# <---------- Переменные ---------->
filename = 'main.py'


# <---------- Функции on_startup и on_shutdown ---------->
async def on_startup():
	if db:
		print('- - - Database is connected - - -\n')
	if ut_logger.start_logger():
		print('- - - Logger is created - - -\n')
	print('- - - Reminder is online - - -\n')


async def on_shutdown():
	print('\nGoodbye...')


# <---------- Запуск бота ---------->
async def main():
	dp.startup.register(on_startup)
	dp.shutdown.register(on_shutdown)

	dp.include_routers(
		router_base
	)

	commands.register_handlers(router=router_base)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)

if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
