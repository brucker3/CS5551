from unittest import TestCase
from checkers.game import Game

class test_board_class(TestCase):
    def setUp(self):
        self.test_game = Game()

    def test_matrix_length(self):
        self.assertEqual(len(self.test_game.matrix),8)
        self.assertEqual(len(self.test_game.matrix[0]),8)

    
    def test_matrix_type(self):
        self.assertIsInstance((self.test_game.matrix),list)

    def test_jump_available(self):
        self.assertEqual(self.test_game.check_for_jumps_available('D'), False)
