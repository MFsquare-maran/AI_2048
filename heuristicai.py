import random
import game
import sys

import numpy as np

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    # Try all moves and pick the one with the highest heuristic score
    bestmove = -1
    bestscore = -float('inf')
    
    for move in [UP, DOWN, LEFT, RIGHT]:
        newboard = execute_move(move, np.copy(board))
        
        if not board_equals(board, newboard):
            score = heuristic(newboard)
            if score > bestscore:
                bestscore = score
                bestmove = move
    
    if bestmove == -1:  # If no move found (game over situation), fallback to random
        bestmove = find_best_move_random_agent()
        
    return bestmove

def heuristic(board):
    return max_tile_in_corner(board) + empty_tiles(board)

def max_tile_in_corner(board):
    # Reward the largest tile being in a corner
    max_tile = np.max(board)
    corners = [board[0][0], board[0][-1], board[-1][0], board[-1][-1]]
    return max_tile if max_tile in corners else 0

def empty_tiles(board):
    # Reward more empty tiles (0s)
    return len(np.where(board == 0)[0])

def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])

def execute_move(move, board):
    """
    Apply the move and return the new grid without a new random tile 
    It won't affect the state of the game in the browser.
    """
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
    return np.array_equal(newboard, board)
