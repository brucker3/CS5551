from unittest import TestCase
from checkers.aiplayer import *
from checkers.game import Game


# Create your tests here.
# this is a set of new test added for the player clas
 

class test_ai_player(TestCase):
    def setUp(self):
        self.game = Game()
        self.ai_player = Aiplayer(self.game.get_board())

    #9
    def test_ai_setup(self):
        self.assertIsInstance(self.ai_player.ai_pieces, list)
        self.assertIsInstance(self.ai_player.color, str)
        self.assertEqual(len(self.ai_player.ai_pieces), 12)
        self.assertEqual(len(self.ai_player.opponent_pieces), 12)

    #10
    def test_ai_minmax(self):
        self.assertIsInstance(self.ai_player.minmax(self.game.get_board(),3), tuple)
   