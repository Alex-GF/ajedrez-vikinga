import random

def get(state):
    board = state[0]
    turn = state[1]
    result = []
    movements = []    
    rowCounter = 0
    colCounter = 0
    movement = ()
    
    for line in board:
        for cell in line:
            if cell == turn or (cell == 3 and turn == 2):
                movement = (rowCounter, colCounter)
                movements.append(movement)
            colCounter += 1
        colCounter = 0
        rowCounter += 1
    
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

def get_cell(board, rowMovement, colMovement):
    return board[rowMovement][colMovement]

def is_free_cell(board, rowMovement, colMovement):
    return get_cell(board, rowMovement, colMovement) == 0

def get_up(movement, board, size, throneCol):
    rowMovement, colMovement = movement
    result = []
    newRow = rowMovement

    minSize = 0 if (colMovement!=0 and colMovement!=size-1) or get_cell(board, rowMovement, colMovement)==3 else 1
    while newRow>minSize and is_free_cell(board, newRow-1, colMovement):
        if newRow-1 != throneCol or colMovement != throneCol or get_cell(board, rowMovement, colMovement) == 3:
            result += [(rowMovement, colMovement, newRow-1, colMovement)]
        newRow-=1
    return result

def get_down(movement, board, size, throneCol):
    rowMovement, colMovement = movement
    result = []
    newRow = rowMovement

    maxSize = size-1 if (colMovement!=0 and colMovement!=size-1) or get_cell(board, rowMovement, colMovement)==3 else size-2
    while newRow<maxSize and is_free_cell(board, newRow+1, colMovement):
        if newRow+1 != throneCol or colMovement != throneCol or get_cell(board, rowMovement, colMovement) == 3:
            result += [(rowMovement, colMovement, newRow+1, colMovement)]
        newRow+=1
    return result

def get_right(movement, board, size, throneRow):
    rowMovement, colMovement = movement
    result = []
    newCol = colMovement
    
    maxSize = size-1 if (rowMovement!=0 and rowMovement!=size-1)or get_cell(board, rowMovement, colMovement)==3 else size-2
    while newCol<maxSize and is_free_cell(board, rowMovement, newCol+1):
        if rowMovement != throneRow or newCol+1 != throneRow or get_cell(board, rowMovement, colMovement) == 3:
            result += [(rowMovement, colMovement, rowMovement, newCol+1)]
        newCol+=1
    return result

def get_left(movement, board, size, throneRow):
    rowMovement, colMovement = movement
    result = []
    newCol = colMovement
    
    minSize = 0 if (rowMovement!=0 and rowMovement!=size-1) or get_cell(board, rowMovement, colMovement)==3 else 1
    while newCol>minSize and is_free_cell(board, rowMovement, newCol-1):
        if rowMovement != throneRow or newCol-1 != throneRow or get_cell(board, rowMovement, colMovement) == 3:
            result += [(rowMovement, colMovement, rowMovement, newCol-1)]
        newCol-=1
    return result