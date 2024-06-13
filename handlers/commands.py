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
	message = State()


# <---------- Start/help commands ---------->
async def message_commandStartOrHelp(message: types.Message):
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


# <---------- Cancel FSM machine ---------->
async def callback_query_cancelFSM(callback_query: types.CallbackQuery, state: FSMContext):
	"""
	Cancel active FSM machine.
	:param callback_query:
	:param state:
	:return:
	"""
	try:
		current_state = await state.get_state()
		if not current_state:
			await callback_query.answer()
			await callback_query.message.delete()

			content = 'Tried to cancel non-active FSM machine.'
		else:
			await state.clear()

			await callback_query.answer(text='Отменено.')
			await callback_query.message.delete()

			kb = InlineKeyboardMarkup(
				inline_keyboard=[
					[InlineKeyboardButton(text='Добавить напоминание', callback_data='add_task')],
					[InlineKeyboardButton(text='Список напоминаний', callback_data='list_task')]
				]
			)

			await callback_query.message.answer(
				text=f'Да-да, <b>{callback_query.from_user.first_name}</b>?',
				reply_markup=kb
			)

			content = 'State aborted.'
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_cancelFSM',
		exception=exception,
		content=content
	)


async def message_cancelFSM(message: types.Message, state: FSMContext):
	"""
	Cancel active FSM machine.
	:param message:
	:param state:
	:return:
	"""
	try:
		current_state = await state.get_state()
		if not current_state:
			await message.delete()

			content = 'Tried to cancel non-active FSM machine.'
		else:
			data = await state.get_data()
			await state.clear()

			for i in range(data['message'], message.message_id + 1):
				try:
					await bot.delete_message(message.from_user.id, message_id=i)
				except:
					pass

			kb = InlineKeyboardMarkup(
				inline_keyboard=[
					[InlineKeyboardButton(text='Добавить напоминание', callback_data='add_task')],
					[InlineKeyboardButton(text='Список напоминаний', callback_data='list_task')]
				]
			)

			await message.answer(
				text=f'Да-да, <b>{message.from_user.first_name}</b>?',
				reply_markup=kb
			)

			content = 'State aborted.'
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_cancelFSM',
		exception=exception,
		content=content
	)


# <---------- Add task ---------->
async def callback_query_addTaskName(callback_query: types.CallbackQuery, state: FSMContext):
	try:
		await callback_query.answer()

		kb = InlineKeyboardMarkup(
			inline_keyboard=[
				[InlineKeyboardButton(text='Отмена',  callback_data='cancel')]
			]
		)

		await callback_query.message.edit_text(
			text=(
				'Укажи название:\n'
				'<i>Оно должно быть уникальным</i>'
			),
			reply_markup=kb
		)

		await state.update_data(message=callback_query.message.message_id)
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


async def message_addTaskTime(message: types.Message, state: FSMContext):
	try:
		data = await state.get_data()

		kb = InlineKeyboardMarkup(
			inline_keyboard=[
				[InlineKeyboardButton(text='Отмена', callback_data='cancel')]
			]
		)

		await message.delete()

		await bot.edit_message_text(
			chat_id=message.from_user.id,
			message_id=data['message'],
			text=(
				f'Название: <b>{message.text}</b>\n'
				'Укажите время: количеством минут\n'
				'<i>Имеется ввиду, через какое время будет срабатывать напоминание</i>'
			),
			reply_markup=kb
		)

		await state.update_data(name=message.text)
		await state.set_state(FSMAddTask.time)

		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_addTaskTime',
		exception=exception,
		content=content
	)


async def message_addTaskLink(message: types.Message, state: FSMContext):
	try:
		data = await state.get_data()

		kb = InlineKeyboardMarkup(
			inline_keyboard=[
				[InlineKeyboardButton(text='Отмена', callback_data='cancel')]
			]
		)

		await message.delete()

		await bot.edit_message_text(
			chat_id=message.from_user.id,
			message_id=data['message'],
			text=(
				f'Название: <b>{data["name"]}</b>\n'
				f'Время: <b>{message.text}</b>\n'
				'Укажите ссылку:\n'
				'<i>Опционально, напишите "нет", чтобы оставить поле пустым</i>'
			),
			reply_markup=kb
		)

		await state.update_data(time=message.text)
		await state.set_state(FSMAddTask.link)

		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_addTaskLink',
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
	router.message.register(
		message_cancelFSM,
		ut_filters.TextEquals(list_ms=['/cancel', 'cancel', 'отмена', '/отмена'], data_type='message'), StateFilter('*')
	)
	router.callback_query.register(callback_query_cancelFSM, F.data == 'cancel', StateFilter('*'))
	router.callback_query.register(callback_query_addTaskName, F.data == 'add_task')
	router.message.register(message_addTaskTime, FSMAddTask.name)
