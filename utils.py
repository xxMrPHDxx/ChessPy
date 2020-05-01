def _is_row(position, row):
	return int(position / 8) == row

def _is_column(position, col):
	return position % 8 == col

class BoardUtils(object):
	def __init__(self):
		raise Exception('Error: Not instantiable!')
	@staticmethod
	def is_valid(position):
		return position >= 0 and position < 64
	@staticmethod
	def is_first_row(position): return _is_row(position, 0)
	@staticmethod
	def is_second_row(position): return _is_row(position, 1)
	@staticmethod
	def is_seventh_row(position): return _is_row(position, 6)
	@staticmethod
	def is_eighth_row(position): return _is_row(position, 7)
	@staticmethod
	def is_first_column(position): return _is_column(position, 0)
	@staticmethod
	def is_second_column(position): return _is_column(position, 1)
	@staticmethod
	def is_seventh_column(position): return _is_column(position, 6)
	@staticmethod
	def is_eighth_column(position): return _is_column(position, 7)