from board import Board
from move import MoveFactory
from player import Alliance
from piece import Rook, Knight, Bishop, Queen, King, Pawn
from utils import BoardUtils

from functools import reduce

def separator(sep='*'*60): print(sep)

def get_random_move(board):
	from random import random
	moves = board.current_player.get_legal_moves()
	index = int(random() * len(moves))
	return moves[index]

def create_board_from_array(config, move_maker=Alliance.White, enpassant_pawn=None):
	if not (isinstance(config, list) or len(config) != 64):
		if len(config) < 64: 
			for _ in range(64-len(config)): config.append((0, 0))
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

def enpassant_test():
	board = create_board_from_array([
		 1, 2, 3, 4, 5, 3, 2, 1,
		 0, 6, 0, 6, 6, 6, 6, 6,
		*[0 for _ in range(16)],
		 (6, False), 0, (6, False), 0, 0, 0, 0, 0,
		 0, 0, 0, 0, 0, 0, 0, 0,
		-6,-6,-6,-6,-6,-6,-6,-6,
		-1,-2,-3,-4,-5,-3,-2,-1
	])

	transition = MoveFactory.create_move(board, 49, 33)
	assert transition.is_success(), 'Failed to execute PawnJump from 49 to 33!'
	board = transition.board
	board1 = create_board_from_array([
		 1, 2, 3, 4, 5, 3, 2, 1,
		 0, 6, 0, 6, 6, 6, 6, 6,
		*[0 for _ in range(16)],
		 (6, False), (-6, False), (6, False), 0, 0, 0, 0, 0,
		 0, 0, 0, 0, 0, 0, 0, 0,
		-6, 0,-6,-6,-6,-6,-6,-6,
		-1,-2,-3,-4,-5,-3,-2,-1
	], enpassant_pawn=33)
	assert board == board1, 'Board 1 is not equal!'

	transition = MoveFactory.create_move(board, 32, 41)
	assert transition.is_success(), 'Failed to execute PawnEnPassantAttack from 32 to 41!'
	board = transition.board
	board2 = create_board_from_array([
		 1, 2, 3, 4, 5, 3, 2, 1,
		 0, 6, 0, 6, 6, 6, 6, 6,
		*[0 for _ in range(16)],
		 0, 0, (6, False), 0, 0, 0, 0, 0,
		 0, (6, False), 0, 0, 0, 0, 0, 0,
		-6, 0,-6,-6,-6,-6,-6,-6,
		-1,-2,-3,-4,-5,-3,-2,-1
	])
	assert board == board2, 'Board 2 is not equal'
	print(board)