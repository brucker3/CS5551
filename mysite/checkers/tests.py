from django.test import TestCase
from checkers import  board



# Create your tests here.
# build test board
test_board = board()

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
