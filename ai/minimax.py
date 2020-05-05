from move import MoveFactory
from player import Alliance

def _MiniMax__is_game_over(board):
	return board.current_player.is_in_check_mate() or board.current_player.is_in_stale_mate()

class MiniMax(object):
	def __init__(self, evaluator):
		self.__evaluator = evaluator
	# Default methods
	def execute(self, board, depth):
		if depth == 0 or __is_game_over(board):
			return self.__evaluator.evaluate(board, depth)
		min_value, max_value = [sign * 1e10 for sign in [1, -1]]
		best_move = None
		is_white = board.current_player.alliance == Alliance.White
		for move in board.current_player.get_legal_moves():
			next_board = move.execute()
			value = (self.__min if is_white else self.__max)(next_board, depth-1)
			if is_white and value > max_value:
				max_value, best_move = value, move
			elif not is_white and value < min_value:
				min_value, best_move = value, move
		return best_move
	def __min(self, board, depth):
		if depth == 0 or __is_game_over(board):
			return self.__evaluator.evaluate(board, depth)
		min_value = 1e10
		for move in board.current_player.get_legal_moves():
			try:
				next_board = move.execute()
				value = self.__max(next_board, depth-1)
				if value < min_value: min_value = value
			except: pass
		return min_value
	def __max(self, board, depth):
		if depth == 0 or __is_game_over(board):
			return self.__evaluator.evaluate(board, depth)
		max_value = -1e10
		for move in board.current_player.get_legal_moves():
			try:
				next_board = move.execute()
				value = self.__min(next_board, depth-1)
				if value > max_value: max_value = value
			except: pass
		return max_value