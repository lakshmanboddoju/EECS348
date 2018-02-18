# File: Player.py
# Author(s) names AND netid's: Lakshman Pavan Kumar Boddoju (lpb8177)
# Date: 10/13/2017
# Group work statement: I did this alone.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=8):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0
            
    

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        
        
        move = -1
        score = -INFINITY
        turn = self
                
        alpha = -INFINITY
        beta = INFINITY
        #Initialize the values of Alpha and Beta to -Infinity and +Infinity respectively.
        
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.alphaBetaMinValue(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move
        
    def alphaBetaMaxValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaBetaMinValue(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > beta:
                return s
            alpha = max(alpha, s)
            score = max(score, s)
        return score
    
    def alphaBetaMinValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaBetaMaxValue(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < alpha:
                return s
            beta = min(beta, s)
            score = min(score, s)
        return score
        
    def customMove(self, board, ply):
        
        #custom just has a preset ply value set to 9. Please use the custom player with the scoring function defined in the score function in the class lpb8177(Player)
        
        move = -1
        score = -INFINITY
        turn = self
                
        alpha = -INFINITY
        beta = INFINITY
        #Initialize the values of Alpha and Beta to -Infinity and +Infinity respectively.
        
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.customMinValue(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move
        
    def customMaxValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.customMinValue(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > beta:
                return s
            alpha = max(alpha, s)
            score = max(score, s)
        return score
    
    def customMinValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.customMaxValue(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < alpha:
                return s
            beta = min(beta, s)
            score = min(score, s)
        return score
    
        
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # makes each move in about 10 seconds or less
            
            val, move = self.customMove(board, 9)
            
            #plyvalue set to 9, use the score function defined below to work

            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class lpb8177(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        
        if board.hasWon(self.num):
            return 10000.0
        elif board.hasWon(self.opp):
            return -10000.0
        
        #setting the default values higher so that I dont have to worry the computed score will go out of bound.
        
        else:
            customScore = 0.0
            
            if self.num == 1:
                myScore = board.scoreCups[0]
                oppScore = board.scoreCups[1]
                myPieces = board.P1Cups[:]
                oppPieces = board.P2Cups[:]
            else:
                myScore = board.scoreCups[1]
                oppScore = board.scoreCups[0]
                myPieces = board.P2Cups[:]
                oppPieces = board.P1Cups[:]
            
            #basically using this so that i dont have to write the statements twice for player numbers
            
            
            differenceInScore = myScore - oppScore
            differenceInPieces = sum(myPieces) - sum(oppPieces)
            
            customScore = differenceInScore*10 + differenceInPieces*5
            #Initializing the custom score to be the sum of difference in scores and differencr in pieces (in the cups), but with different weights
            
            i = 0
            while i < 6:
                if myPieces[i] == 0:
                    customScore+=5
                if oppPieces[i] == 0:
                    customScore-=5
                i+=1
            #Checking the cups in the mancala board and rewarding the player if he/she has empty cups, punishing him/her if the opponent has empty cups
            
            if myPieces[5] > 1:
                customScore+=myPieces[5]*80
            #Rewarding the player if they have higher number of peices in their last cup, since those cant be stolen from
            
            if oppPieces[5] > 1:
                customScore-=oppPieces[5]*80
            #Punishing the player if the opponent has higher number of pieces in their last cup, since the player cant steal them
            
            i = 0
            while i < 6:
                if myPieces[i] == i+1:
                    customScore+=500
                if oppPieces[i] == i+1:
                    customScore-=500
                i+=1
            #Checking the stones in the respective cup numbers, and if they are equal to the cup number, they can be used for an extra turn.
            
            return customScore
            