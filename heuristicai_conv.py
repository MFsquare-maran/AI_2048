import random
import game
import sys
import numpy as np

# Definieren der möglichen Züge
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    """
    Findet den besten Zug für das aktuelle Board.
    Ruft die Funktion find_best_move_agent auf, um den besten Zug basierend auf einer Heuristik zu bestimmen.
    """
    return find_best_move_agent(board)

def find_best_move_agent(board):
    """
    Testet alle möglichen Züge und wählt den Zug aus, der das beste heuristische Ergebnis liefert.
    Wenn kein Zug das Board verändert, wird ein zufälliger Zug gewählt.
    """
    bestmove = -1
    bestscore = -float('inf')
    
    for move in [UP, DOWN, LEFT, RIGHT]:
        newboard = execute_move(move, np.copy(board))
        
        if not board_equals(board, newboard):  # Überprüft, ob der Zug das Board verändert hat
            score = heuristic(newboard,board,move)
            if score > bestscore:
                bestscore = score
                bestmove = move
            print("Move Score" , bestscore)
    
    # Wenn kein gültiger Zug gefunden wurde (z.B. bei einem Game Over), wähle einen zufälligen Zug
    if bestmove == -1:
        bestmove = find_best_move_random_agent()
        
    return bestmove

def heuristic(newboard,board,move):
    return score_board(newboard)



def score_board(board):
    r = 2

    weights = np.array([[r**8, r**7, r**6, r**5], [r**1, r**2, r**3, r**4.9], [r**0, r**-1, r**-2, r**-3], [r**-7,r**-6 , r**-5, r**-4]])


    return sum(np.multiply(board,weights).flatten())

def execute_move(move, board):
    """
    Führt den Zug aus und gibt das neue Board zurück. Das Hinzufügen einer neuen Zufalls-Kachel wird hier nicht berücksichtigt.
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
        sys.exit("Kein gültiger Zug")

def board_equals(board, newboard):
    """
    Vergleicht zwei Boards und prüft, ob sie gleich sind.
    """
    return np.array_equal(newboard, board)

def find_best_move_random_agent():
    """
    Gibt einen zufälligen Zug zurück, falls kein besserer Zug gefunden werden konnte.
    """
    return random.choice([UP, DOWN, LEFT, RIGHT])
