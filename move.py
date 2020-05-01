from error import *
from player import Alliance

class Move(object):
	def __init__(self, board, piece, dest, attacked_piece):
		self._board = board
		self._piece = piece
		self._dest = dest
		self._attacked_piece = attacked_piece
	# Properties and getters
	@property
	def board(self): return self._board
	@property
	def piece(self): return self._piece
	@property
	def destination(self): return self._dest
	@property
	def attacked_piece(self): return self._attacked_piece
	# Default Methods
	def is_attack_move(self): return self.attacked_piece != None
	# Abstract methods
	def execute(self, override=False): 
		if not override: raise AbstractError(type(self), 'execute')
		from board import Board
		return Board.Builder()
	# Overrides
	def __str__(self):
		_type = str(type(self)).split('.')[-1].split('\'')[0]
		_extra = '' if not self.is_attack_move() else str(self.attacked_piece)
		return f'{_type}[{str(self.piece)}{self.destination}{_extra}]'

class MajorMove(Move):
	def __init__(self, board, piece, dest):
		Move.__init__(self, board, piece, dest, None)
	def execute(self):
		builder = Move.execute(self, True)
		for piece in self.board.get_all_pieces():
			if piece == self.piece: continue
			builder.set_piece(piece)
		return builder. \
			set_piece(self.piece.move_piece(self.destination)). \
			set_move_maker(self.piece.get_opponent()). \
			build()

class AttackMove(Move):
	def __init__(self, board, piece, dest, attacked_piece):
		Move.__init__(self, board, piece, dest, attacked_piece)
	def execute(self):
		builder = Move.execute(self, True)

		return builder. \
			set_piece(self.piece.move_piece(self.destination)). \
			set_move_maker(self.piece.get_opponent()). \
			build()