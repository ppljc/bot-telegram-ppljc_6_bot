# <---------- Python modules ---------->
from aiogram import types, Router, F
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove


# <---------- Local modules ---------->
from create_bot import bot, db
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'commands.py'


# <---------- Start/help commands ---------->
async def message_commandStartOrHelp(message: types.Message):
	"""
	Triggered by start/help command for registered users.
	:param message:
	:return:
	"""
	try:
		db.add_user(
			user_id=message.from_user.id,
			username=message.from_user.username
		)

		kb = InlineKeyboardMarkup(
			inline_keyboard=[
				[InlineKeyboardButton(text='Добавить напоминание',  callback_data='add_task')],
				[InlineKeyboardButton(text='Список напоминаний', callback_data='list_task')]
			]
		)

		await message.answer(
			text=f'Привет, <b>{message.from_user.first_name}</b>!',
			reply_markup=kb
		)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_commandStartOrHelp_registered',
		exception=exception,
		content=content
	)


def register_handlers(router: Router):
	"""
	Registration of all messages and callback handlers.
	Use router with filter ChatType(['private'])
	:param router:
	:return:
	"""
	router.message.register(
		message_commandStartOrHelp,
		ut_filters.TextEquals(list_ms=['/start', '/help', 'start', 'help', 'старт', 'помощь'], data_type='message')
	)
