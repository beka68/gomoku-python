#!/usr/bin/python3 
from tkinter import *
from time import *
import sys
myInterface = Tk()
c = Canvas(myInterface, width=800, height=800, background= "#b69b4c")
c.pack()

#Board Size
Board_Size = 15
Frame_Gap = 35
width = 800
height = 800

#Board
Board_Size = Board_Size - 1
Board_X1 = width / 10
Board_Y1 = height / 10
Board_GapX = (width - Board_X1 * 2) / Board_Size
Board_GapY = (height - Board_Y1 * 2) / Board_Size

#game states
from enum import Enum
class GameState(Enum):
    EXIT = 0
    GAME = 1
    BLACK_WIN = 2
    WHITE_WIN = 3
    MENU = 4

#higher order function
def Radius_Func(x,y,z):
    def func(data):
        return data*(x/y)*1/z
    return func

radius = Radius_Func(9,10,2)
Chess_Radius=radius(Board_GapX)

#Turn
Turn_Num = 1
Turn = "black"
Stage = GameState.GAME

#Cord List
Black_Cord_PickedX = []
Black_Cord_PickedY = []
White_Cord_PickedX = []
White_Cord_PickedY = []

#Click Detection Cord - list comprehension
Game_CordX = [z for i in range(1, Board_Size + 2) for z in range(1, Board_Size + 2)]
Game_CordY = [i for i in range(1, Board_Size + 2) for _ in range(1, Board_Size + 2)]
XStart = [(z - 1) * Board_GapX + Board_X1 - Chess_Radius for _ in range(1, Board_Size + 2) for z in range(1, Board_Size + 2)]
YStart = [(i - 1) * Board_GapY + Board_Y1 - Chess_Radius for i in range(1, Board_Size + 2) for _ in range(1, Board_Size + 2)]
XEnd = [(z - 1) * Board_GapX + Board_X1 + Chess_Radius for _ in range(1, Board_Size + 2) for z in range(1, Board_Size + 2)]
YEnd = [(i - 1) * Board_GapY + Board_Y1 + Chess_Radius for i in range(1, Board_Size + 2) for _ in range(1, Board_Size + 2)]

#2D Board List - list comprehension
board = [[0] * (Board_Size + 1) for _ in range(Board_Size + 1)]

def create_circle(x, y, radius, fill = "", outline = "black", width = 1):
    return c.create_oval(x - radius, y - radius, x + radius, y + radius, fill = fill, outline = outline, width = width)

def Value_Check_int(Value):
    try:
        Value = int(Value)
    except ValueError:
        return "string"
    else:
        return "int"

def MouseClick(event):
    global Click_Cord
    X_click = event.x
    Y_click = event.y
    Click_Cord = Piece_Location(X_click, Y_click)
    print(Click_Cord)

c.bind("<Button-1>", MouseClick)

Click_Cord = [None, None]

#lambda function - start
Piece_Location = lambda x, y: (next(Game_CordX[i] for i in range(len(XStart)) if x > XStart[i] and x < XEnd[i]), next(Game_CordY[i] for i in range(len(YStart)) if y > YStart[i] and y < YEnd[i]))

LocationFree = lambda x, y: x is not None and y is not None and board[y - 1][x - 1] == 0 
#lambda function - end

def winCheck(Piece_Number, Piece_Colour, board):
    def rowCheck(Piece_Number, board):
        for i in range(len(board)):
            if board[i].count(Piece_Number) >= 5:
                
                for z in range(len(board) - 3):
                    Connection = 0

                    for c in range(5):
                        if board[i][z + c] == Piece_Number:
                            Connection += 1
                        else:
                            break

                    if Connection == 5:
                        return True
        return False

    if rowCheck(Piece_Number, board) or rowCheck(Piece_Number, transpose(board)) or rowCheck(Piece_Number, transposeDiagonalInc(board)) or rowCheck(Piece_Number, transposeDiagonalDec(board)):
        Winner = Piece_Colour
        return Winner

#list comprehension - start
def getDiagonalDec(board, digNum):
    if digNum <= len(board) - 1:
        return [board[j][len(board) - 1 - i] for (i, j) in enumerate(range(digNum, -1, -1))]
    else:
        return [board[j][(len(board) * 2 - 2) - digNum - i] for (i,j) in enumerate(range(len(board) - 1, digNum - len(board), -1))]

def transposeDiagonalDec(board):
    return [getDiagonalDec(board, i) for i in range(len(board) * 2 - 1)]

