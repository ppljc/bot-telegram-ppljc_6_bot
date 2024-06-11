# <---------- Python modules ---------->
from aiogram import types, Router, F
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# <---------- Local modules ---------->
from create_bot import bot, db
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'commands.py'


# <---------- FSM machine ---------->
class FSMAddTask(StatesGroup):
	name = State()
	link = State()
	time = State()


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
		function='message_commandStartOrHelp',
		exception=exception,
		content=content
	)


async def callback_query_addTaskName(callback_query: types.CallbackQuery, state: FSMContext):
	try:
		await callback_query.answer()
		await callback_query.message.answer(
			text=(
				"Укажи название для своего нового напоминания:\n"
				"<i>Оно должно быть уникальным</i>"
			)
		)
		await callback_query.message.delete()
		await state.set_state(FSMAddTask.name)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_addTaskName',
		exception=exception,
		content=content
	)


async def callback_query_addTaskTime(callback_query: types.CallbackQuery, state: FSMContext):
	try:
		await callback_query.answer()
		await callback_query.message.answer(
			text=(
				"Укажи время для своего нового напоминания:\n"
				"<i>Имеется ввиду, через сколько будет срабатывать напоминание</i>"
			)
		)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_addTaskTime',
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
