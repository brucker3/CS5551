from django.test import TestCase
from checkers import  players 
from checkers.game import Game

# Create your tests here.
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

test_game = Game()

def test_game_build():
    assert isinstance(test_game.board, list)
    assert isinstance(test_game.selected_piece, list)
    assert isinstance(test_game.turn, str)
    assert isinstance(test_game.winner, str)
    assert isinstance(test_game.hop, bool)
    assert isinstance(test_game.selected_legal_moves, list)
    
def test_game_change_turn():
    assert test_game.turn == "D"
    test_game.end_turn()
    assert test_game.turn == "L"
    test_game.end_turn()
    assert test_game.turn == "D"

def test_game_functions():
    test_game.update_game_object([0,5]) #this selects piece at position 0,5
    assert test_game.selected_piece == [0,5]
    test_game.update_game_object([1,4]) #this moves seleted piece if it passes conditions
    assert test_game.turn == "L"

def test_game_check_end_game():
    assert isinstance(test_game.check_for_endgame(), bool)
    assert test_game.check_for_endgame() == False





