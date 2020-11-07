from .game import *

class Player():
	def __init__(self):
		#player initailisation method
		
	def create_game(self):
		new_game = Game()
		self.game = new_game
		
	def join_game(self, game):
		self.game = game