#from players import * 
# player import was being useed for inherinency I dont 
# think I need this any more 
from game import *
from board import *
import math


class Aiplayer():
    def __init__(self):
        self.game = None  


    # basic min max will add alpha beta prunning after  
    def minmax(self, posistion, depth, max_player, board):
        if depth == 0 or position.winner() != None: 
            return postions.eval() #reutrn heurtisitc value of the node 
        if  max_player:
            player.max_value()
        else:
            player.min_value()

    #alpha to be implemented later 
    def max_value(self, posisiton, depth, alpha=0):
        max_eval = float('-inf') 
        best_move = None
        for move in posotion.legal_moves():
             evaluation = minimax(move, depth-1, False, board)
             max_eval = max(evalution, max_eval)
             if max_eval == evalution:
                 best_move = move 
        return best_move , max_eval


    def min_value(self,position, depth, beta = 0):
        min_eval = float('inf')
        best_min = None
        for move in possiton.legal_moves():
            evaluation = min(evalution, min_eval)
            if min_eval == evalution:
                best_move = move
        return best_move, min_eval 






