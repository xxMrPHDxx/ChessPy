from error import *
from tile import Tile
from player import Alliance, Player
from piece import Piece, Rook, Knight, Bishop, Queen, King, Pawn
from move import MoveFactory

from random import random
from functools import reduce

def _separate_pieces(tiles):
	whites, blacks = [[] for _ in range(2)]
	for tile in tiles:
		if tile.is_empty(): continue
		piece = tile.piece
		(whites if piece.is_white() else blacks).append(piece)
	return whites, blacks

def _calculate_moves(board):
	white_moves, black_moves = [[] for _ in range(2)]
	for i in range(2):
		for piece in (board._white_pieces if i == 0 else board._black_pieces):
			for move in piece.calculate_moves(board):
				(white_moves if i == 0 else black_moves).append(move)
	return white_moves, black_moves

def _create_player(board, white_moves, black_moves):
	white = Player(Alliance.White, board, white_moves, black_moves)
	black = Player(Alliance.Black, board, black_moves, white_moves)
	return white, black

class Board(object):
	def __init__(self, builder):
		if not isinstance(builder, Board.Builder):
			raise ArgumentError(f'Argument 1 is not a BoardBuilder object. Got {type(builder)}!')
		self._tiles = builder.tiles
		self.__enpassant_pawn = builder.enpassant_pawn
		self._white_pieces, self._black_pieces = _separate_pieces(self._tiles)
		white_moves, black_moves = _calculate_moves(self)
		self.white_player, self.black_player = _create_player(self, white_moves, black_moves)
		self.current_player = self.white_player if builder.move_maker == Alliance.White else self.black_player
	# Properties / Getters
	@property
	def enpassant_pawn(self): return self.__enpassant_pawn
	# Default methods
	def get_all_pieces(self):
		return [*self._white_pieces, *self._black_pieces]
	def get_opponent(self):
		return self.white_player if self.current_player == self.black_player else self.black_player
	def has_enpassant_pawn(self):
		return self.enpassant_pawn != None
	def get_random_move(self):
		moves = self.current_player.get_legal_moves()
		index = int(random() * len(moves))
		return moves[index]
	# Overrides
	def __eq__(self, other):
		if not isinstance(other, Board): return False
		return all([
			str(self) == str(other),
			self.enpassant_pawn == other.enpassant_pawn,
			self.white_player == other.white_player,
			self.black_player == other.black_player
		])
	def __str__(self):
		return '\n'.join([' '.join([str(self._tiles[r*8+c]) for c in range(8)]) for r in range(8)])
	def __getitem__(self, index):
		if type(index) != int: 
			raise ArgumentError(f'Must specify an integer. Got {type(index)}!')
		if not (index >= 0 and index < 64):
			raise IndexError('Out of bounds. Range 0-63!')
		return self._tiles[index]
	def __iter__(self):
		for i in range(64): yield self[i]
	# Static methods
	@staticmethod
	def create_standard_board():
		builder = Board.Builder()

		# Blacks' & Whites' Pawn
		for ally in [Alliance.White, Alliance.Black]:
			offs = 48 if ally == Alliance.White else 8
			for i in range(8): builder.set_piece(Pawn(ally, i+offs))

		# Other pieces
		return builder \
			.set_piece(Rook  (Alliance.Black, 0)) \
			.set_piece(Knight(Alliance.Black, 1)) \
			.set_piece(Bishop(Alliance.Black, 2)) \
			.set_piece(Queen (Alliance.Black, 3)) \
			.set_piece(King  (Alliance.Black, 4)) \
			.set_piece(Bishop(Alliance.Black, 5)) \
			.set_piece(Knight(Alliance.Black, 6)) \
			.set_piece(Rook  (Alliance.Black, 7)) \
			.set_piece(Rook  (Alliance.White, 63-0)) \
			.set_piece(Knight(Alliance.White, 63-1)) \
			.set_piece(Bishop(Alliance.White, 63-2)) \
			.set_piece(King  (Alliance.White, 63-3)) \
			.set_piece(Queen (Alliance.White, 63-4)) \
			.set_piece(Bishop(Alliance.White, 63-5)) \
			.set_piece(Knight(Alliance.White, 63-6)) \
			.set_piece(Rook  (Alliance.White, 63-7)) \
			.build()
	@staticmethod
	def create_board_from_array(config, move_maker=Alliance.White, enpassant_pawn=None):
		if not (isinstance(config, list) or len(config) != 64):
			if len(config) < 64: 
				for _ in range(64-len(config)): config.append(0)
			else: 
				raise Exception('Invalid config!')
		def process_tile(builder, args):
			pos, args = args
			if type(args) == int: tile, first_move = args, True
			elif len(args) == 2: tile, first_move = args
			else:
				raise Exception(f'Invalid board config!')
			if tile != 0:
				_ally = Alliance.White if tile < 0 else Alliance.Black
				Piece = [None, Rook, Knight, Bishop, Queen, King, Pawn][abs(tile)]
				piece = Piece(_ally, pos, first_move)
				if enpassant_pawn != None and all([
					isinstance(piece, Pawn),
					type(enpassant_pawn) == int,
					BoardUtils.is_valid(enpassant_pawn),
					pos == enpassant_pawn
				]):
					builder.set_enpassant_pawn(piece)
				builder.set_piece(piece)
			return builder
		return reduce(process_tile, enumerate(config), Board.Builder()) \
			.set_move_maker(move_maker) \
			.build()

	class Builder(object):
		def __init__(self):
			self.tiles = [Tile(position) for position in range(64)]
			self.move_maker = Alliance.White
			self.enpassant_pawn = None
		def set_move_maker(self, move_maker):
			if not isinstance(move_maker, Alliance):
				raise AllianceError(f'Invalid alliance: Found {type(move_maker)}!')
			self.move_maker = move_maker
			return self
		def set_piece(self, piece):
			if not isinstance(piece, Piece):
				raise ArgumentError(f'Argument 1 is not a Piece object. Got {type(piece)}!')
			self.tiles[piece.position] = Tile(piece)
			return self
		def set_enpassant_pawn(self, pawn):
			if not pawn == None and not isinstance(pawn, Pawn):
				raise ArgumentError(f'Argument 1 is not a Pawn object. Got {type(pawn)}!')
			self.enpassant_pawn = pawn
			return self
		def build(self):
			return Board(self)

if __name__ == '__main__':
	from gui.frame import GuiChess

	app = GuiChess(Board.create_standard_board(), MoveFactory) # 
	app.mainloop()