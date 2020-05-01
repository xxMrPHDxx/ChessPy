from error import *

class Alliance(object):
	def __init__(self, _name):
		self._name = _name
	def __str__(self):
		return str(self._name)

Alliance.White = Alliance('White')
Alliance.Black = Alliance('Black')

class Player(object):
	def __init__(self, ally, board, moves, opponent_moves):
		from piece import Piece
		self._ally = ally
		self._board = board
		self._pieces = board._white_pieces if ally == Alliance.White else board._black_pieces
		self._moves = moves
		self._king = None
		for piece in self._pieces:
			if piece.is_king(): self._king = piece
		if self._king == None:
			raise IllegalBoardError('No king found!')
	# Properties and getters
	@property
	def board(self): return self._board
	# Default methods
	def get_legal_moves(self): return self._moves
	# Overrides
	def __str__(self):
		return f'{str(self._ally)}Player[{len(self._pieces)} pieces, {len(self._moves)} moves]'