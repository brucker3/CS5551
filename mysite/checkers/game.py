import sys, json, random, string

from .board import Board
##COLORS##
'''
.   1,0     .   3,0     .   5,0     .   7,0
0,1     .   2,1     .   4,1     .   6,1     .
.   1,2     .   3,2     .   5,2     .   7,2
0,3     .   2,3     .   4,3     .   6,3     .
.   1,4     .   3,4     .   5,4     .   7,4
0,5     .   2,5     .   4,5     .   6,5     .
.   1,6     .   3,6     .   5,6     .   7,6
0,7     .   2,7     .   4,7     .   6,7     . 
'''
DARK     = 'D' #bottom pieces
LIGHT      = 'L' #uppoer pieces
BLACK    = 'BLACK'


##
translation_dict = {};k =1;
for i in range(8):
	for j in range(8):
		if (((j+i))%2!=0):
			translation_dict[k]=[j,i]
			k+=1
					
class Game(object):
	"""
	The main game control.
	"""
	def __init__(self):
		self.id = self.generate_random_alphanumeric_string()
		self.board = Board() 
		self.turn = DARK
		self.selected_piece = None # a board location. 
		self.hop = False
		self.selected_legal_moves = []
		self.winner  = ''
		self.player1 = ''
		self.player2 = ''
		
	def generate_random_alphanumeric_string(self):
		return (''.join(random.choices(string.ascii_letters + string.digits, k=16))) #here k is length of string
		
	def regenerate_game_id(self):
		self.id = self.generate_random_alphanumeric_string()
	
	def update_legal_moves(self):
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)
		
	def update_game_object(self, mouse_position=[0,0]):
		"""	The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state."""
		self.mouse_pos = mouse_position # what square is the mouse clicked in? .. format (x,y)
		if self.hop == False:
			if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
				self.selected_piece = self.mouse_pos

			elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):
				self.board.move_piece(self.selected_piece, self.mouse_pos)
			
				if self.mouse_pos not in self.board.adjacent(self.selected_piece):
					self.board.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))
				
					self.hop = True
					self.selected_piece = self.mouse_pos

				else:
					self.end_turn()
		self.update_legal_moves()
		
		if self.hop == True:					
			if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
				self.board.move_piece(self.selected_piece, self.mouse_pos)
				self.board.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))

			if self.board.legal_moves(self.mouse_pos, self.hop) == []:
					self.end_turn()

			else:
				self.selected_piece = self.mouse_pos
		# for event in pygame.event.get():

			# if event.type == QUIT:
				# self.terminate_game()

			# if event.type == MOUSEBUTTONDOWN:


	def update(self):
		"""Calls on the graphics class to update the game display."""
		#send signal to update front end
		moves = []
		for i in self.selected_legal_moves:
			moves.append(self.board.get_key_dictionary(translation_dict,i))
			
		if self.selected_piece != None:
			sel_piece = (self.board.get_key_dictionary(translation_dict,self.selected_piece))
		else: sel_piece = None
		return (self.board.board_string(self.board.matrix), moves, sel_piece) #self.selected_legal_moves

	def terminate_game(self):
		"""Quits the program and ends the game."""
		print ('game terminated')

	def main(self):
		""""This executes the game and controls its flow."""
		self.setup()
		while True: # main game loop
			self.update_game_object()
			self.update()

	def end_turn(self):
		"""
		End the turn. Switches the current player. 
		end_turn() also checks for and game and resets a lot of class attributes.
		"""
		if self.turn == DARK:
			self.turn = LIGHT
		else:
			self.turn = DARK

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == DARK:
				self.winner = "LIGHT"
			else:
				self.winner = "DARK"

	def check_for_endgame(self):
		"""
		Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
		"""
		for x in range(8):
			for y in range(8):
				if self.board.location((x,y)).color == BLACK and self.board.location((x,y)).occupant != None and self.board.location((x,y)).occupant.color == self.turn:
					if self.board.legal_moves((x,y)) != []:
						return False

		return True



