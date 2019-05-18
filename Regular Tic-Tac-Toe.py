from tkinter import *
import tkinter.messagebox
import copy
from operator import itemgetter

click = True
tk = None

#-------------------------------------------------------------------------------THIS IS 3X3--------------------------------------------------------------------------------------

def start():
    global tk
    tk = Tk()


    def play(index):
        global click, tk
        if buttons[index]["text"] == " " and click:
            buttons[index]["text"] = "X"
            click = False
        elif buttons[index]["text"] == " ":
            buttons[index]['text'] = "O"
            click = True
        #Conditions for win!
        if (buttons[0]["text"] == "X" and buttons[1]["text"] == "X" and buttons[2]["text"] == "X" or
            buttons[3]["text"] == "X" and buttons[4]["text"] == "X" and buttons[5]["text"] == "X" or
            buttons[6]["text"] == "X" and buttons[7]["text"] == "X" and buttons[8]["text"] == "X" or
            buttons[0]["text"] == "X" and buttons[3]["text"] == "X" and buttons[6]["text"] == "X" or
            buttons[1]["text"] == "X" and buttons[4]["text"] == "X" and buttons[7]["text"] == "X" or
            buttons[2]["text"] == "X" and buttons[5]["text"] == "X" and buttons[8]["text"] == "X" or
            buttons[0]["text"] == "X" and buttons[4]["text"] == "X" and buttons[8]["text"] == "X" or
            buttons[2]["text"] == "X" and buttons[4]["text"] == "X" and buttons[6]["text"] == "X"):
            answer = tkinter.messagebox.askquestion('ATTENTION', 'X Player has won!!! \n Do you want to play again?')
            tk.destroy()
            if answer == 'yes': start()
        
        elif (buttons[0]["text"] == "O" and buttons[1]["text"] == "O" and buttons[2]["text"] == "O" or
            buttons[3]["text"] == "O" and buttons[4]["text"] == "O" and buttons[5]["text"] == "O" or
            buttons[6]["text"] == "O" and buttons[7]["text"] == "O" and buttons[8]["text"] == "O" or
            buttons[0]["text"] == "O" and buttons[3]["text"] == "O" and buttons[6]["text"] == "O" or
            buttons[1]["text"] == "O" and buttons[4]["text"] == "O" and buttons[7]["text"] == "O" or
            buttons[2]["text"] == "O" and buttons[5]["text"] == "O" and buttons[8]["text"] == "O" or
            buttons[0]["text"] == "O" and buttons[4]["text"] == "O" and buttons[8]["text"] == "O" or
            buttons[2]["text"] == "O" and buttons[4]["text"] == "O" and buttons[6]["text"] == "O"):
            answer = tkinter.messagebox.askquestion("ATTENTION", " O Player wins!!! \n Do you want to play again?")
            tk.destroy()
            if answer == 'yes': start()
        #Conditions for Draw
        elif (buttons[0]["text"] != " " and buttons[1]["text"] != " " and buttons[2]["text"] != " " and buttons[3]["text"] != " "
            and buttons[4]["text"] != " " and buttons[4]["text"] != " " and buttons[6]["text"] != " " and buttons[7]["text"] != " "
            and buttons[8]["text"] != " "):
            answer = tkinter.messagebox.askquestion("ATTENTION", " You have drawn!!! \n Do you want to play again?")
            tk.destroy()
            if answer == "yes" : start()

    buttons = []

    #These are the buttons
    for j in range(0,3):
        for k in range(0,3):   
            button = Button(tk, text=" ", font=('Times 26 bold'), height=4, width=4, command = lambda x = 3*j+k : play(x))
            button.grid(row=j, column=k, sticky=S+N+E+W)
            buttons.append(button)


    tk.mainloop()

