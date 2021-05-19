from random import randint
from random import choice
from copy import copy
import os

def print_grid(board):
	print('   |   |')
	print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
	print('   |   |')

def choose_symbol():
    letter = ''
    while not (letter == "X" or letter == "O"):
        letter = input("Do you want to be X or O: ").upper()
    if letter == "X":
        return ["X", "O"]
    else:
        return ["O", "X"]

def whoGoesFirst():
	if randint(0, 1) == 0:
		return "Computer"
	else:
		return "Human"

def empty_places(board):
    l = []
    for i in range(9):
        if board[i] == " ":
            l.append(i)
    return l, len(l)

#key --> playing = 0, tie = 1, X = 2, O = 3
def check_state(b): #input board and return state 
    winning_triplets = [[0,1,2],[0,3,6],[0,4,8],[3,4,5],[1,4,7],[2,4,6],[6,7,8],[2,5,8]]
    for l in winning_triplets:
        if b[l[0]] == b[l[1]] == b[l[2]] == "X":
            return 2
    for m in winning_triplets:
        if b[m[0]] == b[m[1]] == b[m[2]] == "O":
            return 3
    if empty_places(b)[1] == 0:
        return 1
    return 0    
    
#returns list of possible winners --  list of a list -- sublist contains [winning symbol, winning move]
def check_win_possible(b):
    winning_triplets = [[0,1,2],[0,3,6],[0,4,8],[3,4,5],[1,4,7],[2,4,6],[6,7,8],[2,5,8]]
    winners = []
    for triplet in winning_triplets:
        k = triplet
        for i in range(3):
            new_k = copy(k)
            empty_checker = new_k.pop(i)
            if (b[new_k[0]] == b[new_k[1]] == "X" or b[new_k[0]] == b[new_k[1]] == "O")  and b[empty_checker] == " ":
                winners.append([b[new_k[1]], empty_checker]) 
    if winners:
        return winners
    return False 

def computer_turn(board): #take input of grid and return best move (int) for computer
    k = empty_places(board)

    #if computer can win, then play winning move
    winners = check_win_possible(board)
    if winners: #can anyone win?
        for winner in winners:
            if winner[0] == computer_symbol: #checking if comp can win
                return winner[1]  #(computer can win)

        return winners[0][1] #human can win - block human

    if 4 in k[0]:
        return 4
    for box in [0,2,6,8]:
        if box in k[0]:
            return box

    #if cannot do either, play in a random empty spot (most likely draw?)
    return choice(empty_places(board)[0])
    

def move(board, symbol, move):
    board[move] = symbol


def getPlayerMove(board):
    move = '100'
    l = empty_places(board)[0]
    k = [str(x+1) for x in l]
    while move not in k:
        move = input("What is your next move? (1-9): ")
    return int(move) - 1

def playAgain():
    return input("Do you want to play again? (y/n): ").lower().startswith('y')

#MAIN 
while True:
    board = [" " for _ in range(10)]
    player_symbol, computer_symbol = choose_symbol()
    print("Player's symbol: ", player_symbol)
    print("Computer's symbol: ", computer_symbol)

    turn = whoGoesFirst()
    print('The ' + turn + ' will start.')
    
    playing = True

    while playing:
        os.system("clear")
                
        if turn == "Computer": #computer's turn
            move_turn = computer_turn(board)
            move(board, computer_symbol, move_turn)
            turn = "Human"

        elif turn == "Human": #player's turn
            print_grid(board)
            move_turn = getPlayerMove(board)
            move(board, player_symbol, move_turn)
            turn = "Computer"

        state = check_state(board)
        if state:
            print_grid(board)
            if state == 1:
                print("The game is a draw!")
            elif state == 2:
                print("X is the winner!")
            elif state == 3:
                print("O is the winner!")
            break
    if not playAgain():
        break



            
