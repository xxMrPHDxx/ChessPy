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
	def position(self): return self._piece.position
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
	def __getitem__(self, prop):
		if prop == 'board': return self.board
		if prop == 'piece': return self.piece
		if prop == 'destination': return self.destination
		if prop == 'attacked_piece': return self.attacked_piece
	def __eq__(self, other):
		if not isinstance(other, Move): return False
		return all([
			self[prop] == other[prop] 
			for prop in ['board', 'piece', 'destination', 'attacked_piece']
		])
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
		return builder \
			.set_piece(self.piece.move_piece(self.destination)) \
			.set_move_maker(self.piece.get_opponent()) \
			.build()

class AttackMove(Move):
	def __init__(self, board, piece, dest, attacked_piece):
		Move.__init__(self, board, piece, dest, attacked_piece)
	def execute(self):
		builder = Move.execute(self, True)
		for piece in self.board.get_all_pieces():
			if piece == self.piece or piece == self.attacked_piece: continue
			builder.set_piece(piece)
		return builder \
			.set_piece(self.piece.move_piece(self.destination)) \
			.set_move_maker(self.piece.get_opponent()) \
			.build()

class PawnMove(MajorMove):
	def __init__(self, board, piece, dest):
		MajorMove.__init__(self, board, piece, dest)
	def execute(self):
		return MajorMove.execute(self)

class PawnJump(Move):
	def __init__(self, board, piece, dest, enpassant):
		Move.__init__(self, board, piece, dest, None)
		self.__enpassant = enpassant
	def execute(self):
		builder = Move.execute(self, True)
		for piece in self.board.get_all_pieces():
			if piece == self.piece: continue
			builder.set_piece(piece)
		pawn = self.piece.move_piece(self.destination)
		if self.__enpassant: builder.set_enpassant_pawn(pawn)
		return builder \
			.set_piece(pawn) \
			.set_move_maker(self.piece.get_opponent()) \
			.build()

class PawnAttack(AttackMove):
	def __init__(self, board, piece, dest, attacked_piece):
		AttackMove.__init__(self, board, piece, dest, attacked_piece)
	def execute(self):
		return AttackMove.execute(self)

class PawnEnPassantAttack(PawnAttack):
	def __init__(self, board, piece, dest, pawn):
		PawnAttack.__init__(self, board, piece, dest, pawn)
	def execute(self):
		return PawnAttack.execute(self)

class CastlingMove(MajorMove):
	def __init__(self, board, rook, dest, king):
		MajorMove.__init__(self, board, rook, dest)
		self.king = king
	def execute(self):
		return self.board

#================================================================#
#                       Move Factory Stuff                       #
#================================================================#

class MoveStatus(object):
	def __init__(self, name):
		self.__name = name
	def __str__(self):
		return self.__name

MoveStatus.Success = MoveStatus('Success')
MoveStatus.LeavesPlayerInCheck = MoveStatus('LeavesPlayerInCheck')
MoveStatus.Illegal = MoveStatus('Illegal')

class MoveTransition(object):
	def __init__(self, status, board):
		if not isinstance(status, MoveStatus):
			raise ArgumentError(f'Argument 1 is not a MoveStatus object. Got {type(status)}!')
		self.__status = status
		self.__board = board
	# Properties & getters
	@property
	def status(self): return self.__status
	@property
	def board(self): return self.__board
	# Default methods
	def is_success(self):
		return self.status == MoveStatus.Success

class MoveFactory(object):
	def __init__(self):
		raise InstantiateError('Cannot instantiate MoveFactory!')
	@staticmethod
	def create_move(board, position, destination):
		for move in board.current_player.get_legal_moves():
			if move.position == position and move.destination == destination:
				return MoveTransition(MoveStatus.Success, move.execute())
		return MoveTransition(MoveStatus.Illegal, board)