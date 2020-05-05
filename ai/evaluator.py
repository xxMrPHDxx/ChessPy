from functools import reduce

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
			lambda value, piece: value + BoardEvaluator.__get_value(piece),
			pieces,
			0
		)
	@staticmethod
	def __calculate_check_bonus(opponent):
		return BoardEvaluator.__CHECK_BONUS if opponent.is_in_check() else 0
	@staticmethod
	def __calculate_check_mate_bonus(opponent, depth):
		if not opponent.is_in_check_mate(): return 0
		return BoardEvaluator.__CHECK_MATE_BONUS * BoardEvaluator.__depth_bonus(depth)
	@staticmethod
	def __get_value(piece):
		return BoardEvaluator.__PIECES_VALUES[str(piece.type)[0].lower()]
	@staticmethod
	def __depth_bonus(depth):
		return 1 if depth == 0 else (depth * BoardEvaluator.__DEPTH_BONUS)
	@staticmethod
	def __castling_bonus(player):
		return BoardEvaluator.__CASTLING_BONUS * player.get_castle_capability()
	# Static variables
	__PIECES_VALUES = {
		'r': 500,
		'n': 300,
		'b': 300,
		'q': 800,
		'k': 10000,
		'p': 100
	}
	__CHECK_BONUS = 50
	__CHECK_MATE_BONUS = 1000
	__DEPTH_BONUS = 10
	__CASTLING_BONUS = 20