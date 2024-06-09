# <---------- Python modules ---------->
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


# <---------- Variables ---------->
filename = 'ut_filters.py'
__all__ = ['TextEquals']


# <---------- Filter classes ---------->
class TextEquals(BaseFilter):
	"""
	Checks if message.text matches one of the elements of the given list.
	"""

	def __init__(self, list_ms: list[str], data_type: str) -> None:
		"""
		:param list_ms: List of a message
		:param data_type: message, callback_query
		"""
		self.list_ms = list_ms
		self.data_type = data_type

	async def __call__(self, data: Message or CallbackQuery) -> bool:
		"""
		:param data: Aiogram message or callback_query object
		:return: True if message.text in a given list
		"""
		result = False
		if self.data_type == 'message':
			result = False
			if data.text.lower() in self.list_ms:
				result = True
		elif self.data_type == 'callback_query':
			result = False
			if data.data.lower() in self.list_ms:
				result = True
		print(f'TextEquals to {self.list_ms} >> {result}')
		return result
