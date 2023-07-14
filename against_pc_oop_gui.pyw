from tkinter import *
import os


'''
BOARD STRUCTURE (list representation)
[
[ 1, 2, 3 ],
[ 4, 5, 6 ],
[ 7, 8, 9 ]
]
Each inner list represents a row
'''


class CharPrompt(Toplevel):

    ''' Toplevel prompting the user to pick X or O to play with '''

    TITLE = ""
    TEXT = "Choose X or O"
    BUTTON_SIZE = 70
    LBL_FONT = ("Calibri", 16)
    BTN_FONT = ("Calibri", 30)
    RESIZABLE = False
    
    def __init__(self, master : Misc):
        super().__init__(master)
        self.title(CharPrompt.TITLE)
        self.resizable(width = CharPrompt.RESIZABLE, height = CharPrompt.RESIZABLE)
        self.label = Label(self, text = CharPrompt.TEXT, font = CharPrompt.LBL_FONT)
        self.label.grid(row = 0, columnspan = 2, sticky = EW)
        # X Button
        self.xframe = Frame(self, height = CharPrompt.BUTTON_SIZE, width = CharPrompt.BUTTON_SIZE)
        self.xframe.grid_propagate(0)
        self.xframe.grid_rowconfigure(0, weight = 1)
        self.xframe.grid_columnconfigure(0, weight = 1)
        self.xbtn = Button(
            self.xframe, text = App.X, font = CharPrompt.BTN_FONT, command = self.chooseX)
        self.xframe.grid(row = 1, column = 0)
        self.xbtn.grid(sticky = NSEW)
        # O Button
        self.oframe = Frame(self, height = CharPrompt.BUTTON_SIZE, width = CharPrompt.BUTTON_SIZE)
        self.oframe.grid_propagate(0)
        self.oframe.grid_rowconfigure(0, weight = 1)
        self.oframe.grid_columnconfigure(0, weight = 1)
        self.obtn = Button(
            self.oframe, text = App.O, font = CharPrompt.BTN_FONT, command = self.chooseO)
        self.oframe.grid(row = 1, column = 1)
        self.obtn.grid(sticky = NSEW)
        # To store the selected character (stays "" if user closes window without choosing)
        self.selected = ""
    
    def chooseX(self):
        self.selected = App.X
        self.destroy()

    def chooseO(self):
        self.selected = App.O
        self.destroy()

    def get_result(self) -> str:
        return self.selected


class EndPrompt(Toplevel):

    ''' Toplevel showing the result of the game, with options to quit or restart '''

    TITLE = "Game over"
    WIN = "You won!"
    LOSS = "You lost!"
    DRAW = "A draw!"
    RESTART = "Restart"
    QUIT = "Quit"
    BTN_FONT = ("Calibri", 16)
    BTN_WIDTH = 8
    LBL_FONT = ("Calibri", 16)
    RESIZABLE = False

    def __init__(self, master : Misc, result : str):
        super().__init__(master)
        self.title(EndPrompt.TITLE)
        self.resizable(width = EndPrompt.RESIZABLE, height = EndPrompt.RESIZABLE)
        # Label
        self.label = Label(self, text = result, font = EndPrompt.LBL_FONT)
        self.label.grid(row = 0, columnspan = 2, sticky = NSEW)
        # Restart button
        self.restart_btn = Button(
            self, text = EndPrompt.RESTART, width = EndPrompt.BTN_WIDTH, 
            font = EndPrompt.BTN_FONT, command = self.choose_restart)
        self.restart_btn.grid(row = 1, column = 0, sticky = NSEW)
        # Quit button
        self.quit_btn = Button(
            self, text = EndPrompt.QUIT, width = EndPrompt.BTN_WIDTH, 
            font = EndPrompt.BTN_FONT, command = self.choose_quit)
        self.quit_btn.grid(row = 1, column = 1, sticky = NSEW)
        # User wants to restart?
        self.restart = False

    def choose_quit(self):
        self.destroy()
    
    def choose_restart(self):
        self.restart = True
        self.destroy()

    def get_result(self) -> str:
        return self.restart


