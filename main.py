board = [["-", "-", "-"],
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

complete = False

display_board(board)

player1 = "X"
player2 = "O"

while complete == False:

    ## Player 1 turn
    valid = False
    while valid == False:
        try:
            print("\nPLAYER 1:")
            selection = input("Enter coords of square (row,col): ")
            row, col = selection.strip("()").split(",")
            print(row, col)
            row = int(row)
            col = int(col)
            select(board, row, col, player1)
            valid = True
        except:
            print("Choose a different square")
    
    display_board(board)

    ## Check if game is over
    if check_draw(board) == True:
        print("GAME OVER: A DRAW")
        complete = True
    elif check_win(board, player1) == True:
        print("GAME OVER: PLAYER 1 WINS")
        complete = True

    ## Player 2 turn
    if complete == False:
        valid = False
        while valid == False:
            try:
                print("\nPLAYER 2:")
                selection = input("Enter coords of square (row,col): ")
                row, col = selection.strip("()").split(",")
                print(row, col)
                row = int(row)
                col = int(col)
                select(board, row, col, player2)
                valid = True
            except:
                print("Choose a different square")

        display_board(board)

        ## Check if game is over
        if check_draw(board) == True:
            print("GAME OVER: A DRAW")
            complete = True
        elif check_win(board, player2) == True:
            print("GAME OVER: PLAYER 2 WINS")
            complete = True
    