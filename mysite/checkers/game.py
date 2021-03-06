"""
I adapted some code found at
@ inspired by: https://github.com/everestwitman/Pygame-Checkers/blob/master/checkers.py
"""

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

class Game(Board):
	"""
	The main game control.
	"""
	def __init__(self):
		self.id = self.generate_random_alphanumeric_string()
		self.matrix = self.new_board()
		self.turn = DARK
		self.selected_piece = None # a board location.
		self.jump_available = False # this instance var is to force player to jump
		self.hop = False
		self.selected_legal_moves = []
		self.winner  = ''
		self.player1 = ''
		self.player2 = ''

	def get_board(self):
		return self

	def generate_random_alphanumeric_string(self):
		return (''.join(random.choices(string.ascii_lowercase + string.digits, k=16))) #here k is length of string

	def regenerate_game_id(self):
		self.id = self.generate_random_alphanumeric_string()

	def update_legal_moves(self):
		if self.selected_piece != None:
			self.selected_legal_moves = self.legal_moves(self.selected_piece, self.hop, self.jump_available)

	def update_game_object(self, mouse_position=[0,0]):
		if (not self.jump_available): self.set_jump_available()
		"""	This function updates game object based on input of position"""
		self.mouse_pos = mouse_position # what square is the mouse clicked in? .. format (x,y)
		if self.hop == False:
			if self.location(self.mouse_pos).occupant != None and self.location(self.mouse_pos).occupant.color == self.turn:
				self.selected_piece = self.mouse_pos

			elif self.selected_piece != None and self.mouse_pos in self.legal_moves(self.selected_piece,jump_available=self.jump_available):
				self.move_piece(self.selected_piece, self.mouse_pos)

				if self.mouse_pos not in self.adjacent(self.selected_piece):
					self.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))

					self.hop = True
					self.selected_piece = self.mouse_pos
				else:
					self.end_turn()
		self.update_legal_moves()

		if self.hop == True:
			if self.selected_piece != None and self.mouse_pos in self.legal_moves(self.selected_piece, self.hop, jump_available=self.jump_available):
				self.move_piece(self.selected_piece, self.mouse_pos)
				self.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))

			if self.legal_moves(self.mouse_pos, self.hop,jump_available=self.jump_available) == []:
					self.end_turn()
			else:
				self.selected_piece = self.mouse_pos

	def get_update(self):
		"""Returns all updates on game object in required string format."""
		#send signal to update front end
		moves = []
		for i in self.selected_legal_moves:
			moves.append(self.get_key_dictionary(translation_dict,i))

		if self.selected_piece != None:
			sel_piece = (self.get_key_dictionary(translation_dict,self.selected_piece))
		else: sel_piece = None
		return (self.board_string(self.matrix), moves, sel_piece) #self.selected_legal_moves

	def set_jump_available(self):
		#
		if(self.check_for_jumps_available(self.turn)):
			self.jump_available = True

	def terminate_game(self):
		"""Quits the program and ends the game."""
		print ('game terminated')

	def end_turn(self):
		"""
		End the turn. Switches the current player.
		end_turn() also checks for and game and resets a lot of class attributes.
		"""
		if self.turn == DARK:
			self.turn = LIGHT
		else:
			self.turn = DARK
		#boelow line add board to txt file which stores record
		with open("games_record/"+self.id+".txt", "a") as file:
			file.write(self.board_string(self.matrix)+"\n")
		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False
		self.jump_available = False

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
				if self.location((x,y)).color == BLACK and self.location((x,y)).occupant != None and self.location((x,y)).occupant.color == self.turn:
					if self.legal_moves((x,y)) != []:
						return False

		return True

	def check_for_both_color_on_board(self):
		dark_piece = False
		light_piece = False
		for x in range(8):
			for y in range(8):
				if self.location((x,y)).color == BLACK and self.location((x,y)).occupant != None:
					if self.location((x,y)).occupant.color == DARK:
						dark_piece = True
					elif self.location((x,y)).occupant.color == LIGHT:
						light_piece = True
		if dark_piece and light_piece:
			return True
		else:
			return False
