from .game import *
from .board import *
import math
import copy
from itertools import chain


class Aiplayer():
    def __init__(self, board, color="L"):
        self.state = copy.deepcopy(board)
        self.color = color
        self.opponent_color = "D"
        self.ai_pieces= []
        self.opponent_pieces= []
        self.initial_state(self.color)
        self.best_move= None


    # basic min max will add alpha beta prunning after
    def minmax(self, state, depth, max_player= True, move = None):
        if depth == 0 or self.terminal(max_player):
            return self.heuristic(), move
        if  max_player:
            return self.max_value(self.state, depth)
        else:
            return self.min_value(self.state, depth)
        return self.best_move

    #alpha to be implemented later
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

    # set the initial stat of both player pieces
    def initial_state(self, color):
        if color == "D":
            self.opponent_pieces = [(0,1),(1,0),(1,2),(2,1),
            (3,0),(3,2),(4,1),(5,0),(5,2),(6,1),(7,0),(7,2)]
            self.ai_pieces = [(0,5),(0,7),(1,6),(2,5),
            (2,7),(3,6),(4,5),(4,7),(5,6),(6,5),(6,7),(7,6)]
        elif color == "L":
            self.ai_pieces = [(0,1),(1,0),(1,2),(2,1),
            (3,0),(3,2),(4,1),(5,0),(5,2),(6,1),(7,0),(7,2)]
            self.opponent_pieces = [(0,5),(0,7),(1,6),(2,5),
            (2,7),(3,6),(4,5),(4,7),(5,6),(6,5),(6,7),(7,6)]


    # there are bugs in this function 
    # simple fuction for updating each players pieces
    def pieces_update(self):
        for i in range(0, len(self.ai_pieces)):
            check = self.ai_pieces[i]
            if self.state.matrix[check[0]][check[1]].get_square()[1]== None:
                self.ai_pieces.pop(i)
            elif self.state.matrix[check[0]][check[1]].get_square()[1].get_piece()[1] != self.color:
                self.ai_pieces.pop(i)
        for i in range(0, len(self.opponent_pieces)):
            check2 = self.opponent_pieces[i]
            if self.state.matrix[check2[0]][check2[1]].get_square() == None:
                self.opponent_pieces.pop(i)
            elif self.state.matrix[check2[0]][check2[1]].get_square()[1].get_piece()[1] != self.opponent_color:
                self.opponent_pieces.pop(i)

    def heuristic(self):
        return  len(self.ai_pieces) - len(self.opponent_pieces)

    def moves(self, player_pieces):
        moves = []
        for i in range(0,len(player_pieces)):
           check = self.state.legal_moves(player_pieces[i])
           check.append(player_pieces[i])
           if len(check) >= 2:
               moves.append(check)
        return moves

    def get_move(self):
        return self.best_move


    # might still need an update for the opptuninate
    # this funciton switch out the best move and moves it to ai list 
    def move_update(self):
        self.ai_pieces = [i for i in self.ai_pieces if i != self.best_move[1]] 
        self.ai_pieces.append(self.best_move[0])




    def terminal(self, max_player):
        if max_player == True:
            check = self.moves(self.ai_pieces)
            if check == []:
                return True
            else:
                return False
        elif max_player == False:
            check = self.moves(self.opponent_pieces)
            if check == []:
                return True
            else:
                return False


