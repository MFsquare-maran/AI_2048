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
            score = heuristic(newboard)
            if score > bestscore:
                bestscore = score
                bestmove = move
    
    # Wenn kein gültiger Zug gefunden wurde (z.B. bei einem Game Over), wähle einen zufälligen Zug
    if bestmove == -1:
        bestmove = find_best_move_random_agent()
        
    return bestmove

def heuristic(board):
    """
    Bewertet das Board basierend auf mehreren Faktoren:
    - Anzahl der leeren Felder
    - Höchste Kachel in der Ecke
    - Potenzial für Merges
    - Monotonie der Anordnung
    """
    return (
        empty_tiles(board) * 4 +  # Belohne leere Felder stärker
        max_tile_in_corner(board) * 5 +  # Belohne hohe Kacheln in den Ecken
        merge_potential(board) * 3 +  # Belohne potenzielle Merges
        monotonicity_score(board) * 4  # Belohne monotone Anordnung der Kacheln
    )

def empty_tiles(board):
    """
    Zählt die Anzahl der leeren Felder auf dem Board.
    """
    return len(np.where(board == 0)[0])

def max_tile_in_corner(board):
    """
    Belohnt das Board, wenn die höchste Kachel in einer der vier Ecken liegt.
    """
    max_tile = np.max(board)
    if board[0][0] == max_tile:
        return max_tile
    return 0

def merge_potential(board):
    """
    Bewertet das Potenzial für Merges auf dem Board.
    - Gehe alle Reihen und Spalten durch und suche nach benachbarten Kacheln mit dem gleichen Wert.
    """
    score = 0
    for i in range(4):
        for j in range(3):  # Bis 3, da wir nur benachbarte Kacheln vergleichen
            if board[i][j] == board[i][j+1]:  # Horizontale Merges
                score += board[i][j]
            if board[j][i] == board[j+1][i]:  # Vertikale Merges
                score += board[j][i]
    return score

def monotonicity_score(board):
    """
    Bewertet das Board basierend auf der Monotonie der Anordnung der Kacheln.
    Belohnt eine Anordnung, bei der die Kacheln von oben links nach unten rechts abnehmen.
    """
    score = 0
    
    for i in range(3):  # Für die ersten 3 Zeilen
        for j in range(3):  # Für die ersten 3 Spalten
            if board[i][j] >= board[i+1][j]:  # Vertikale Monotonie
                score += board[i][j]
            if board[i][j] >= board[i][j+1]:  # Horizontale Monotonie
                score += board[i][j]
    
    # Höhere Belohnung, wenn die größte Kachel oben links ist
    if board[0][0] == np.max(board):
        score += np.max(board) * 2
    
    return score

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


"""
Erklärung:
find_best_move: Diese Funktion wird aufgerufen, um den besten Zug für das aktuelle Board zu finden. Sie verwendet die Funktion find_best_move_agent, um den besten Zug basierend auf einer Heuristik zu bestimmen.

find_best_move_agent: Diese Funktion testet alle möglichen Züge (nach oben, unten, links, rechts). Für jeden Zug wird eine Kopie des Boards erstellt, der Zug ausgeführt und das neue Board bewertet. Der Zug mit dem besten heuristischen Wert wird ausgewählt. Falls kein Zug das Board verändert, wird ein zufälliger Zug gewählt.

heuristic: Diese Funktion berechnet eine Bewertung für das Board basierend auf vier Faktoren: Anzahl der leeren Felder, höchste Kachel in der Ecke, Potenzial für Merges und Monotonie der Kachel-Anordnung.

empty_tiles: Gibt die Anzahl der leeren Felder auf dem Board zurück.

max_tile_in_corner: Belohnt das Board, wenn die höchste Kachel in einer der vier Ecken liegt.

merge_potential: Bewertet das Potenzial, benachbarte Kacheln zusammenzuführen.

monotonicity_score: Bewertet das Board basierend auf der Monotonie der Kachel-Anordnung, wobei eine Abnahme von oben links nach unten rechts bevorzugt wird.

execute_move: Führt den angegebenen Zug aus und gibt das neue Board zurück, ohne eine neue Kachel hinzuzufügen.

board_equals: Vergleicht zwei Boards und prüft, ob sie gleich sind.

find_best_move_random_agent: Gibt einen zufälligen Zug zurück, falls kein besserer Zug gefunden werden konnte.

Diese Funktionen arbeiten zusammen, um den besten Zug für das 2048-Spiel zu finden, indem sie verschiedene Aspekte des Boards bewerten und analysieren.
"""
