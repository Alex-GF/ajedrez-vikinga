def get(state, movements_number):

    win = False

    if (movements_number == 0 and state[1] == 1) or king_escaped(state[0]):
        win = True

    return win

#------------------------- Funciones auxiliares ----------------------------

def king_escaped(board_state):

    escaped = False

    for row in board_state:
        
        # Suponemos n el id de la casilla que se encuentra al final de la fila/columna

        n = len(row)-1
        
        if board_state[0][0] == 3 or board_state[0][n] == 3 or board_state[n][0] == 3 or board_state[n][n] == 3:
            
            escaped = True
            
    return escaped