class Tile(Frame):

    ''' Button, with parent frame to set size in pixels '''

    FONT = ("Calibri", 30)
    SIZE = 90
    BUTTON_RELIEF = SUNKEN
        
    def __init__(self, master : Misc, row : int, col : int):
        # Both the height and width (as it is square)
        super().__init__(master, height = Tile.SIZE, width = Tile.SIZE)
        self.button = Button(self, text = App.PLACEHOLDER, font = Tile.FONT, relief = Tile.BUTTON_RELIEF, command = self.on_press)
        self.isTaken = False
        # Position in the grid (where top-left is 0, 0)
        self.row = row
        self.col = col
        self.grid_propagate(0)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.button.grid(sticky = NSEW)

    def on_press(self):
        ''' Handle click event '''
        self.master.player_move(self.row, self.col)
        
    def set_char(self, char : str):
        ''' Occupy the tile with the given character '''
        self.char = char
        self.button.config(text = self.char)
        self.isTaken = True
        
    def disable(self):
        ''' Prevent tile from being selected by user '''
        self.button.config(state = "disabled")

    def enable(self):
        ''' Allow user to select tile '''
        self.button.config(state = "active")

    def is_taken(self) -> bool:
        ''' Check if tile is occupied '''
        return self.isTaken


class App(Tk):

    ''' Main application window '''

    RESIZABLE = False
    TITLE = "Tic-Tac-Toe"
    X = "X"
    O = "O"
    PLACEHOLDER = ""
    BOARD_SIZE = 3
    DRAW_STATE = "DRAW"

    def __init__(self):
        super().__init__()
        self.title(App.TITLE)
        self.resizable(width = App.RESIZABLE, height = App.RESIZABLE)
        # Key bindings to close window
        self.bind_all("<Control-w>", self.on_close)
        self.bind_all("<Control-q>", self.on_close)
        self.bind_all("<Control-W>", self.on_close)
        self.bind_all("<Control-Q>", self.on_close)
        # Initialise board and get player to choose X or O
        self.new_game()
        
    def init_board(self):
        ''' Set the initial empty board state and create tiles '''
        self.board = [[] for i in range(App.BOARD_SIZE)]
        self.tiles = [[] for i in range(App.BOARD_SIZE)]
        for row in range(App.BOARD_SIZE):
            for col in range(App.BOARD_SIZE):
                tile = Tile(self, row, col)
                tile.grid(row = row, column = col)
                self.tiles[row].append(tile)
                self.board[row].append(App.PLACEHOLDER)

    def player_move(self, row : int, col : int):
        ''' Update the screen and board when user clicks on a tile '''
        tile = self.tiles[row][col]
        tile.set_char(self.player_char)
        self.make_move(row, col, self.player_char)
        self.disable_tiles()
        self.update()
        # Check whether end state reached
        result = self.check_board_state()
        if result == None:
            # Prompt AI to move if game is not over
            self.ai_move()
        else:
            self.endgame_prompt(result)

    def ai_move(self):
        ''' Find the best move via minimax then play it '''
        r, c = self.minimax()
        tile = self.tiles[r][c]
        tile.set_char(self.ai_char)
        self.make_move(r, c, self.ai_char)
        self.enable_tiles()
        # Check whether end state reached
        result = self.check_board_state()
        if result != None:
            self.endgame_prompt(result)

    def minimax(self, maximising : bool = True, depth : int = 1):
        ''' Find the optimal move for AI by recursion and evaluating end states '''
        # First check for end state
        result = self.check_board_state()
        if result == self.player_char:
            return -1
        elif result == self.ai_char:
            return 1
        elif result == App.DRAW_STATE:
            return 0
        
        # Get possible moves and play each one
        moves = self.get_moves()
        if maximising:
            # AI turn (wants the best score for the AI)
            best_score = -2
            for move in moves:
                r, c = move
                self.make_move(r, c, self.ai_char)
                score = self.minimax(maximising = (not maximising), depth = (depth + 1))
                self.undo_move(r, c)
                if score > best_score:
                    best_score = score
                    best_move = move
                # Can't be better
                if score == 1:
                    break
            # If this is the original minimax call, ready to make the optimal move
            if depth == 1:
                # if best_score == 0:
                #     os.system("cls")
                #     print("should be a draw")
                # if best_score == 1:
                #     os.system("cls")
                #     print("you will lose")
                # if best_score == -1:
                #     os.system("cls")
                #     print("you should win")
                return best_move
            return best_score
        else:
            # Player turn (wants the worst score for the AI)
            worst_score = 2
            for move in moves:
                r, c = move
                self.make_move(r, c, self.player_char)
                score = self.minimax(maximising = (not maximising), depth = (depth + 1))
                self.undo_move(r, c)
                if score < worst_score:
                    worst_score = score
                    worst_move = move
                # Can't be worse
                if score == -1:
                    break
            return worst_score

    def make_move(self, row : int, col : int, char : str):
        ''' Update board with a move '''
        self.board[row][col] = char

    def undo_move(self, row : int, col : int):
        ''' For use in minimax function '''
        self.board[row][col] = App.PLACEHOLDER

    def get_moves(self) -> list:
        ''' Returns list of tuples (row, col) '''
        moves = []
        for r in range(App.BOARD_SIZE):
            for c in range(App.BOARD_SIZE):
                char = self.board[r][c]
                if char == App.PLACEHOLDER:
                    moves.append((r, c))
        return moves

    def check_board_state(self) -> str:
        ''' Check if board state is a win for player, win for AI, or a draw '''

        # Check rows
        for row in self.board:
            result = self.check_list(row)
            if result in (App.X, App.O):
                return result
        
        # Check columns
        for c in range(App.BOARD_SIZE):
            col = []
            for row in self.board:
                col.append(row[c])
            result = self.check_list(col)
            if result in (App.X, App.O):
                return result

        # Check diagonals
        diag1 = []
        diag2 = []
        for i in range(App.BOARD_SIZE):
            # Top-left to bottom-right
            diag1.append(self.board[i][i])
            # Top-right to bottom-left
            diag2.append(self.board[i][2-i])
        results = (self.check_list(diag1), self.check_list(diag2))
        # Check if either of the diagonals is full
        for result in results:
            if result in (App.X, App.O):
                return result

        # Check if board state is a draw (board will be full, and no win detected)
        filled = True
        for row in self.board:
            for x in row:
                if x == App.PLACEHOLDER:
                    filled = False
        if filled:
            return App.DRAW_STATE

    def check_list(self, l : list) -> str:
        ''' Check for 3 in a row in the given list '''
        player_win = all(x == self.player_char for x in l)
        ai_win = all(x == self.ai_char for x in l)
        if player_win:
            return self.player_char
        elif ai_win:
            return self.ai_char
        else:
            return ""

    def disable_tiles(self):
        ''' Set all tile buttons to disabled state (while waiting for AI move) '''
        for row in range(App.BOARD_SIZE):
            for col in range(App.BOARD_SIZE):
                self.tiles[row][col].disable()

    def enable_tiles(self):
        ''' Set all unoccupied tiles to enabled state '''
        for row in range(App.BOARD_SIZE):
            for col in range(App.BOARD_SIZE):
                tile = self.tiles[row][col]
                if not tile.is_taken():
                    tile.enable()

    def new_game(self):
        ''' Initialise board and choose player char to start a new game '''
        #os.system("cls")
        # Initialise board
        self.init_board()
        # Determine whether to play with X or O
        self.prompt_player_char()

    def prompt_player_char(self):
        ''' Create a toplevel prompt and for user to choose X or O '''
        # Hide window and wait for player to choose X or O before redrawing
        self.withdraw()
        prompt = CharPrompt(self)
        prompt.wait_window()
        result = prompt.get_result()
        # If prompt was closed by user, result will not hold X or O
        if result not in (App.X, App.O):
            self.on_close()
        self.player_char = result
        self.ai_char = App.X if self.player_char == App.O else App.O
        self.wm_deiconify()

    def endgame_prompt(self, result : str):
        ''' Create toplevel prompt and wait for user input '''
        if result == App.DRAW_STATE:
            result = EndPrompt.DRAW
        elif result == self.player_char:
            result = EndPrompt.WIN
        else:
            result = EndPrompt.LOSS
        prompt = EndPrompt(self, result = result)
        prompt.wait_window()
        # Does player want to restart?
        restart = prompt.get_result()
        if restart == True:
            self.new_game()
        else:
            self.on_close()

    def on_close(self, event = None):
        ''' Exit application '''
        self.destroy()
        exit()




if __name__ == "__main__":
    app = App()
    app.mainloop()

