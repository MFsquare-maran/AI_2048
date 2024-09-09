import random
import game
import sys
import numpy as np

# Definition der möglichen Bewegungen: Hoch, Runter, Links, Rechts
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

# Diese Funktion findet den besten Zug für das aktuelle Spielbrett
def find_best_move(board):
    bestmove = -1  # Initialisierung des besten Zugs auf -1 (kein Zug gefunden)
    board_1 = board  # Kopie des aktuellen Spielbretts
    
    # Das ist ein Beispielbrett, es ist hier als Kommentar zu sehen:
    # board [[ 2  4  2  4]
    #        [ 4  2  4  2]
    #        [ 2 16 64  4]
    #        [ 8  4 16  2]]

    # TODO: Hier sollte der Spieler eine Heuristik bauen, die besser als der Zufallsagent ist.
    # Es muss nicht zwingend ein perfekter Agent sein, aber besser als zufällige Züge.

    # Wenn der zufällige Agent genutzt würde, wäre der Code wie folgt:
    # bestmove = find_best_move_random_agent()
    
    # Wir benutzen jedoch einen heuristischen Agenten:
        
        
        
    bestmove = find_best_move_agent(board_1)
    #bestmove = find_best_move_random_agent()
    
    
    return bestmove  # Gibt den besten gefundenen Zug zurück

# Dieser Agent wählt eine zufällige Bewegung
def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])  # Wählt zufällig eine der 4 Richtungen

# Dieser Agent versucht, den besten Zug durch Heuristik zu finden
def find_best_move_agent(board):
    bestmove = -1  # Initialisiert den besten Zug
    bestscore = -float('inf')  # Der beste Score startet bei -∞ (kleinstmöglicher Wert)
    
    # Probiert jede mögliche Bewegung aus (Hoch, Runter, Links, Rechts)
    for move in [UP, DOWN, LEFT, RIGHT]:
        newboard = execute_move(move, np.copy(board))  # Führt die Bewegung aus
        
        # Wenn das neue Board nicht identisch mit dem alten ist (d.h. eine Veränderung erfolgt):
        if not board_equals(board, newboard):
            score = heuristic(newboard)  # Berechnet den Heuristik-Score für das neue Board
            if score > bestscore:  # Wenn der neue Score besser ist:
                bestscore = score  # Speichere den neuen besten Score
                bestmove = move  # Speichere den zugehörigen besten Zug
    
    # Wenn kein Zug gefunden wurde (z.B. Spielende), wähle einen zufälligen Zug:
    if bestmove == -1:
        bestmove = find_best_move_random_agent()
        
    return bestmove  # Gibt den besten Zug zurück

# Diese Heuristik-Funktion bewertet das Spielbrett und gibt eine Punktzahl zurück
def heuristic(board):
    return max_tile_in_corner(board) + empty_tiles(board)
    # Die Bewertung basiert darauf, ob die größte Kachel in einer Ecke ist
    # und wie viele leere Felder (0er) auf dem Brett vorhanden sind.

# Diese Funktion belohnt das Platzieren der größten Kachel in einer Ecke
def max_tile_in_corner(board):
    max_tile = np.max(board)  # Findet die größte Kachel auf dem Brett
    corners = [board[0][0], board[0][-1], board[-1][0], board[-1][-1]]  # Ecken des Bretts
    return max_tile if max_tile in corners else 0  # Gibt den Wert der Kachel zurück, wenn sie in einer Ecke ist, sonst 0

# Diese Funktion belohnt leere Felder (0er) auf dem Spielbrett
def empty_tiles(board):
    return len(np.where(board == 0)[0])  # Zählt die Anzahl der leeren Felder (0er) auf dem Brett

# Führt eine Bewegung auf dem Brett aus und gibt das neue Brett zurück
def execute_move(move, board):
    """
    Führt den Zug auf dem Brett aus und gibt das neue Brett ohne neues zufälliges Tile zurück.
    Es beeinflusst nicht den Spielzustand im Browser.
    """
    if move == UP:
        return game.merge_up(board)  # Führt einen 'Hoch'-Zug aus
    elif move == DOWN:
        return game.merge_down(board)  # Führt einen 'Runter'-Zug aus
    elif move == LEFT:
        return game.merge_left(board)  # Führt einen 'Links'-Zug aus
    elif move == RIGHT:
        return game.merge_right(board)  # Führt einen 'Rechts'-Zug aus
    else:
        sys.exit("Kein gültiger Zug")  # Falls ein ungültiger Zug übergeben wurde

# Diese Funktion prüft, ob zwei Bretter identisch sind
def board_equals(board, newboard):
    """
    Prüft, ob zwei Bretter identisch sind
    """
    return np.array_equal(newboard, board)  # Vergleicht die beiden Bretter pixelgenau
