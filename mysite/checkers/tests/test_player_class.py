from unittest import TestCase
from checkers import  players 
from checkers.game import Game

# Create your tests here.
# this is a set of new test added for the player class


class test_player_class(TestCase):
    def setup(self):
        test_player = players.Player("ted", "ted@.com")
        print (test_player)

    #1
    def test_player_build(self):
        test_player = players.Player("ted", "ted@.com")
        self.assertIsInstance(test_player.name, str)
        self.assertIsInstance(test_player.email, str)
        self.assertIsInstance(test_player.game_color, str)
        self.assertIsInstance(test_player.active_game, bool)
        self.assertIsInstance(test_player.piece_count, list)
    #2     
    def test_player_new_game(self):
        test_player = players.Player("ted", "ted@.com")
        test_player.new_game([(1,2),(2,3),(3,4)], "red")
        self.assertEqual( test_player.game_color, "red")
        self.assertEqual( test_player.active_game , True)
        self.assertEqual( len(test_player.piece_count), 3)
    #3
    def test_player_get_funcitons(self):
        test_player = players.Player("ted", "ted@.com")
        self.assertEqual(test_player.get_name(), "ted")
        self.assertEqual(test_player.get_email(), "ted@.com")
        self.assertEqual(test_player.is_active(), False)
        self.assertIsInstance(test_player.player_pieces(), list)

    #4
    def test_player_reset(self):
        test_player = players.Player("ted", "ted@.com")
        test_player.game_reset()
        self.assertEqual(test_player.is_active(), True)
        self.assertEqual(test_player.player_color(), "none")
        self.assertEqual(len(test_player.player_pieces()), 0)
