import random
import game
import sys
import numpy as np
import math


# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.
ground_depth = 4



def find_best_move(board,score):
    """
    find the best move for the next turn.
    """
    
    """
    find the best move for the next turn.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]
    
    result = [score_toplevel_move(i, board,score) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return bestmove
    
def score_toplevel_move(move, board,total_score):
    """
    Entry Point to score the first move.
    """
    depth = 1
    
    amount_of_nummers = count_unique_numbers(board)
    depth = int(((count_unique_numbers(board))/2)+0.5)
    #depth = int(math.exp((amount_of_nummers-2) / 5.9)+1.5)
    
    
    if depth == 0:
        depth = 1
    
    
    
    

    print("unique nummer", amount_of_nummers)
    print("Tiefe =", depth)
    
    

    score = []
    newboard = execute_move(move, board)

    if board_equals(board,newboard):
        return -1
    

    return expectimax(newboard, depth, chance = True)



def count_unique_numbers(matrix):
    # Umwandlung der Matrix in eine flache Liste
    flattened_matrix = np.array(matrix).flatten()
    
    # Verwende die Funktion 'np.unique', um die eindeutigen Werte zu zählen
    unique_numbers = np.unique(flattened_matrix)
    
    return len(unique_numbers)

def count_zeros(board):
   
    return len(np.where(board == 0)[0])
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

def score_board(board):

    score1 = 0
    r = 2

    # 82664 weights = np.array([[r**8, r**7, r**6, r**5], 
                                #[r**1, r**2, r**3, r**4.9], 
                                #[r**0, r**-1, r**-2, r**-3], 
                                #[r**-7,r**-6 , r**-5, r**-4]])
                                
    # 161936 weights = np.array([[r**15, r**1, r**0.9, r**-7],
                        #[r**7, r**2, r**-1, r**-6], 
                        #[r**6, r**3, r**-2, r**-5], 
                        #[r**5,r**4.9,r**-3, r**-3.1]])
    
    #129344 weights = np.array([[r**15, r**1, r**0.9, r**-7],
                        #[r**10, r**2, r**-1, r**-6], 
                        #[r**8, r**3, r**-2, r**-5], 
                        #[r**5,r**4.9,r**-3, r**-3.1]])
    
    weights = np.array([[r**15, r**1, r**0, r**-7],
                        [r**7, r**2, r**-1, r**-6], 
                        [r**6, r**3, r**-2, r**-5], 
                        [r**5,r**4.9,r**-3, r**-4]])

    # 69908 weights = np.array([[r**8,r**6,r**3,r**-1],
                                #[r**7,r**4,r**0,r**-4],
                                #[r**5,r**1,r**-3,r**-6],
                                #[r**2,r**-2,r**-5,r**-7]])

    # 25620 weights = np.array([[r**8,r**3.9,r**2.8,r**-0.5],
                        #[r**7,r**4,r**3,r**0],
                        #[r**6,r**5,r**2,r**1],
                        #[r**4.9,r**4.8,r**3.8,r**-1]])

    return sum(np.multiply(board,weights).flatten())#+merge_potential(board)

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

def expectimax(board, depth, chance=False):
    """
    Expectimax algorithm
    """
    max_score = 0
    if depth == 0:
        return score_board(board)  # Blattknoten erreicht, also heuristischen Score berechnen
    
    if chance == True:
        expected_score = 0
        counter = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:  # Leeres Feld gefunden
                    newboard2 = board.copy()
                    newboard4 = board.copy()
                    
                    newboard2[i][j] = 2  # Setze eine 2 auf das leere Feld
                    newboard4[i][j] = 4  # Setze eine 4 auf das leere Feld
                    
                    # Berechne den erwarteten Score unter Berücksichtigung der Wahrscheinlichkeiten
                    expected_score += (
                        0.9 * expectimax(newboard2, depth-1, chance=False) +  # 90% Wahrscheinlichkeit für 2
                        0.1 * expectimax(newboard4, depth-1, chance=False)    # 10% Wahrscheinlichkeit für 4
                    )
                    counter += 1
        
        if counter > 0:
            return expected_score / counter  # Durchschnitt der erwarteten Scores
        else:
            return 0  # Kein leeres Feld verfügbar
    
    elif chance == False:  # Spielerzug
        for i in range(4):  # Probiere jeden möglichen Zug (UP, DOWN, LEFT, RIGHT)
            moved_board = execute_move(i, board)
            if not board_equals(board, moved_board):  # Nur wenn der Zug das Spielfeld verändert
                total_score = expectimax(moved_board, depth-1, chance=True)  # Rekursiv weitermachen
                if total_score > max_score:
                    max_score = total_score

    return max_score
