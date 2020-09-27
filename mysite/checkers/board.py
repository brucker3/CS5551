from array import *

class  board(object):

		# this class generates a arrya for the boad class
        # this data strucutre is an inbetweeen between the UI and
        # game logic in the game class
    def __init__(self, black_space, red_space, free_space, board):
        self.black_space = black_space
        self.red_space =   red_space
        self.free_space =  free_space
        self.board = board


    # game type variable was added so that different boards could be
    # generated later
    # this fuction generates sstandard  board array.
    def generate_board(self, game_type ):
        if(game_type == "standard"):
            piece = "b"
            for  i in range(0,32):
                index = i % 4
                holder = [i ,piece]
                self.board.append(holder)
                if i  == 7:
                    piece = "f"
                if i == 23 :
                    piece = "r"
        self.black_space = self.board[:8]
        self.free_space = self.board[8:24]
        self.red_space = self.board[23:31]

    # this is a simple method for retrieving set of board squares
    def get_spaces(self, piece_type):
        if(piece_type == "black"):
            return self.black_space
        if(piece_type == "red"):
            return self.red_space
        if(piece_type == "free"):
            return self.free_space

    # this method handles swapping spaces
    # but calls game engine class for game rules logic
    # this if this metho will call the game engin
    def space_swap(self, original, new):
        if original in self.free_space:
            return "invalie space swap"
        elif new in self.red_space or  new in self.black_space:
            print( "call game egine funciton player take funtioin")
        else:
            print("call is legal move function")





