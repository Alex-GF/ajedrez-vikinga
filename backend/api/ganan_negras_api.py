def get(state, movements_number):

    win = False

    if movements_number == 0 and state[1] == 2:
        win = True
    elif king_captured(state[0]):
        win = True

    return win

#------------------------- Funciones auxiliares ----------------------------

def king_captured(board_state):

    captured = True

    for row in board_state:
        
        for cell in row:

            if cell == 3:

                captured = False
    
    return captured