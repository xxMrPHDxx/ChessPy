from functools import reduce

__PIECES_VALUES = {
	'r': 500,
	'n': 300,
	'b': 300,
	'q': 800,
	'k': 10000,
	'p': 100
}

_BoardEvaluator__CHECK_BONUS = 90
_BoardEvaluator__CHECK_MATE_BONUS = 1000
_BoardEvaluator__DEPTH_BONUS = 10

def _BoardEvaluator__get_value(piece):
	return __PIECES_VALUES[str(piece.type)[0].lower()]

def _BoardEvaluator__depth_bonus(depth):
	return 1 if depth == 0 else (depth * __DEPTH_BONUS)

class Evaluator(object):
	def evaluate(self, board, depth):
		raise Exception(f'Unimplemented abstract method Evaluator::evaluate!')

class BoardEvaluator(Evaluator):
	# Default methods
	def evaluate(self, board, depth):
		white_score = BoardEvaluator.__player_score(board, board.white_player, depth)
		black_score = BoardEvaluator.__player_score(board, board.black_player, depth)
		return white_score - black_score
	# Private static methods
	@staticmethod
	def __player_score(board, player, depth):
		opponent = board.get_opponent() if board.current_player == player else board.current_player
		return BoardEvaluator.__calculate_piece_values(player.get_active_pieces()) + \
				BoardEvaluator.__calculate_check_bonus(opponent) + \
				BoardEvaluator.__calculate_check_mate_bonus(opponent, depth)
				
	@staticmethod
	def __calculate_piece_values(pieces):
		return reduce(
			lambda value, piece: value + __get_value(piece),
			pieces,
			0
		)
	@staticmethod
	def __calculate_check_bonus(opponent):
		return __CHECK_BONUS if opponent.is_in_check() else 0
	@staticmethod
	def __calculate_check_mate_bonus(opponent, depth):
		return (__CHECK_MATE_BONUS * __depth_bonus(depth)) if opponent.is_in_check_mate() else 0