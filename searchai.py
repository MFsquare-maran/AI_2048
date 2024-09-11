import random
import game
import sys
import numpy as np
import math

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    """
    find the best move for the next turn.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]
    
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return bestmove
    
def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    score = []
    newboard = execute_move(move, board)

    if board_equals(board,newboard):
        return -1
    
    return expectimax(newboard,board,move, 5, chance = True)
    #return max(score)

	# TODO:
	# Implement the Expectimax Algorithm.
	# 1.) Start the recursion until it reach a certain depth
	# 2.) When you don't reach the last depth, get all possible board states and 
	#		calculate their scores dependence of the probability this will occur. (recursively)
	# 3.) When you reach the leaf calculate the board score with your heuristic.
    #return random.randint(1,1000)

def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")
        
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()


def score_board(board1,board0,move):

    return (
        (empty_tiles(board1) * 7 +  # Belohne leere Felder stärker
        max_tile_in_corner(board1) * 10000  +  # Belohne hohe Kacheln in den Ecken
        merge_potential(board1) * 10 +  # Belohne potenzielle Merges
        monotonicity_score(board1) * 5 + # Belohne monotone Anordnung der Kacheln
        stayleft(board1) * 10000 +
        forceleft(board0,move) * 1 +
        forceup(board0,move) * 1
        )
        * down_allowed(board1,move) * right_allowed(board1,move) #prioleftup(move) * 100
        

         
    )

         




"""
forceleft(board,move) * 100000 +
forceup(board,move) * 1000000
"""
"""
def prioleftup(move):
    
    if move == UP or move == LEFT:
        return 1
    else:
        return 0
"""

def forceleft(board,move):
    score = 0
    if move == LEFT:
        if board[0][0] == board[0][1]:
            score += board[0][0]
            
        if board[1][0] == board[1][1]:
            score += board[1][0]
        
        if board[2][0] == board[2][1]:
            score += board[2][0]
            
        if board[3][0] == board[3][1]:
            score += board[3][0]
        return score 
    return 0
            

def forceup(board,move):
    if move == UP:
        if board[0][0] == board[1][0]:
            return board[0][0]
            
        if board[1][0] == board[2][0]:
            return board[1][0]
        
        if board[2][0] == board[3][0]:
            return board[2][0]

        return 0 
    return 0
        

def stayleft(newboard):
    
    
    # Maximalwert ermitteln
    max_tile = np.max(newboard)

    # Zweithöchste Zahl ermitteln
    second_highest = np.max(newboard[newboard != max_tile])

    # Dritthöchste Zahl ermitteln, indem du das Maximum und das Zweithöchste entfernst
    try:
        third_highest = np.max(newboard[(newboard != max_tile) & (newboard != second_highest)])
    except:
        third_highest = 0
        
    if newboard[1][0] == second_highest:
        if newboard[2][0] == third_highest:
            #return second_highest+third_highest
            return 2
            
        #return second_highest
        return 1
    
    return 0


    
def down_allowed(newboard, move):
    if move == DOWN:
        for i in range(3):
            if newboard[0][i] == 0:
                return 0
            else:
                return 1
    else:
        return 1
def right_allowed(newboard, move):
    if move == RIGHT:
        for i in range(3):
            if newboard[i][0] == 0:
                return 0
            else:
                return 1
    else:
        return 1


def empty_tiles(newboard):
    """
    Zählt die Anzahl der leeren Felder auf dem Board.
    """
    return len(np.where(newboard == 0)[0])

def max_tile_in_corner(newboard):
    """
    Belohnt das Board, wenn die höchste Kachel in einer der vier Ecken liegt.
    """
    max_tile = np.max(newboard)
    if newboard[0][0] == max_tile:
        return max_tile
    return 0




def merge_potential(newboard):
    """
    Bewertet das Potenzial für Merges auf dem Board.
    - Gehe alle Reihen und Spalten durch und suche nach benachbarten Kacheln mit dem gleichen Wert.
    """
    score = 0
    for i in range(4):
        for j in range(3):  # Bis 3, da wir nur benachbarte Kacheln vergleichen
            if newboard[i][j] == newboard[i][j+1]:  # Horizontale Merges
                score += newboard[i][j]
                #score+= 1
            if newboard[j][i] == newboard[j+1][i]:  # Vertikale Merges
                score += newboard[j][i]
                #score+= 1
    return score

def monotonicity_score(newboard):
    """
    Bewertet das Board basierend auf der Monotonie der Anordnung der Kacheln.
    Belohnt eine Anordnung, bei der die Kacheln von oben links nach unten rechts abnehmen.
    """
    score = 0
    
    for i in range(3):  # Für die ersten 3 Zeilen
        for j in range(3):  # Für die ersten 3 Spalten
            if newboard[i][j] >= newboard[i+1][j]:  # Vertikale Monotonie
                #score += board[i][j]
                score+= 1
            if newboard[i][j] >= newboard[i][j+1]:  # Horizontale Monotonie
                score+= 1
                #score += board[i][j]
    

    
    return score




def expectimax(board1,board0,move, depth, chance=False):
    """
    Expectimax algorithm
    """
    max_score = 0
    if depth == 0:
                 #return whatever should be returned
        return score_board(board1,board0,move)
    
    

    if(chance == True):
        expected_score = 0
        counter = 0
        for i in range(4):
            for j in range(4):
                if board1[i][j] == 0:
                    board2 = board1.copy()
                    #newboard4 = board.copy()
                    board2[i][j] = 2
                    #newboard4[i][j] = 4
                    expected_score += (
                        expectimax(board2,board1,move, depth-1, chance= False)
                        #0.1 * expectimax(newboard4, depth-1)
                    )
                    counter += 1

                    if expected_score/counter > max_score:
                        max_score = expected_score/counter


    elif(chance == False):
        
        for i in range(4):
            #board2 = board.copy()
            moved_board = execute_move(i, board0)
            total_score = 0

            if not board_equals(board0, moved_board):
                current_score = score_board(moved_board,board0,move)

                total_score = expectimax(moved_board,board0,i, depth-1, chance = True)
                
                #future_score = expectimax(moved_board, depth-1, True)

                #total_score += future_score
                if total_score > max_score:
                    max_score = total_score

    return max_score


    
    #print(newboards)

    
    