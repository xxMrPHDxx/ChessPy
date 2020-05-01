class ArgumentError(BaseException):
	def __init__(self, message):
		self._message = message
	def __str__(self):
		return self._message

class AbstractError(BaseException):
	def __init__(self, _type, _method):
		self._type = _type
		self._method = _method
	def __str__(self):
		return f'Unimplemented method for {self._type}::{self._method}'

class IllegalBoardError(BaseException):
	def __init__(self, message):
		self._message = message
	def __str__(self):
		return f'IllegalBoardError: {self._message}'