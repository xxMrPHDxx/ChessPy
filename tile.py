from error import *

class Tile(object):
	def __init__(self, pos):
		from piece import Piece
		if not isinstance(pos, int) and not isinstance(pos, Piece):
			raise ArgumentError(f'Argument 1 is not a number or a Piece object. Got {type(pos)}!')
		self._piece = pos if isinstance(pos, Piece) else None
		self._pos = pos if not isinstance(pos, Piece) else pos.position
	# Properties & getters
	@property
	def piece(self): return self._piece
	@property
	def position(self): return self._pos
	# Default methods
	def is_empty(self):
		return self._piece == None
	# Overrides
	def __str__(self):
		return '-' if self._piece == None else str(self._piece)