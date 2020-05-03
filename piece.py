from error import *
from utils import BoardUtils
from move import *

class Piece(object):
	class Type(object):
		def __init__(self, name):
			self._name = name
		def __str__(self):
			if self._name == 'Knight': return 'N'
			return self._name[0]

	Type.Rook = Type('Rook')
	Type.Knight = Type('Knight')
	Type.Bishop = Type('Bishop')
	Type.Queen = Type('Queen')
	Type.King = Type('King')
	Type.Pawn = Type('Pawn')	

	def __init__(self, _type, _ally, _pos, _first_move):
		from player import Alliance
		if not isinstance(_type, Piece.Type):
			raise ArgumentError(f'Argument 1 is not a Type object. Got {type(_type)}')
		if not isinstance(_ally, Alliance):
			raise ArgumentError(f'Argument 2 is not an Alliance object. Got {type(_ally)}')
		if type(_pos) != int:
			raise ArgumentError(f'Argument 3 is not an integer. Got {type(_pos)}')
		self._type = _type
		self._ally = _ally
		self._pos = _pos
		self._first_move = _first_move
	# Properties
	@property
	def type(self): return self._type
	@property
	def alliance(self): return self._ally
	@property
	def position(self): return self._pos
	@property
	def first_move(self): return self._first_move
	@property
	def direction(self):
		return -1 if self.alliance == Alliance.White else 1
	@property
	def opposite(self):
		return -1 * self.direction
	# Default Methods
	def is_white(self): 
		from player import Alliance
		return self._ally == Alliance.White
	def is_black(self): return not self.is_white();
	def has_exclusion(self, pos, offset):
		return self.is_first_column_excluded(pos, offset) or \
				self.is_second_column_excluded(pos, offset) or \
				self.is_seventh_column_excluded(pos, offset) or \
				self.is_eighth_column_excluded(pos, offset)
	def get_opponent(self):
		return Alliance.Black if self.alliance == Alliance.White else Alliance.White
	def is_king(self): return self.type == Piece.Type.King
	# Abstract Methods
	def calculate_moves(self, board): return []
	def is_first_column_excluded(self, pos, offset): return False
	def is_second_column_excluded(self, pos, offset): return False
	def is_seventh_column_excluded(self, pos, offset): return False
	def is_eighth_column_excluded(self, pos, offset): return False
	# Overrides
	def __eq__(self, other):
		if not isinstance(other, Piece): return False
		return self.type == other.type and \
			self.alliance == other.alliance and \
			self.position == other.position and \
			self.first_move == other.first_move
	def __str__(self):
		from player import Alliance
		func = lambda x: x.upper()
		if self.alliance == Alliance.White: func = lambda x: x.lower()
		return func(str(self.type))
	def __hash__(self):
		return reduce([hash(self.__dict__[prop]) for prop in self.__dict__])

class Rook(Piece):
	def __init__(self, ally, pos, first_move=True):
		Piece.__init__(self, Piece.Type.Rook, ally, pos, first_move)
	def calculate_moves(self, board):
		legal_moves = Piece.calculate_moves(self, board)
		for offset in [ -8, -1, 1, 8 ]:
			dest = self.position
			while BoardUtils.is_valid(dest + offset):
				if self.has_exclusion(dest, offset): break
				dest += offset
				tile, piece = board[dest], board[dest].piece
				if not tile.is_empty():
					if piece.alliance != self.alliance:
						legal_moves.append(AttackMove(board, self, dest, piece))
					elif all([
						isinstance(piece, King),
						piece.first_move,
						self.first_move
					]):
						legal_moves.append(CastlingMove(board, self, dest, piece))
					break
				else:
					legal_moves.append(MajorMove(board, self, dest))
		return legal_moves
	def is_first_column_excluded(self, pos, offset):
		return BoardUtils.is_first_column(pos) and offset == -1
	def is_eighth_column_excluded(self, pos, offset):
		return BoardUtils.is_eighth_column(pos) and offset == 1
	def move_piece(self, dest):
		return Rook(self.alliance, dest, False)

class Knight(Piece):
	def __init__(self, ally, pos, first_move=True):
		Piece.__init__(self, Piece.Type.Knight, ally, pos, first_move)
	def calculate_moves(self, board):
		legal_moves = Piece.calculate_moves(self, board)
		for offset in [ -17, -15, -10, -6, 6, 10, 15, 17 ]:
			dest = self.position + offset
			if not BoardUtils.is_valid(dest) or self.has_exclusion(self.position, offset):
				continue
			tile, piece = board[dest], board[dest].piece
			if not tile.is_empty():
				if piece.alliance != self.alliance:
					legal_moves.append(AttackMove(board, self, dest, piece))
			else:
				legal_moves.append(MajorMove(board, self, dest))
		return legal_moves
	def is_first_column_excluded(self, pos, offset):
		return BoardUtils.is_first_column(pos) and offset in [-17,-10,6,15]
	def is_second_column_excluded(self, pos, offset):
		return BoardUtils.is_second_column(pos) and offset in [-10,6]
	def is_seventh_column_excluded(self, pos, offset):
		return BoardUtils.is_seventh_column(pos) and offset in [-6,10]
	def is_eighth_column_excluded(self, pos, offset):
		return BoardUtils.is_eighth_column(pos) and offset in [-15,-6,10,17]
	def move_piece(self, dest):
		return Knight(self.alliance, dest, False)

