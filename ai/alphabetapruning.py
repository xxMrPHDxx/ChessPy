from move import MoveFactory
from player import Alliance
from error import *

def _AlphaBetaPruning__try_move(move, original_board):
	try:
		return move.execute()
	except IllegalBoardError as e:
		return original_board

class AlphaBetaPruning(object):
	def __init__(self, evaluator, depth=4):
		if depth <= 0:
			raise Exception(f'Depth must be greater than 0. Got {depth}!')
		self.__evaluator = evaluator
		self.__depth = depth
	def execute(self, board, depth=None, alpha=-1e10, beta=1e10, maximizing_player=None):
		if depth == None: depth = self.__depth
		if depth == 0 or board.is_game_over():
			return self.__evaluator.evaluate(board, depth)
		best_move = None
		if maximizing_player == None:
			maximizing_player = board.current_player.is_white()
		if maximizing_player:
			max_value = -1e10
			for move in board.current_player.get_legal_moves():
				_board = __try_move(move, board)
				value = self.execute(_board, depth-1, alpha, beta, False)
				max_value = max(max_value, value)
				alpha = max(alpha, max_value)
				if alpha >= beta: break
				if value >= max_value: best_move = move
			return best_move if depth == self.__depth else max_value
		else:
			min_value = 1e10
			for move in board.current_player.get_legal_moves():
				_board = __try_move(move, board)
				value = self.execute(_board, depth-1, alpha, beta, True)
				min_value = min(min_value, value)
				beta = min(beta, min_value)
				if alpha >= beta: break
				if value <= min_value: best_move = move
			return best_move if depth == self.__depth else min_value