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
    """
    Bewertet das Board basierend auf mehreren Faktoren:
    - Anzahl der leeren Felder
    - Höchste Kachel in der Ecke
    - Potenzial für Merges
    - Monotonie der Anordnung
    """
    
    return (
        (empty_tiles(newboard) * 7 +  # Belohne leere Felder stärker
        max_tile_in_corner(newboard) * 10000  +  # Belohne hohe Kacheln in den Ecken
        merge_potential(newboard) * 10 +  # Belohne potenzielle Merges
        monotonicity_score(newboard) * 5 + # Belohne monotone Anordnung der Kacheln
        stayleft(newboard) * 10000 +
        forceleft(board,move) * 1 +
        forceup(board,move) * 1
        )
        * down_allowed(newboard,move) * right_allowed(newboard,move) #prioleftup(move) * 100
        

         
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
