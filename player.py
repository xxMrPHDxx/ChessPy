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
		self.__in_check = len(Player.calculate_attacks_on_tile(opponent_moves, self._king.position)) > 0
	# Properties and getters
	@property
	def board(self): return self._board
	@property
	def alliance(self): return self._ally
	@property
	def active_pieces(self): return self._pieces
	# Default methods
	def get_legal_moves(self): return self._moves
	def get_active_pieces(self): return self._pieces
	def is_in_check(self):
		return self.__in_check
	def is_in_check_mate(self):
		return self.__in_check and not Player.has_escape_moves(self)
	def is_in_stale_mate(self):
		return not self.__in_check and not Player.has_escape_moves(self)
	# Overrides
	def __eq__(self, other):
		if not isinstance(other, Player): return False
		return all([
			str(self) == str(other),
			len(self.active_pieces) == len(other.active_pieces),
			all([self.active_pieces[i] == other.active_pieces[i] for i in range(len(self.active_pieces))])
		])
	def __str__(self):
		return f'{str(self._ally)}Player[{len(self._pieces)} pieces, {len(self._moves)} moves]'
	# Static methods
	@staticmethod
	def calculate_attacks_on_tile(opponent_moves, destination):
		attack_moves = []
		for move in opponent_moves:
			if move.is_attack_move() and move.destination == destination:
				attack_moves.append(move)
		return attack_moves
	@staticmethod
	def has_escape_moves(player):
		escape_moves = []
		for move in player.get_legal_moves():
			try:
				board = move.execute()
				if board.get_opponent().is_in_check(): 
					del board
					continue
				del board
				escape_moves.append(move)
			except: pass
		return len(escape_moves) > 0