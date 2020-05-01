from error import *
from tile import Tile
from player import Alliance, Player
from piece import Piece, Rook, Knight, Bishop, Queen, King, Pawn

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
		self._white_pieces, self._black_pieces = _separate_pieces(self._tiles)
		white_moves, black_moves = _calculate_moves(self)
		self.white_player, self.black_player = _create_player(self, white_moves, black_moves)
		self.current_player = self.white_player if builder.move_maker == Alliance.White else self.black_player
		# print(self.white_player, self.black_player)
	# Default methods
	def get_all_pieces(self):
		return [*self._white_pieces, * self._black_pieces]
	# Overrides
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
	@staticmethod
	def create_standard_board():
		from piece import Piece, Knight
		builder = Board.Builder()

		# Black' & Whites' Pawn
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

	class Builder(object):
		def __init__(self):
			self.tiles = [Tile(position) for position in range(64)]
			self.move_maker = Alliance.White
		def set_move_maker(self, move_maker):
			if not isinstance(move_maker, Alliance):
				raise AllianceError(f'Invalid alliance: Found {type(move_maker)}!')
			self.move_maker = move_maker
			return self
		def set_piece(self, piece):
			if not isinstance(piece, Piece):
				raise ArgumentError(f'Argument 1 is not a Piece. Got {type(piece)}!')
			self.tiles[piece.position] = Tile(piece)
			return self
		def build(self):
			return Board(self)

board = Board.create_standard_board()
_board = board

from random import random

# with open('moves.log', 'r') as file:
# 	lines = file.read().split('='*60)
# 	print(len(lines)+1)

n = 792
# n = 1000
# print(n*8 + n - 1)
print((7127+1)//9)

exit()
with open('moves.log', 'w') as file:
	boards = []
	while len(boards) < 1000:
		moves = board.current_player.get_legal_moves()
		index = int(random() * len(moves))
		move = moves[index]
		print(f'Executing move {move}...')
		try:
			board = move.execute()
			boards.append(str(board))
		except IllegalBoardError as e: 
			print('Failed!')
	file.write('\n{}\n'.format('=' * 60).join(boards))