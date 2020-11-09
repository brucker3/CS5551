from django.test import TestCase

from checkers import  board, players 



# Create your tests here.
# build test board
"""
test_board = board( black_space=[], red_space=[], free_space= [],board=[])

# check is board data structures are correct
def test_board_build():
    assert isinstance(test_board.board, list)
    assert isinstance(test_board.red_space, list)
    assert isinstance(test_board.black_space, list)
    assert isinstance(test_board.free_space, list)

# genrate a standard board and check it
def test_board_generate():
    test_board.generate_board("standard")
    assert len(test_board.board) == 32
    assert len(test_board.red_space) == 8
    assert len(test_board.black_space) == 8
    assert len(test_board.free_space) == 16

def test_baord_get_spaces():
    black = test_board.get_spaces("black")
    red = test_board.get_spaces("red")
    free= test_board.get_spaces("free")
    assert isinstance(black , list)
    assert isinstance(red,list)
    assert isinstance(free, list)
"""

# this is a set of new test added for the player class
test_player = players.Player("ted", "ted@.com")

def test_player_build():
    assert isinstance(test_player.name, str)
    assert isinstance(test_player.email, str)
    assert isinstance(test_player.game_color, str)
    assert isinstance(test_player.active_game, bool)
    assert isinstance(test_player.piece_count, list)
     
def test_player_new_game():
    test_player.new_game([(1,2),(2,3),(3,4)], "red")
    assert test_player.game_color =="red"
    assert test_player.active_game , True
    assert len(test_player.piece_count), 2

def test_player_get_funcitons():
    assert test_player.get_name() == "ted"
    assert test_player.get_email() == "ted@.com"
    assert test_player.is_active() == True
    assert test_player.player_color() == "red"
    assert isinstance(test_player.player_pieces(), list)


def test_player_reset():
    test_player.game_reset()
    assert test_player.is_active() ==False
    assert test_player.player_color() =="none"
    assert len(test_player.player_pieces()) ==  0