class Bishop(Piece):
	def __init__(self, ally, pos, first_move=True):
		Piece.__init__(self, Piece.Type.Bishop, ally, pos, first_move)
	def calculate_moves(self, board):
		legal_moves = Piece.calculate_moves(self, board)
		for offset in [ -9, -7, 7, 9 ]:
			dest = self.position
			while BoardUtils.is_valid(dest + offset):
				if self.has_exclusion(dest, offset): break
				dest += offset
				tile, piece = board[dest], board[dest].piece
				if not tile.is_empty():
					if piece.alliance != self.alliance:
						legal_moves.append(AttackMove(board, self, dest, piece))
					break
				else:
					legal_moves.append(MajorMove(board, self, dest))
		return legal_moves
	def is_first_column_excluded(self, pos, offset):
		return BoardUtils.is_first_column(pos) and offset in [-9,7]
	def is_eighth_column_excluded(self, pos, offset):
		return BoardUtils.is_eighth_column(pos) and offset in [-7,9]
	def move_piece(self, dest):
		return Bishop(self.alliance, dest, False)

class Queen(Piece):
	def __init__(self, ally, pos, first_move=True):
		Piece.__init__(self, Piece.Type.Queen, ally, pos, first_move)
	def calculate_moves(self, board):
		legal_moves = Piece.calculate_moves(self, board)
		for offset in [ -9, -8, -7, -1, 1, 7, 8, 9 ]:
			dest = self.position
			while BoardUtils.is_valid(dest + offset):
				if self.has_exclusion(dest, offset): break
				dest += offset
				tile, piece = board[dest], board[dest].piece
				if not tile.is_empty():
					if piece.alliance != self.alliance:
						legal_moves.append(AttackMove(board, self, dest, piece))
					break
				else:
					legal_moves.append(MajorMove(board, self, dest))
		return legal_moves
	def is_first_column_excluded(self, pos, offset):
		return BoardUtils.is_first_column(pos) and offset in [-9,-1,7]
	def is_eighth_column_excluded(self, pos, offset):
		return BoardUtils.is_eighth_column(pos) and offset in [-7,1,9]
	def move_piece(self, dest):
		return Queen(self.alliance, dest, False)

class King(Piece):
	def __init__(self, ally, pos, first_move=True):
		Piece.__init__(self, Piece.Type.King, ally, pos, first_move)
	def calculate_moves(self, board):
		legal_moves = Piece.calculate_moves(self, board)
		for offset in [ -9, -8, -7, -1, 1, 7, 8, 9 ]:
			dest = self.position + offset
			if not BoardUtils.is_valid(dest) or self.has_exclusion(dest, offset): continue
			tile, piece = board[dest], board[dest].piece
			if not tile.is_empty():
				if piece.alliance != self.alliance:
					legal_moves.append(AttackMove(board, self, dest, piece))
			else:
				legal_moves.append(MajorMove(board, self, dest))
		return legal_moves
	def is_first_column_excluded(self, pos, offset):
		return BoardUtils.is_first_column(pos) and offset in [-9,-1,7]
	def is_eighth_column_excluded(self, pos, offset):
		return BoardUtils.is_eighth_column(pos) and offset in [-7,1,9]
	def move_piece(self, dest):
		return King(self.alliance, dest, False)

class Pawn(Piece):
	def __init__(self, ally, pos, first_move=True):
		Piece.__init__(self, Piece.Type.Pawn, ally, pos, first_move)
	def calculate_moves(self, board):
		legal_moves = Piece.calculate_moves(self, board)
		for offset in [ 7, 8, 9, 16 ]:
			dest = self.position + offset * self.direction
			if not BoardUtils.is_valid(dest) or self.has_exclusion(self.position, offset): continue
			tile = board[dest]
			if offset == 16: # Pawn Jump
				behind_tile = board[dest + 8 * self.opposite]
				if self.first_move and tile.is_empty() and behind_tile.is_empty():
					enpassant = False
					for beside in [board[dest + off] for off in [-1, 1]]:
						if beside.is_empty(): continue
						enpassant = True
					legal_moves.append(PawnJump(board, self, dest, enpassant))
			elif offset == 8: # Pawn Move
				if tile.is_empty():
					legal_moves.append(PawnMove(board, self, dest))
			else:
				if not tile.is_empty() and tile.piece.alliance != self.alliance:
					# Pawn Attack Move
					legal_moves.append(PawnAttack(board, self, dest, tile.piece))
				elif board.has_enpassant_pawn():
					# Pawn Enpassant Attack
					pawn = board.enpassant_pawn
					behind_pawn = pawn.position + 8 * pawn.opposite
					if dest == behind_pawn and pawn.alliance != self.alliance:
						legal_moves.append(PawnEnPassantAttack(board, self, dest, pawn))
		return legal_moves
	def move_piece(self, dest):
		return Pawn(self.alliance, dest, False)