def getDiagonalInc(board, digNum):
    lst=[]
    if digNum <= len(board) - 1:
        return [board[j][i] for (i, j) in enumerate(range(digNum, -1, -1))]
    else:
        return [board[j][digNum - len(board) + 1 + i] for (i, j) in enumerate(range(len(board) - 1, digNum - len(board), -1))]

def transposeDiagonalInc(board):
    return [getDiagonalInc(board, i) for i in range(len(board) * 2 - 1)]

def transpose(board):
    return [getCol(board, i) for i in range(len(board))]
    
def getCol(board, colNum):
    return [board[i][colNum] for i in range(len(board))]
#llist comprehension - end


def Exit():
    global Stage
    Stage = GameState.EXIT
    myInterface.destroy()

def exit_button():
    b = Button(myInterface, text = "EXIT", font = "Helvetica 10 bold", command = Exit, bg = "gray", fg = "black")
    b.pack()
    b.place(x = width / 2 * 0.5, y = height - Frame_Gap * 1.6 + 15, height = Chess_Radius * 2, width = Chess_Radius * 4)
    return b

exit_btn = exit_button()

Unfilled = 0
Black_Piece = 1
White_Piece = 2

def draw_board(c):
    board_gfx = []
    board_gfx.append(c.create_rectangle(Board_X1 - Frame_Gap, Board_Y1 - Frame_Gap, Board_X1 + Frame_Gap + Board_GapX * Board_Size, Board_Y1 + Frame_Gap + Board_GapY * Board_Size, width = 3))

    for f in range(Board_Size + 1):
        board_gfx.append(c.create_line(Board_X1, Board_Y1 + f * Board_GapY, Board_X1 + Board_GapX * Board_Size, Board_Y1 + f * Board_GapY))
        board_gfx.append(c.create_line(Board_X1 + f * Board_GapX, Board_Y1, Board_X1 + f * Board_GapX, Board_Y1 + Board_GapY * Board_Size))

        board_gfx.append(c.create_text(Board_X1 - Frame_Gap * 1.7, Board_Y1 + f * Board_GapY, text = f + 1, font = "Helvetica 10 bold", fill = "black"))
        board_gfx.append(c.create_text(Board_X1 + f * Board_GapX, Board_Y1 - Frame_Gap * 1.7, text = f + 1, font = "Helvetica 10 bold", fill = "black"))
    return board_gfx

board_gfx = draw_board(c)
pieces = []

#Game Code
while Stage != GameState.EXIT:
    if Stage == GameState.MENU:
        #draw menu
        pass
    elif Stage == GameState.GAME:
        Bottom_Label = c.create_text(width / 2, height - Frame_Gap + 15, text = f"Turn {int(Turn_Num/2 + 0.5)}, {Turn}", font = "Helvetica 25 bold", fill = Turn)
                
        X = Click_Cord[0]
        Y = Click_Cord[1]
        Click_Cord = [None, None]

        if LocationFree(X, Y):
            pieces.append(create_circle(Board_X1 + Board_GapX * (X - 1), Board_Y1 + Board_GapY * (Y - 1), radius = Chess_Radius, fill = Turn))
            c.update()

            if Turn_Num % 2 == 0:
                White_Cord_PickedX.append(X)
                White_Cord_PickedY.append(Y)
                board[Y - 1][X - 1] = 2
                Turn = "black"
            else:
                Black_Cord_PickedX.append(X)
                Black_Cord_PickedY.append(Y)
                board[Y - 1][X - 1] = 1
                Turn = "white"

            Turn_Num += 1

            if Turn == "white" and winCheck(Black_Piece, "Black", board):
                Stage = GameState.BLACK_WIN
            elif Turn == "black" and winCheck(White_Piece, "White", board):
                Stage = GameState.WHITE_WIN
        
        c.update()
        c.delete(Bottom_Label)
    elif Stage == GameState.BLACK_WIN or Stage == GameState.WHITE_WIN:
        for e in pieces:
            c.delete(e)
        for e in board_gfx:
            c.delete(e)
        if Stage == GameState.WHITE_WIN:
            Bottom_Label = c.create_text(width / 2, height / 2, text = "WHITE WINS!", font = "Helvetica 25 bold", fill = "white")
        elif Stage == GameState.BLACK_WIN:
            Bottom_Label = c.create_text(width / 2, height / 2, text = "BLACK WINS!", font = "Helvetica 25 bold", fill = "black")
        exit_btn.destroy()
        c.update()
        sleep(5)
        Click_Cord = [None, None]
        c.delete(Bottom_Label)
        board_gfx = draw_board(c)
        exit_btn = exit_button()
        board = [[0] * (Board_Size + 1) for _ in range(Board_Size + 1)]
        Stage = GameState.GAME
        Turn = "black"
        Turn_Num = 1