#---------------------------------------------------------------------------THIS IS 3X3 GUI-----------------------------------------------------------------------------------------
def comp():
    class TicTacToe:
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        buttons = []

        def __init__(self):
            self.board = [" "] * 9
            # List comprehension is needed so that each StringVar will not point to the same object
            self.moves = [StringVar() for _ in range(9)]
            self.x_wins = 0
            self.o_wins = 0
            self.curr_player = "X"
            self.move_number = 0
            self.winning_squares = []


        # Call this to make a move
        def make_move(self, move):
            self.move_number += 1
            if self.curr_player == "X":
                self.board[move] = "X"
                self.curr_player = "O"
                # Tells the AI to take its turn
                if self.move_number < 9:
                    self.ai_mm_init()
            else:
                self.board[move] = "O"
                self.curr_player = "X"


            # Check for a win
            winner = self.game_won(self.board)
            if winner is not None:
                self.scoreboard(winner)
                self.game_over = True
            self.update_board()


        # Just like the function any, but returns the element instead of True
        def any_return(self, iterable):
            for e in iterable:
                if e:
                    return e
            return False

        # Check who won the game, and change the GUI state accordingly
        def scoreboard(self, winner):
            if winner == "X":
                self.x_wins += 0.5
            else:
                self.o_wins += 0.5
            count_text.set("X: " + str(self.x_wins) + "\tO: " + str(self.o_wins))
            for b in self.buttons:
                b.config(state="disabled")

        # Reset the game to its base state
        def reset(self):
            self.curr_player = "X"
            self.move_number = 0
            self.game_over = False
            self.board = [" " for _ in self.board]
            self.update_board()

            for b in self.buttons:
                b.config(state="normal")
                b.config(disabledforeground="black")

        # Update the GUI to reflect the moves in the board attribute
        def update_board(self):
            for i in range(9):
                self.moves[i].set(self.board[i])

        # Check each of the winning combinations to check if anyone has won
        def game_won(self, gameboard):
            # Check if any of the winning combinations have been used
            check = self.any_return([self.three_in_a_row(gameboard, c) for c in TicTacToe.winning_combinations])
            if check:
                return check
            else:
                return None

        # Check if the three given squares are owned by the same player
        def three_in_a_row(self, gameboard, squares):
            # Get the given squares from the board are check if they are all equal
            combo = set(itemgetter(squares[0], squares[1], squares[2])(gameboard))
            if len(combo) == 1 and combo.pop() != " ":
                self.winning_squares = squares
                return gameboard[squares[0]]
            else:
                return None

        # Get the opposite player
        def get_enemy(self, curr_player):
            if curr_player == "X":
                return "O"
            else:
                return "X"

        # Returns true if the board is full
        def board_full(self, board):
            for s in board:
                if s == " ":
                    return False

            return True

        # Call this to start the minimax algorithm
        def ai_mm_init(self):
            player = "O"
            a = -1000
            b = 1000

            board_copy = copy.deepcopy(self.board)

            best_outcome = -100

            best_move = None

            for i in range(9):
                if board_copy[i] == " ":
                    board_copy[i] = player
                    val = self.minimax(self.get_enemy(player), board_copy, a, b)
                    board_copy[i] = " "
                    if player == "O":
                        if val > best_outcome:
                            best_outcome = val
                            best_move = i
                    else:
                        if val < best_outcome:
                            best_outcome = val
                            best_move = i

            self.make_move(best_move)

        # The minimax algorithm, with alpha-beta pruning
        def minimax(self, player, board, alpha, beta):
            board_copy = copy.deepcopy(board)

            # Check for a win
            winner = self.game_won(board_copy)

            if winner == "O":
                return 1
            elif winner == "X":
                return -1
            elif self.board_full(board_copy):
                return 0

            best_outcome = -100 if player == "O" else 100

            for i in range(9):
                if board_copy[i] == " ":
                    board_copy[i] = player
                    val = self.minimax(self.get_enemy(player), board_copy, alpha, beta)
                    board_copy[i] = " "
                    if player == "O":
                        best_outcome = max(best_outcome, val)
                        alpha = min(alpha, best_outcome)
                    else:
                        best_outcome = min(best_outcome, val)
                        beta = max(beta, best_outcome)

                    if beta <= alpha:
                        return best_outcome

            return best_outcome


    root = Tk()
    root.title("Tic-Tac-Toe Game")
    game = TicTacToe()


    # Start Label
    start = StringVar()
    start.set("Tic-Tac-Toe Game!")
    welcome = Label(root, textvariable=start)
    welcome.grid(row=0, column=0, columnspan=3)

    # Label used to display the scoreboard
    count_text = StringVar()
    count_text.set("X: " + str(game.x_wins) + "\tO: " + str(game.o_wins))
    count = Label(root, textvariable=count_text)
    count.grid(row=1, column=0, columnspan=3)


    # Create buttons
    for square in range(9):
        temp_button = Button(root, textvariable=game.moves[square], command=lambda s=square: game.make_move(s))
        # Divide by 3 to get row number, modulus by 3 to get column number
        temp_button.grid(row=int((square / 3)) + 3, column=(square % 3), sticky=NSEW)
        game.buttons.append(temp_button)

    # Button for resetting the game
    restart_button_text = StringVar()
    restart_button_text.set("Restart")
    restart_button = Button(root, textvariable=restart_button_text, command=game.reset)
    restart_button.grid(row=1, column=0)

    # Set the size of the rows and columns
    root.columnconfigure(0, minsize=100)
    root.columnconfigure(1, minsize=100)
    root.columnconfigure(2, minsize=100)
    root.rowconfigure(3, minsize=100)
    root.rowconfigure(4, minsize=100)
    root.rowconfigure(5, minsize=100)

    # Start the GUI loop
    root.mainloop()





    

