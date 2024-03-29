import copy

main_board = [["-", "-", "-"],
["-", "-", "-"],
["-", "-", "-"]]

def display_board(board):
    print()
    for row in board:
        for col in row:
            print(col, end = " ")
        print()

def select(board, row, col, player):
    if board[row][col] == "-":
        board[row][col] = player
    else:
        raise Exception("square is occupied")
    return board

def check_win(board, player):
    ## Horizontal
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
    
    ## Vertical
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True
    
    ## Diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    elif board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    ## No win
    return False

def check_draw(board):
    draw = True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "-":
                draw = False
    if draw == True:
        return True
    else:
        return False

def possible_moves(board):
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "-":
                moves.append((row, col))
    return moves

def minimax(board, player_symbol, ai_symbol, depth, isMaximising):
    ## Check if result is a draw
    if check_draw(board) == True:
        return 0
    ## Check if result is loss for AI
    elif check_win(board, player_symbol) == True:
        return -1
        print("L")
    ## Check if result is win for AI
    elif check_win(board, ai_symbol) == True:
        return 1

    if isMaximising:
        ## AI picks optimal move by maximising AI's score
        best_value = -2
        moves = possible_moves(board)
        for move in moves:
            row, col = move
            new_board = copy.deepcopy(board)
            new_board[row][col] = ai_symbol
            value = minimax(new_board, player_symbol, ai_symbol, depth + 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        ## Player picks optimal move by minimising AI's score
        best_value = 2
        moves = possible_moves(board)
        for move in moves:
            row, col = move
            new_board = copy.deepcopy(board)
            new_board[row][col] = player_symbol
            value = minimax(new_board, player_symbol, ai_symbol, depth + 1, True)
            best_value = min(best_value, value)
        return best_value

def find_best_move(board, player_symbol, ai_symbol):
    moves = possible_moves(board)
    best_value = -2
    for move in moves:
        row, col = move
        new_board = copy.deepcopy(board)
        new_board[row][col] = ai_symbol
        value = minimax(new_board, player_symbol, ai_symbol, 1, False)
#        print(move, value)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move

complete = False

display_board(main_board)

player_symbol = "X"
ai_symbol = "O"

while complete == False:

    ## Player 1 turn
    valid = False
    while valid == False:
        try:
            print("\nPLAYER:")
            selection = input("Enter coords of square (row,col): ")
            row, col = selection.strip("()").split(",")
#            print(row, col)
            row = int(row)
            col = int(col)
            current_state = copy.deepcopy(main_board)
            main_board = select(current_state, row, col, player_symbol)
            valid = True
        except:
            print("Choose a different square")
    
    display_board(main_board)

    ## Check if game is over
    if check_draw(main_board) == True:
        print("GAME OVER: A DRAW")
        complete = True
    elif check_win(main_board, player_symbol) == True:
        print("GAME OVER: YOU WIN")
        complete = True

    ## AI turn
    if complete == False:
        current_state = copy.deepcopy(main_board)
        ai_move = find_best_move(current_state, player_symbol, ai_symbol)
        row, col = ai_move
        print("\nAI move: ({},{})".format(row, col))

        main_board = select(main_board, row, col, ai_symbol)

        display_board(main_board)

        ## Check if game is over
        if check_draw(main_board) == True:
            print("GAME OVER: A DRAW")
            complete = True
        elif check_win(main_board, ai_symbol) == True:
            print("GAME OVER: AI WINS")
            complete = True
    