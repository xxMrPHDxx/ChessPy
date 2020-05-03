class Stack(object):
	def __init__(self):
		self.__items = []
	# Default methods
	def push(self, item):
		self.__items.append(item)
	def pop(self):
		if len(self.__items) <= 0: return False
		del self.__items[-1]
		return True
	def peek(self):
		if len(self.__items) == 0: return
		return self.__items[len(self.__items)-1]
	# Overrides
	def __getitem__(self, index):
		return self.__items[index]
	def __iter__(self):
		return self.__items.__iter__()