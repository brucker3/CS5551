from .game import *
from .board import *
import math
import copy
from itertools import chain

WHITE    = 'WHITE'
DARK     = 'D' #bottom pieces
LIGHT      = 'L' #uppoer pieces
BLACK    = 'BLACK'

class Aiplayer():
    def __init__(self, board, color="L"):
        self.state = copy.deepcopy(board)
        self.color = color
        self.opponent_color = "D"
        self.ai_pieces= []
        self.opponent_pieces= []
        self.pieces_update()
        self.best_move = None

    def set_state(self, board):
        self.state = copy.deepcopy(board)

    # basic min max will add alpha beta prunning after
    def minmax(self, state, depth, max_player= True, move = None):
        if depth == 0 or self.terminal(max_player):
            return self.heuristic(), move
        if  max_player:
            return self.max_value(self.state, depth)
        else:
            return self.min_value(self.state, depth)
        return self.best_move

    def max_value(self, state, depth):
        max_eval = float('-inf')
        best_move = None
        holder = self.moves(self.ai_pieces)
        for moveset in holder:
            location = moveset.pop()
            for move in moveset:
                evaluation = self.minmax(self.state.move_piece(location,move), depth-1, False, move)
                max_eval = max(evaluation[0], max_eval)
                if max_eval == evaluation[0]:
                    best_move = move
                    self.best_move = [move, location]
                    
        
        return max_eval, best_move


    def min_value(self,state, depth):
        min_eval = float('inf')
        best_min = None
        holder = self.moves(self.opponent_pieces)
        for moveset in holder:
            location = moveset.pop()
            for move in moveset:
                evaluation = self.minmax(self.state.move_piece(location, move), depth-1, True, move)
                min_eval = min(evaluation[0], min_eval)
                if min_eval == evaluation[0]:
                    best_min = move
        return min_eval, best_min


    # simple fuction for updating each players pieces
    def pieces_update(self):
        for x in range(8):
            for y in range(8):
                if (self.state.location((x,y)).color == BLACK and self.state.location((x,y)).occupant !=None):
                    if (self.state.location((x,y)).occupant.color == self.color):
                        self.ai_pieces.append((x,y))
                    elif (self.state.location((x,y)).occupant.color == self.opponent_color):
                        self.opponent_pieces.append((x,y))


    # heuristic used for minmax
    def heuristic(self):
        return  len(self.ai_pieces) - len(self.opponent_pieces)

    # gives a list of moved assoictated with each piece 
    def moves(self, player_pieces):
        moves = []
        if self.state.check_for_jumps_available(self.color) == True:
            for i in range(0, len(player_pieces)):
                check = self.state.legal_moves(player_pieces[i],True)
                check.append(player_pieces[i])
                if len(check) >= 2:
                    moves.append(check)
        else:        
            for i in range(0,len(player_pieces)):
               check = self.state.legal_moves(player_pieces[i])
               check.append(player_pieces[i])
               if len(check) >= 2:
                   moves.append(check)
        return moves
    
    # returns best move with starting location 
    def get_move(self):
        if self.best_move ==None:
            self.full_piece_update()
            self.minmax(self.state,3)
        return self.best_move

    # might still need an update for the opptuninate
    # this funciton switch out the best move and moves it to ai list 
    def move_update(self):
        self.ai_pieces = [i for i in self.ai_pieces if i != self.best_move[1]] 
        self.ai_pieces.append(self.best_move[0])

    # checks for basic termnial game situations 
    def terminal(self, max_player):
        if max_player == True:
            check = self.moves(self.ai_pieces)
            if len(check) == 0:
                return True
            else:
                return False
        elif max_player == False:
            check = self.moves(self.opponent_pieces)
            if len(check) == 0:
                return True
            else:
                return False



