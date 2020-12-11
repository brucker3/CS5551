#mysite/checkers/board.py
"""
I adapted some code from checkers.py found at
@ inspired by: https://github.com/everestwitman/Pygame-Checkers/blob/master/checkers.py
"""
import sys
import json

WHITE    = 'WHITE'
DARK     = 'D' #bottom pieces
LIGHT      = 'L' #uppoer pieces
BLACK    = 'BLACK'

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Board:
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):
		"""		Create a new board matrix.		"""

		matrix = [[None] * 8 for i in range(8)]
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)

		# initialize the pieces and put them in the appropriate squares

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(LIGHT)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(DARK)
		return matrix

	def board_string(self, board):
		"""Takes a board and returns a matrix of the board space colors. Used for testing new_board()"""
		board_dict = {}; counter=1
		for x in range(8):
			for y in range(8):
				if board[y][x].color == BLACK:
					piece_name = ''
					if board[y][x].occupant != None:
						if board[y][x].occupant.color == LIGHT: piece_name='L'
						elif board[y][x].occupant.color == DARK: piece_name='D'
						if board[y][x].occupant.king: piece_name += 'K'
					else : piece_name = 'X'
					board_dict[counter] = [piece_name]
					counter+=1

		return json.dumps(board_dict)

	def get_key_dictionary(self, dictionary, value):
		return list(dictionary.keys())[list(dictionary.values()).index(list(value))]

	def rel(self, dir, x_y ):
		"""	Returns the coordinates one square in a different direction to (x,y).	"""
		[x,y] = x_y
		if dir == NORTHWEST:
			return [x - 1, y - 1]
		elif dir == NORTHEAST:
			return [x + 1, y - 1]
		elif dir == SOUTHWEST:
			return [x - 1, y + 1]
		elif dir == SOUTHEAST:
			return [x + 1, y + 1]
		else:
			return 0

	def adjacent(self, x_y):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""
		(x,y) = x_y
		return [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)),self.rel(SOUTHWEST, (x,y)),self.rel(SOUTHEAST, (x,y))]

	def location(self, x_y):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""
		(x,y) =x_y
		return self.matrix[x][y]

	def blind_legal_moves(self, x_y):
		"""
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
		If that location is empty, then blind_legal_moves() return an empty list.
		"""
		[x,y]  = x_y
		if self.matrix[x][y].occupant != None:

			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == DARK:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y))]

			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == LIGHT:
				blind_legal_moves = [self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)), self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def check_for_jumps_available(self,turn):
		"""
		Checks to see if a player has any jump moves. If so, then return True. Else return False.
		"""
		for x in range(8):
			for y in range(8):
				if self.location((x,y)).color == BLACK and self.location((x,y)).occupant != None and self.location((x,y)).occupant.color == turn:
					if self.legal_moves((x,y),jump_available=True) != []:
						return True
		return False

	def legal_moves(self, x_y, hop = False, jump_available=False):
		"""
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""
		[x,y] = x_y
		blind_legal_moves = self.blind_legal_moves((x,y))
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move):
						if self.location(move).occupant == None and not jump_available:
							legal_moves.append(move)

						elif self.location(move).occupant!=None and self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append([move[0] + (move[0] - x), move[1] + (move[1] - y)])

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move) and self.location(move).occupant != None:
					if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append([move[0] + (move[0] - x), move[1] + (move[1] - y)])
		return legal_moves

	def remove_piece(self, x_y):
		"""
		Removes a piece from the board at position (x,y).
		"""
		(x,y) = list(map(int,x_y))
		self.matrix[x][y].occupant = None

	def move_piece(self, start_x_y, end_x_y):
		"""
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""
		(start_x, start_y) = start_x_y
		(end_x, end_y) = end_x_y
		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))
		self.king((end_x, end_y))


	def is_end_square(self, coords):
		"""
		Is passed a coordinate tuple (x,y), and returns true or
		false depending on if that square on the board is an end square."""

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	def on_board(self, x_y):
		"""
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false."""
		(x,y)  = x_y
		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, x_y):
		"""
		Takes in (x,y), the coordinates of square to be considered for kinging.
		If it meets the criteria, then king() kings the piece in that square and kings it.
		"""
		(x,y) = x_y
		if self.location((x,y)).occupant != None:
			if (self.location((x,y)).occupant.color == DARK and y == 0) or (self.location((x,y)).occupant.color == LIGHT and y == 7):
				self.location((x,y)).occupant.king = True

class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

	def get_piece(self):
		return self.king, self.color

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object

	def get_square(self):
		return self.color, self.occupant
