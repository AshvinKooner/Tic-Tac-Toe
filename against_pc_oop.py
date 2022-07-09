
class Game:

    def __init__(self):
        ## Allow user to choose whether to play as X or O, and then assign the other to the AI accordingly
        self.player_symbol = input("Choose 'X' or 'O': ").upper()
        while self.player_symbol != "X" and self.player_symbol != "O":
            print("Must enter either 'X' or 'O")
            self.player_symbol = input("Choose 'X' or 'O': ").upper()
        if self.player_symbol == "X":
            self.ai_symbol = "O"
        else:
            self.ai_symbol = "X"
        
        ## Generate empty playing board
        self.board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    
    def display_board(self):
        print()
        for i in range(len(self.board)):
            print(self.board[i], end = " ")
            ## Insert new line after every 3 squares (making up the 3 rows)
            if i == 2 or i == 5:
                print()
        print("\n")

    def move(self, selection, symbol):
        ## Check if chosen square is empty, if it is then place the symbol in that square
        if self.board[selection] == "-":   
            self.board[selection] = symbol
        else:
            raise Exception("Square is occupied")

    def undo(self, selection):
        self.board[selection] = "-"

    def get_possible_moves(self):
        ## Find which tiles are empty in current board state and return as a list
        moves = []
        for i in range(len(self.board)):
            if self.board[i] == "-":
                moves.append(i)
        return moves

    def check_result(self):
        ## Check if board is full - indicates a draw
        draw = True
        for i in range(len(self.board)):
            if self.board[i] == "-":
                draw = False
        if draw == True:
            return "draw"
        
        ## Check if player or AI has won
        for symbol in [self.player_symbol, self.ai_symbol]:
            ## Horizontal
            if self.board[0] == self.board[1] == self.board[2] == symbol:
                return symbol
            elif self.board[3] == self.board[4] == self.board[5] == symbol:
                return symbol  
            elif self.board[6] == self.board[7] == self.board[8] == symbol:
                return symbol 

            ## Vertical
            if self.board[0] == self.board[3] == self.board[6] == symbol:
                return symbol
            elif self.board[1] == self.board[4] == self.board[7] == symbol:
                return symbol  
            elif self.board[2] == self.board[5] == self.board[8] == symbol:
                return symbol
            
            ## Diagonal
            if self.board[0] == self.board[4] == self.board[8] == symbol:
                return symbol
            elif self.board[2] == self.board[4] == self.board[6] == symbol:
                return symbol

    def minimax(self, isMaximising, depth = 1):
        ## Check if terminal board state reached and evaluate
        #print("DEPTH", depth)
        #self.display_board()
        result = self.check_result()
        if result == "draw":
            return 0
        elif result == self.ai_symbol:
            return 1
        elif result == self.player_symbol:
            return -1

        if isMaximising:
            ## AI picks optimal move by maximising AI's score
            best_value = -2
            moves = self.get_possible_moves()
            for move in moves:
                self.move(move, self.ai_symbol)
                value = self.minimax(False, depth + 1)
                best_value = max(best_value, value)
                self.undo(move)
            return best_value
        else:
            ## Player picks optimal move by minimising AI's score
            best_value = 2
            moves = self.get_possible_moves()
            for move in moves:
                self.move(move, self.player_symbol)
                value = self.minimax(True, depth + 1)
                best_value = min(best_value, value)
                self.undo(move)
            return best_value

    def player_move(self):
        selection = input("Enter a number 1-9 to choose a square (1 = top left, 9 = bottom right): ")
        valid = False
        while valid == False:
            try:
                ## User enters number 1-9 as more intuitive - must be reduced by 1
                selection = int(selection) - 1
                #print(selection)
                if selection < 0:
                    raise Exception("Number entered was below 1")
                self.move(selection, self.player_symbol)
                valid = True
            except:
                print("Must enter a number between 1 and 9, and chosen square must be empty")
                selection = int(input("Enter a number 1-9 to choose a square (1 = top left, 9 = bottom right): "))
        self.display_board()
    
    def ai_move(self):
        moves = self.get_possible_moves()
        best_value = -2
        for move in moves:
            self.move(move, self.ai_symbol)
            value = self.minimax(False)
            self.undo(move)
    #        print(move, value)
            if value > best_value:
                best_value = value
                best_move = move
        self.move(best_move, self.ai_symbol)
        self.display_board()

game = Game()

## Flag to end the program when the game has reached terminal state
terminal = False

game.display_board()

while terminal == False:
    game.player_move()
    if game.check_result() == "draw":
        terminal = True
        print("GAME OVER: A DRAW")
    elif game.check_result() == game.player_symbol:
        terminal = True
        print("GAME OVER: YOU WIN")
    else:
        print("AI move:\n")
        game.ai_move()
        if game.check_result() == "draw":
            terminal = True
            print("GAME OVER: A DRAW")
        elif game.check_result() == game.ai_symbol:
            print("GAME OVER: YOU LOSE")

    

        