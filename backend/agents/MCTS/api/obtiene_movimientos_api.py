import random

def get(state):
    board = state[0]
    turn = state[1]
    result = []
    movements = []    
    row_counter = 0
    col_counter = 0
    movement = ()
    
    for line in board:
        for cell in line:
            if cell == turn or (cell == 3 and turn == 2):
                movement = (row_counter, col_counter)
                movements.append(movement)
            col_counter += 1
        col_counter = 0
        row_counter += 1
    
    if not movements:
        return result
    
    for movement in movements:
        result += get_movements(movement, board)
        
    random.shuffle(result)
    
    return result

#------------------------- Funciones auxiliares ----------------------------

def get_movements(movement, board):
    size = len(board)
    throne = round(size/2)-1
    
    result = get_right(movement, board, size, throne)
    result += get_left(movement, board, size, throne)
    result += get_up(movement, board, size, throne)
    result += get_down(movement, board, size, throne)
    
    return result

def get_cell(board, row_movement, col_movement):
    return board[row_movement][col_movement]

def is_free_cell(board, row_movement, col_movement):
    return get_cell(board, row_movement, col_movement) == 0

def get_up(movement, board, size, throne_col):
    row_movement, col_movement = movement
    result = []
    new_row = row_movement

    min_size = 0 if (col_movement!=0 and col_movement!=size-1) or get_cell(board, row_movement, col_movement)==3 else 1
    while new_row>min_size and is_free_cell(board, new_row-1, col_movement):
        if new_row-1 != throne_col or col_movement != throne_col or get_cell(board, row_movement, col_movement) == 3:
            result += [(row_movement, col_movement, new_row-1, col_movement)]
        new_row-=1
    return result

def get_down(movement, board, size, throne_col):
    row_movement, col_movement = movement
    result = []
    new_row = row_movement

    max_size = size-1 if (col_movement!=0 and col_movement!=size-1) or get_cell(board, row_movement, col_movement)==3 else size-2
    while new_row<max_size and is_free_cell(board, new_row+1, col_movement):
        if new_row+1 != throne_col or col_movement != throne_col or get_cell(board, row_movement, col_movement) == 3:
            result += [(row_movement, col_movement, new_row+1, col_movement)]
        new_row+=1
    return result

def get_right(movement, board, size, throne_row):
    row_movement, col_movement = movement
    result = []
    new_col = col_movement
    
    max_size = size-1 if (row_movement!=0 and row_movement!=size-1)or get_cell(board, row_movement, col_movement)==3 else size-2
    while new_col<max_size and is_free_cell(board, row_movement, new_col+1):
        if row_movement != throne_row or new_col+1 != throne_row or get_cell(board, row_movement, col_movement) == 3:
            result += [(row_movement, col_movement, row_movement, new_col+1)]
        new_col+=1
    return result

def get_left(movement, board, size, throne_row):
    row_movement, col_movement = movement
    result = []
    new_col = col_movement
    
    min_size = 0 if (row_movement!=0 and row_movement!=size-1) or get_cell(board, row_movement, col_movement)==3 else 1
    while new_col>min_size and is_free_cell(board, row_movement, new_col-1):
        if row_movement != throne_row or new_col-1 != throne_row or get_cell(board, row_movement, col_movement) == 3:
            result += [(row_movement, col_movement, row_movement, new_col-1)]
        new_col-=1
    return result