def get(current_state, movement, max_movements):

    next_turn = get_next_turn(current_state[1])
    next_board, removed_tokens = get_next_board(current_state[0], current_state[1], movement)

    return (next_board, next_turn, max_movements-1, removed_tokens)

#------------------------- Funciones auxiliares ----------------------------

def get_next_board(current_board, current_turn, movement):

    new_board = do_movement(current_board, movement)
    
    removed_tokens = remove_captured_tokens(new_board, current_turn, movement)

    return (new_board, removed_tokens)

def do_movement(current_board, movement):
    
    result = recursive_copy(current_board)

    result[movement[2]][movement[3]] = result[movement[0]][movement[1]]
    result[movement[0]][movement[1]] = 0
    
    return result

def remove_captured_tokens(board, turn, movement):

    newCell_x = movement[3]
    newCell_y = movement[2]

    if turn == 1:
        enemies = (2, 3)
        alies = (1, None)
    else:
        enemies = (1, None)
        alies = (2,3)

    return do_remove(board, alies, enemies, newCell_x, newCell_y)

def do_remove(board, alies, enemies, newCell_x, newCell_y):

    board_length = len(board)-1
    half_board = board_length/2
    result = 0

    if newCell_y > 0 and newCell_y - 1 > 0:
        if check_top(board, alies, enemies, newCell_x, newCell_y, half_board):

            if board[newCell_y - 1][newCell_x] == 3:
                if king_capture(board, newCell_x, newCell_y - 1):

                    board[newCell_y - 1][newCell_x] = 0
                    result += 1

            else:

                board[newCell_y - 1][newCell_x] = 0
                result += 1

    if newCell_y < board_length and newCell_y + 1 < board_length:
        if check_bottom(board, alies, enemies, newCell_x, newCell_y, half_board):

            if board[newCell_y + 1][newCell_x] == 3:
                if king_capture(board, newCell_x, newCell_y + 1):

                    board[newCell_y + 1][newCell_x] = 0
                    result += 1

            else:

                board[newCell_y + 1][newCell_x] = 0
                result += 1
        

    if newCell_x < board_length and newCell_x + 1 < board_length:
        if check_right(board, alies, enemies, newCell_x, newCell_y, half_board):

            if board[newCell_y][newCell_x + 1] == 3:
                if king_capture(board, newCell_x + 1, newCell_y):

                    board[newCell_y][newCell_x + 1] = 0
                    result += 1

            else:

                board[newCell_y][newCell_x + 1] = 0
                result += 1

    if newCell_x > 0 and newCell_x - 1 > 0:
        if check_left(board, alies, enemies, newCell_x, newCell_y, half_board):

            if board[newCell_y][newCell_x - 1] == 3:
                if king_capture(board, newCell_x - 1, newCell_y):

                    board[newCell_y][newCell_x - 1] = 0
                    result += 1

            else:

                board[newCell_y][newCell_x - 1] = 0
                result += 1
    
    return result
        

def check_top(board, alies, enemies, newCell_x, newCell_y, half_board):

    return (board[newCell_y - 1][newCell_x] in enemies 
            and (board[newCell_y - 2][newCell_x] in alies or is_exit(newCell_x, newCell_y - 2, board) or is_throne_without_king(newCell_x, newCell_y - 2, half_board, board)))

def check_right(board, alies, enemies, newCell_x, newCell_y, half_board):

    return (board[newCell_y][newCell_x + 1] in enemies 
            and (board[newCell_y][newCell_x + 2] in alies or is_exit(newCell_x + 2, newCell_y, board) or is_throne_without_king(newCell_x + 2, newCell_y, half_board, board)))

def check_left(board, alies, enemies, newCell_x, newCell_y, half_board):
    
    return (board[newCell_y][newCell_x - 1] in enemies 
            and (board[newCell_y][newCell_x - 2] in alies or is_exit(newCell_x - 2, newCell_y, board) or is_throne_without_king(newCell_x - 2, newCell_y, half_board, board)))

def check_bottom(board, alies, enemies, newCell_x, newCell_y, half_board):

    return (board[newCell_y + 1][newCell_x] in enemies 
            and (board[newCell_y + 2][newCell_x] in alies or is_exit(newCell_x, newCell_y + 2, board) or is_throne_without_king(newCell_x, newCell_y + 2, half_board, board)))

def king_capture(board, king_x, king_y):

    half_board = (len(board)-1)/2

    if on_throne_or_surroundings(king_x, king_y, half_board):

        return ((board[king_y][king_x + 1] == 1 or is_throne(king_x + 1, king_y, half_board)) 
                and (board[king_y][king_x - 1] == 1 or is_throne(king_x - 1, king_y, half_board)) 
                and (board[king_y - 1][king_x] == 1 or is_throne(king_x, king_y - 1, half_board)) 
                and (board[king_y + 1][king_x] == 1 or is_throne(king_x, king_y + 1, half_board)))

    else:
        
        return True


def on_throne_or_surroundings(newCell_x, newCell_y, half_board):
    
    return (is_throne(newCell_x, newCell_y, half_board) or (newCell_x == half_board and newCell_y in (half_board-1, half_board+1)) 
            or (newCell_x in (half_board-1, half_board+1) and newCell_y == half_board))

def is_throne(newCell_x, newCell_y, half_board):

    return newCell_x == half_board and newCell_y == half_board

def is_throne_without_king(newCell_x, newCell_y, half_board, board):
    return newCell_x == half_board and newCell_y == half_board and board[newCell_x][newCell_y] == 0

def is_exit(newCell_x, newCell_y, board):

    maxCoord = len(board)-1

    return ((newCell_x == 0 and newCell_y == 0) 
            or (newCell_x == 0 and newCell_y == maxCoord) 
            or (newCell_x == maxCoord and newCell_y == 0) 
            or (newCell_x == maxCoord and newCell_y == maxCoord))

def get_next_turn(current_turn):

    if current_turn == 1:
        return 2
    else:
        return 1

def recursive_copy(list):
    result = []

    for item in list:
        result.append(item.copy())

    return result