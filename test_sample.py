from board import Board
from move import MoveFactory, CastlingMove
from player import Alliance

def separator(sep='*'*60): print(sep)

def test_board():
	board = Board.create_standard_board()
	assert board.current_player.alliance == Alliance.White, 'White Player should start first!'
	assert len(board.current_player.active_pieces) == 16, 'White Player doesn\'t have 16 active pieces!'
	assert len(board.get_opponent().active_pieces) == 16, 'Black Player doesn\'t have 16 active pieces!'
	assert len(board.current_player.get_legal_moves()) == 20, 'White Player doesn\'t have 20 moves!'
	assert len(board.get_opponent().get_legal_moves()) == 20, 'Black Player doesn\'t have 20 moves!'
	assert not board.has_enpassant_pawn(), 'Board should not have enpassant pawn!'

def test_check_stale_mate_cases():
	board = Board.create_standard_board()
	assert not board.current_player.is_in_check(), 'White Player should not in check!'
	assert not board.get_opponent().is_in_check(), 'Black Player should not in check!'
	assert not board.current_player.is_in_check_mate(), 'White Player should not in check mate!'
	assert not board.get_opponent().is_in_check_mate(), 'Black Player should not in check mate!'
	assert not board.current_player.is_in_stale_mate(), 'White Player should not in stale mate!'
	assert not board.get_opponent().is_in_stale_mate(), 'Black Player should not in stale mate!'

def test_move_execution():
	board = Board.create_standard_board()
	for i in range(10):
		move = board.get_random_move()
		is_success = True
		try: board = move.execute()
		except: is_success = False
		assert is_success, f'Failed to execute move {i+1}: {move}'

def test_in_check():
	board = Board.create_board_from_array([
		 0, 0, 0, 0, 5, 0, 0, 0,
		 0, 0, 0,-3, 0,-1, 0, 0,
		*[0 for _ in range(40)],
		 0, 0, 0, 0,-5, 0, 0, 0,
	], Alliance.Black)
	print(board)
	assert board.current_player.is_in_check(), 'Black player is in check!'
	assert not board.current_player.is_in_check_mate(), 'Black player is in check mate!'
	assert not board.current_player.is_in_stale_mate(), 'Black player is in stale mate!'

def test_check_mate():
	board = Board.create_board_from_array([
		 0, 0, 0, 0, 5, 0, 0, 0,
		 0, 0, 0,-4, 0,-4, 0, 0,
		*[0 for _ in range(40)],
		 0, 0, 0, 0,-5, 0, 0, 0,
	], Alliance.Black)
	assert board.current_player.is_in_check(), 'Black player is not in check!'
	assert board.current_player.is_in_check_mate(), 'Black player is not in check mate!'
	assert not board.current_player.is_in_stale_mate(), 'Black player is in stale mate!'

def test_stale_mate():
	board = Board.create_board_from_array([
		 0, 0, 0, 0, 5, 0, 0, 0,
		 0, 0, 0,-1, 0,-1, 0, 0,
		*[0 for _ in range(40)],
		 0, 0, 0, 0,-5, 0, 0, 0,
	], Alliance.Black)
	assert not board.current_player.is_in_check(), 'Black player is in check!'
	assert not board.current_player.is_in_check_mate(), 'Black player is in check mate!'
	assert board.current_player.is_in_stale_mate(), 'Black player is not in stale mate!'

def test_enpassant():
	board = Board.create_board_from_array([
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
	board1 = Board.create_board_from_array([
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
	board2 = Board.create_board_from_array([
		 1, 2, 3, 4, 5, 3, 2, 1,
		 0, 6, 0, 6, 6, 6, 6, 6,
		*[0 for _ in range(16)],
		 0, 0, (6, False), 0, 0, 0, 0, 0,
		 0, (6, False), 0, 0, 0, 0, 0, 0,
		-6, 0,-6,-6,-6,-6,-6,-6,
		-1,-2,-3,-4,-5,-3,-2,-1
	])
	assert board == board2, 'Board 2 is not equal'

def test_castling():
	board = Board.create_board_from_array([
		 1, 0, 0, 0, 5, 0, 0, 1,
		 6, 0, 6, 4, 6, 6, 0, 6,
		 (3, False), (6, False), (2, False), (6, False), 0, (2, False), (6, False), (3, False),
		*[0 for _ in range(16)],
		(-3, False),(-6, False),(-2, False),(-6, False), 0,(-2, False),(-6, False),(-3, False),
		-6, 0,-6,(-4, False),-6,-6, 0,-6,
		-1, 0, 0, 0,-5, 0, 0,-1
	])
	for player in [board.white_player, board.black_player]:
		castling_moves = [
			move 
			for move in player.get_legal_moves()
			if isinstance(move, CastlingMove)
		]
		assert len(castling_moves) == 2, 'Failed to obtain 2 castling moves on the queen and king side!'
		for i, castling_move in enumerate(castling_moves):
			success = True
			try: castling_move.execute()
			except: success = False
			error_message = f'Failed to execute CastlingMove {i+1} for {str(player.alliance)}Player!'
			assert success, error_message