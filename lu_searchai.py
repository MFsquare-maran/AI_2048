import random
import game
import sys
import numpy as np
import math

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

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
    
    return expectimax(newboard, 4, chance = True)
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

"""def score_board(board):

    score = 0

    # Weight matrices for tile position evaluation
    position_weights = [
        [32768, 16384, 8192, 4096],
        [256, 512, 1024, 2048],
        [128, 64, 32, 16],
        [1, 2, 4, 8]
    ]

    # Weight matrix for monotonicity evaluation
    monotonicity_weights = [
        [0.125, 0.25, 0.5, 1],
        [0.25, 0.5, 1, 2],
        [0.5, 1, 2, 4],
        [1, 2, 4, 8]
    ]

    # Calculate tile position score
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                score += board[i][j] * position_weights[i][j]

    # Calculate monotonicity score
    monotonicity_score = 0
    for i in range(4):
        for j in range(3):
            if board[i][j] >= board[i][j + 1]:
                monotonicity_score += board[i][j + 1] * monotonicity_weights[i][j]
            if board[j][i] >= board[j + 1][i]:
                monotonicity_score += board[j + 1][i] * monotonicity_weights[j][i]

    # Calculate smoothness score
    smoothness_score = 0
    for i in range(4):
        for j in range(3):
            if board[i][j] != 0:
                k = j + 1
                while k < 4 and board[i][k] == 0:
                    k += 1
                if k < 4:
                    smoothness_score -= abs(board[i][j] - board[i][k])

    # Calculate the maximum tile value

    # Final score calculation
    score += monotonicity_score
    score += smoothness_score

    return score"""


def score_board(board):

    score1 = 0
    r = 2

    weights = np.array([[r**8, r**7, r**6, r**5], [r**1, r**2, r**3, r**4.9], [r**0, r**-1, r**-2, r**-3], [r**-7,r**-6 , r**-5, r**-4]])


    return sum(np.multiply(board,weights).flatten())

"""
def score_board(board):
    # Define your evaluation parameters
    # You can assign different weights to these parameters
    empty_cells = np.count_nonzero(board == 0)
    max_tile = np.max(board)
    smoothness = calculate_smoothness(board)
    snake_pattern = calculate_snake_pattern(board)
    
    # Define your weights for each parameter
    weight_empty_cells = 100.0
    weight_max_tile = 50.0
    weight_smoothness = 1.0
    weight_snake_pattern = 1.0
    
    # Calculate the final evaluation score
    score = (empty_cells * weight_empty_cells) + (math.log2(max_tile) * weight_max_tile) + (smoothness * weight_smoothness) + (snake_pattern * weight_snake_pattern)
    
    return score

# Helper function to calculate smoothness
def calculate_smoothness(board):
    smoothness = 0

    # Check horizontal smoothness
    for row in board:
        for i in range(len(row) - 1):
            if row[i] > 0 and row[i] == row[i + 1]:
                smoothness += math.log2(row[i]) - 1

    # Check vertical smoothness
    for col in range(len(board[0])):
        for i in range(len(board) - 1):
            if board[i][col] > 0 and board[i][col] == board[i + 1][col]:
                smoothness += math.log2(board[i][col]) - 1

    return -smoothness  # We want to minimize smoothness

# Helper function to calculate snake pattern
def calculate_snake_pattern(board):
    snake_pattern = 0
    snake_head = None

    for i in range(len(board)):
        if i % 2 == 0:
            for j in range(len(board[i])):
                if snake_head is None:
                    snake_head = (i, j)
                else:
                    row_diff = abs(snake_head[0] - i)
                    col_diff = abs(snake_head[1] - j)
                    snake_pattern += max(row_diff, col_diff)

    return -snake_pattern  # We want to maximize the snake pattern


"""
"""
def score_board(board):

    #score the board

    r = np.array([0.125**i for i in range(16)])
    scores = []

    for pos in [
        [[0, 0], [0, 1], [0, 2], [0, 3],
         [1, 3], [1, 2], [1, 1], [1, 0],
         [2, 0], [2, 1], [2, 2], [2, 3],
         [3, 3], [3, 2], [3, 1], [3, 0]],
        [[0, 3], [0, 2], [0, 1], [0, 0],
         [1, 0], [1, 1], [1, 2], [1, 3],
         [2, 3], [2, 2], [2, 1], [2, 0],
         [3, 0], [3, 1], [3, 2], [3, 3]],
        [[3, 0], [2, 0], [1, 0], [0, 0],
         [0, 1], [1, 1], [2, 1], [3, 1],
         [3, 2], [2, 2], [1, 2], [0, 2],
         [0, 3], [1, 3], [2, 3], [3, 3]],
        [[3, 3], [2, 3], [1, 3], [0, 3],
         [0, 2], [1, 2], [2, 2], [3, 2],
         [3, 1], [2, 1], [1, 1], [0, 1],
         [0, 0], [1, 0], [2, 0], [3, 0]]
    ]:
        sub_board = board[np.ix_([pos[i][0] for i in range(16)], [pos[i][1] for i in range(16)])]
        scores.append(np.multiply(sub_board,r))

    return np.max(scores)# + np.count_nonzero(board == 0) * 10
"""
""""
def generate_boards(board):
    
    #add a 2 or 4 to all empty tiles
    
    newboards = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                newboard = board.copy()
                newboard[i][j] = 2
                newboards.append(execute_move(0,newboard))
                newboards.append(execute_move(1,newboard))
                newboards.append(execute_move(2,newboard))
                newboards.append(execute_move(3,newboard))
    
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                newboard = board.copy()
                newboard[i][j] = 4
                newboards.append(execute_move(0,newboard))
                newboards.append(execute_move(1,newboard))
                newboards.append(execute_move(2,newboard))
                newboards.append(execute_move(3,newboard))

    return newboards
"""

def expectimax(board, depth, chance=False):
    """
    Expectimax algorithm
    """
    max_score = 0
    if depth == 0:
        return score_board(board)          #return whatever should be returned
    
    

    if(chance == True):
        expected_score = 0
        counter = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    newboard2 = board.copy()
                    #newboard4 = board.copy()
                    newboard2[i][j] = 2
                    #newboard4[i][j] = 4
                    expected_score += (
                        expectimax(newboard2, depth-1, chance= False)
                        #0.1 * expectimax(newboard4, depth-1)
                    )
                    counter += 1

                    if expected_score/counter > max_score:
                        max_score = expected_score/counter


                    




    elif(chance == False):
        
        for i in range(4):
            #board2 = board.copy()
            moved_board = execute_move(i, board)
            total_score = 0

            if not board_equals(board, moved_board):
                current_score = score_board(moved_board)

                total_score = expectimax(moved_board, depth-1, chance = True)
                
                #future_score = expectimax(moved_board, depth-1, True)

                #total_score += future_score
                if total_score > max_score:
                    max_score = total_score

    return max_score


    
    #print(newboards)

    
    