#---------------------------------------------------------------------------THIS IS 4X4-----------------------------------------------------------------------------------------
def start2():
    global tk
    tk = Tk()

    def play(index):
        global click, tk
        if buttons[index]["text"] == " " and click:
            buttons[index]["text"] = "X"
            click = False
        elif buttons[index]["text"] == " ":
            buttons[index]['text'] = "O"
            click = True

        #conditions for Win
        if (buttons[0]["text"] == "X" and buttons[1]["text"] == "X" and buttons[2]["text"] == "X" and buttons[3]["text"] == "X" or
            buttons[4]["text"] == "X" and buttons[5]["text"] == "X" and buttons[6]["text"] == "X" and buttons[7]["text"] == "X" or
            buttons[8]["text"] == "X" and buttons[9]["text"] == "X" and buttons[10]["text"] == "X" and buttons[11]["text"] == "X" or
            buttons[12]["text"] == "X" and buttons[13]["text"] == "X" and buttons[14]["text"] == "X" and buttons[15]["text"] == "X" or
            buttons[0]["text"] == "X" and buttons[4]["text"] == "X" and buttons[8]["text"] == "X" and buttons[12]["text"] == "X" or
            buttons[1]["text"] == "X" and buttons[5]["text"] == "X" and buttons[9]["text"] == "X" and buttons[13]["text"] == "X" or
            buttons[2]["text"] == "X" and buttons[6]["text"] == "X" and buttons[10]["text"] == "X" and buttons[14]["text"] == "X" or
            buttons[3]["text"] == "X" and buttons[7]["text"] == "X" and buttons[11]["text"] == "X" and buttons[15]["text"] == "X" or
            buttons[0]["text"] == "X" and buttons[5]["text"] == "X" and buttons[10]["text"] == "X" and buttons[15]["text"] == "X"or
            buttons[3]["text"] == "X" and buttons[6]["text"] == "X" and buttons[9]["text"] == "X" and buttons[12]["text"] == "X"):
            answer = tkinter.messagebox.askquestion("ATTENTION", " X Player wins!!! \n Do you want to play again?")
            tk.destroy()
            if answer == 'yes': start2()


        if (buttons[0]["text"] == "O" and buttons[1]["text"] == "O" and buttons[2]["text"] == "O" and buttons[3]["text"] == "O" or
            buttons[4]["text"] == "O" and buttons[5]["text"] == "O" and buttons[6]["text"] == "O" and buttons[7]["text"] == "O" or
            buttons[8]["text"] == "O" and buttons[9]["text"] == "O" and buttons[10]["text"] == "O" and buttons[11]["text"] == "O" or
            buttons[12]["text"] == "O" and buttons[13]["text"] == "O" and buttons[14]["text"] == "O" and buttons[15]["text"] == "O" or
            buttons[0]["text"] == "O" and buttons[4]["text"] == "O" and buttons[8]["text"] == "O" and buttons[12]["text"] == "O" or
            buttons[1]["text"] == "O" and buttons[5]["text"] == "O" and buttons[9]["text"] == "O" and buttons[13]["text"] == "O" or
            buttons[2]["text"] == "O" and buttons[6]["text"] == "O" and buttons[10]["text"] == "O" and buttons[14]["text"] == "O" or
            buttons[3]["text"] == "O" and buttons[7]["text"] == "O" and buttons[11]["text"] == "O" and buttons[15]["text"] == "O" or
            buttons[0]["text"] == "O" and buttons[5]["text"] == "O" and buttons[10]["text"] == "O" and buttons[15]["text"] == "O"or
            buttons[3]["text"] == "O" and buttons[6]["text"] == "O" and buttons[9]["text"] == "O" and buttons[12]["text"] == "O"):
            answer = tkinter.messagebox.askquestion("ATTENTION", " O Player wins!!! \n Do you want to play again?")
            tk.destroy()
            if answer == 'yes': start2()

        #conditions for Draw
        elif (buttons[0]["text"] != " " and buttons[1]["text"] != " " and buttons[2]["text"] != " " and buttons[3]["text"] != " "
            and buttons[4]["text"] != " " and buttons[4]["text"] != " " and buttons[6]["text"] != " " and buttons[7]["text"] != " "
            and buttons[8]["text"] != " " and buttons[9]["text"] != " " and buttons[10]["text"] != " " and buttons[11]["text"] != " "
            and buttons[12]["text"] != " " and buttons[13]["text"] != " " and buttons[14]["text"] != " " and buttons[15]["text"] != " " ):
            answer = tkinter.messagebox.askquestion("ATTENTION", " You have drawn!! \n Do you want to play again?")
            tk.destroy()
            if answer == "yes" : start2()

    buttons = []
    #These are the buttons
    for j in range(0,4):
        for k in range(0,4):   
            button = Button(tk, text=" ", font=('Times 26 bold'), height=4, width=4, command = lambda x = 4*j+k : play(x))
            button.grid(row=j, column=k, sticky=S+N+E+W)
            buttons.append(button)
    tk.mainloop()


#These are the options for 2 player
def player2():
    window2.destroy()
    window = tkinter.Tk()
    window.configure(background="Black")
    window.title("DSA")
    photo = tkinter.PhotoImage(file="image.gif")
    b = Button(window, text=" 3 X 3 ", command= start, font = ( "Helvetica", 35))
    b.config( height = 2 , width = 10)
    b.pack()

    c = Button(window, text=" 4 X 4 ", command=start2, font = ( "Helvetica", 35))
    c.config( height = 2
              , width = 10)
    c.pack()


#This is the startup window giving user options of Computer and 2 Player.
window2 = tkinter.Tk()
window2.configure(background="Black")
window2.title("DSA")
#window.wm_iconbitmap('Icon.ico')

photo = tkinter.PhotoImage(file="image.gif")
y = tkinter.Label(window2,image=photo)
y.pack()
b = Button(window2, text=" Computer ", command=comp, font = ( "Helvetica", 35))
b.config( height = 2 , width = 10)
b.pack()

c = Button(window2, text=" 2 Player", command=player2, font = ( "Helvetica", 35))
c.config( height = 2, width = 10)
c.pack()


