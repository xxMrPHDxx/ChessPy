from tkinter import *

from functools import reduce

class GuiBoard(Canvas):
	def __init__(self, master, MoveFactory):
		if not MoveFactory: raise Exception('Please supply MoveFactory at argument 2!')
		Canvas.__init__(self, master, width=504, height=504)
		self.MoveFactory = MoveFactory
		self.__master = master
		self.__board_img = PhotoImage(file='img/board.png')
		self.__center = { 'x': self.winfo_width()//2, 'y': self.winfo_height()//2 }
		self.__pieces_img = GuiBoard.__split_image(PhotoImage(file='img/figures.png'), 2, 6, 56, 56)
		self.__setup_ui_icons()
		self.pack()
		self.bind('<Button-1>', self.__on_click())
		self.__reset_tiles()
		self.__hints = []
	# Properties & getters
	@property
	def board(self): return self.__master.board
	# Private methods
	def __setup_ui_icons(self):
		ui_imgs = GuiBoard.__split_image(PhotoImage(file='img/ui.png'), 2, 3, 56, 56)
		self.__red_dot, self.__green_dot, self.__castling = ui_imgs[:3]
		self.__incheck, self.__checkmate, self.stale_mate = ui_imgs[3:]
	def __reset_tiles(self): 
			self.__src_tile, self.__dst_tile = [None for _ in range(2)]
	def __on_click(self):
		def inner(event):
			row, col = [(arg-28)//56 for arg in [event.y, event.x]]
			index = row*8 + col
			if not (index >= 0 and index < 64): return
			self.__on_tile_clicked(row, col, index)
		return inner
	def __set_board(self, board):
		self.__master.set_board(board)
	def __on_tile_clicked(self, row, col, index):
		self.__hints.clear()
		tile = self.board[index]
		if self.__src_tile == None:
			# First click
			if tile.is_empty(): return
			has_move = False
			for move in self.board.current_player.get_legal_moves():
				if move.position != index: continue
				has_move = True
				row, col = [fun(move.destination) for fun in [lambda x: x//8, lambda x: x%8]]
				self.__hints.append(((col+1)*56, (row+1)*56, move.is_attack_move()))
			if not has_move: return
			self.__src_tile = tile
		else:
			# Second click
			_from, _to = self.__src_tile.position, tile.position
			transition = self.MoveFactory.create_move(self.board, _from, _to)
			if transition.is_success():
				self.__set_board(transition.board)
			self.__reset_tiles()
		self.draw_board()
	def __draw_fg_hints(self):
		for x, y, is_attack in self.__hints:
			img = self.__red_dot if is_attack != True else self.__green_dot
			self.create_image((x, y), image=img)
	# Private static methods
	@staticmethod
	def __split_image(sheet, rows, cols, subwidth, subheight):
		return reduce(
			lambda array, rows: [*array, *rows],
			[[
				GuiBoard.__create_subimage(sheet, row, col, subwidth, subheight)
				for col in range(cols)
			] for row in range(rows)]
		, [])
	@staticmethod
	def __create_subimage(sheet, row, col, width, height):
		x, y = col * width, row * height
		cpy = PhotoImage()
		cpy.tk.call(cpy, 'copy', sheet, '-from', x, y, x+width, y+height, '-to', 0, 0)
		return cpy
	@staticmethod
	def __get_piece_index(piece):
		return [
			'R','N','B','Q','K','P',
			'r','n','b','q','k','p'
		].index(str(piece))
	# Default methods
	def draw_board(self):
		self.create_image((252, 252), image=self.__board_img)
		if self.board == None: return
		for tile in self.board:
			if tile.is_empty(): continue
			index = GuiBoard.__get_piece_index(tile.piece)
			image = self.__pieces_img[index]
			y, x = [(arg+1)*56 for arg in [tile.piece.position // 8, tile.piece.position % 8]]
			self.create_image((x, y), image=image)
		self.__draw_fg_hints()

class GuiChess(Tk):
	def __init__(self, board=None, MoveFactory=None):
		Tk.__init__(self)
		self.winfo_toplevel().title('Chess')
		self.gui_board = GuiBoard(self, MoveFactory)
		self.set_board(board)
		self.gui_board.draw_board()
	def set_board(self, board):
		self.board = board