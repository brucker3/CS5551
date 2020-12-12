from unittest import TestCase
from checkers.game import Game

# Create your tests here.
# this is a set of new test added for the player clas
 

class test_game_class(TestCase):
    def setUp(self):
        self.test_game= Game()

    #5
    def test_game_build(self):
        self.assertIsInstance(self.test_game.matrix, list)
        self.assertIsInstance(self.test_game.turn, str)
        self.assertIsInstance(self.test_game.winner, str)
        self.assertIsInstance(self.test_game.hop, bool)
        self.assertIsInstance(self.test_game.selected_legal_moves, list)
    #6    
    def test_game_change_turn(self):
        self.assertEqual(self.test_game.turn, "D")
        self.test_game.end_turn()
        self.assertEqual(self.test_game.turn, "L")
        self.test_game.end_turn()
        self.assertEqual(self.test_game.turn, "D")
    #7
    def test_game_functions(self):
        self.test_game.update_game_object([0,5]) #this selects piece at position 0,5
        self.assertEqual(self.test_game.selected_piece, [0,5])
        self.test_game.update_game_object([1,4]) #this moves seleted piece if it passes conditions
        self.assertEqual(self.test_game.turn, "L")
    #8
    def test_game_check_end_game(self):
        self.assertIsInstance(self.test_game.check_for_endgame(), bool)
        self.assertEqual(self.test_game.check_for_endgame(), False)
