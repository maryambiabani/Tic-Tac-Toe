 # Tic Tac Toe

from Game_Base import *
import random
import numpy as np
#______________________________________________________________

game_base = Game_Base()
game_base_matrix,game_base_feasible = game_base.build_matrix()
game_base_feasible.sort(key=lambda x: x[9])
mutation_probability=0.7
crossover_probability=0.8 # don't use crossover
def drawBoard(board):
    # print(board)
# This function prints out the board that it was passed.
# "board" is a list of 9 strings representing the board (ignore index 0)
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
#____________________________________________________________________________________________________
def inputPlayerLetter():
# Lets the player type which letter they want to be.
# Returns a list with the player’s letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
        # the first element in the list is the player’s letter, the second is the computer's letter.
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

#__________________________________________________________________________________________________
def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'
#_________________________________________________________________________________________________
def isWinner(bo, le):
    # bo is board and le is letter
    return ((bo[0] == le and bo[1] == le and bo[2] == le) or # across the top
        (bo[3] == le and bo[4] == le and bo[5] == le) or # across the middle
        (bo[6] == le and bo[7] == le and bo[8] == le) or # across the bottom
        (bo[0] == le and bo[3] == le and bo[6] == le) or #  the left side
        (bo[1] == le and bo[4] == le and bo[7] == le) or #  the middle
        (bo[2] == le and bo[5] == le and bo[8] == le) or #  the right side
        (bo[0] == le and bo[4] == le and bo[8] == le) or # diagonal
        (bo[2] == le and bo[4] == le and bo[6] == le)) # diagonal
#________________________________________________________________________________________________
def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard
#________________________________________________________________________________________________
def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '
#________________________________________________________________________________________________
def getPlayerMove(board):
    # Let the player type in their move.
    move = ' '
    while move not in '0 1 2 3 4 5 6 7 8'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (0-8)')
        move = input()
    return int(move)
#_______________________________________________________________________________________________
def find_level_part(level):
    correct_indices=[]
    for i in game_base_feasible:
        i=list(i)
        p=i.copy()
        e=i.pop()
        if e is level:
            correct_indices.append(game_base_feasible.index(tuple(p)))
    return correct_indices
#____________________________________________________________________________________________
def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
     for i in range(1, 10):
         if isSpaceFree(board, i):
             return False
     return True
#_____________________________________________________________________________________________
def makeMove(board, letter, move):
    board[move] = letter
#_____________________________________________________________________________________________
def fitness(last,next):     # compute fitness by last move just for computer
    pure=[]
    score = 0
    if isWinner(next,1):
        score +=10
    for i in range(len(next)):
        if last[i] is next[i]:
            pure.append(1)
        else:
            pure.append(0)
    if pure[4] is 1:
        score +=1
    if pure[0]==1 or pure[2]==1 or pure[6]==1 :
        score +=0.5
    if pure[1]==1 or pure[3]==1 or pure[5]==1 :
        score +=0.25
    return score
#____________________________________________________________________________________________
def mutation(last, next):
    pure = []
    for i in range(len(next)):
        if last[i] is next[i]:
            pure.append(0)
        else:
            pure.append(1)
    valid_index = []
    for i in range(len(last)):
        if next[i] is 0:
            valid_index.append(i)
    rand=random.uniform(0,1)
    if mutation_probability > rand:
        mutate = random.choice(valid_index)
        last[mutate]=1
    return last

#_____________________________________________________________________________________________
def shape2num(board,playerLetter,computerLetter):
    game_state=[]
    for e in board:
        if e is computerLetter:
            game_state.append(1)
        if e is playerLetter:
            game_state.append(2)
        if e is " ":
            game_state.append(0)
    return game_state
#_____________________________________________________________________________________________


wLevel = []
index_number = []
for row in game_base_feasible:
    row = list(row)
    del row[9]
    wLevel.append(row)
def make_generation(board, level):
    s_space=[]
    final=[]
    feasible_index=find_level_part(level=level)
    for i in feasible_index:
        # list(game_base_feasible[i]).pop()
        if board.count(2)==wLevel[i].count(2):
            if board.count(1) < wLevel[i].count(1):
                s_space.append(wLevel[i])
    for e in s_space:

        c=0
        for i in range(len(e)):
            if e[i] is board[i]:
                c +=1
        if c ==len(board)-1:
            final.append(e)
    return final
#_____________________________________________________________________________________________
def parent_selection(board,generation,num):
    fit=[]
    for chorom in generation:
        fit.append(fitness(board,chorom))
    s=sum(fit)
    prob=[x/s for x in fit if s is not 0]
    selected=np.random.choice(len(generation),num,p=prob)
    new_generation=[]
    for e in selected:
        new_generation.append(generation[e])
    return new_generation           #matrix of new generation
#_____________________________________________________________________________________________
def getComputerMove(board, level):
    # ______________________make initial generation____________________________________________
    generation=make_generation(board, level)
    # print("candid generation is",generation)
    #________________________parent selection__________________________________________________
    selected=parent_selection(board,generation,4)
    next1=random.choice(selected)
    #_________________________mutation_________________________________________________________
    next=mutation(board,next1)
    if next not in generation:
        next=next1
    return next
#______________________________________________________________________________________________
def num2shape(board,playerLetter,computerLetter):
    b=[" "]*9
    for i in  range(len(board)):
        if board[i] is 1:
            b[i]=computerLetter
        if board[i] is 2:
            b[i]=playerLetter
    return b

#_____________________________________________________________________________________________
def playAgain():
# This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')
#_____________________________________________________________________________________________
def crossover(chrom1,chrom2):
    child1 = []
    child2 = []
    if len(chrom1) is not len(chrom2):
        print("error the length of chromosome must be same!!!!")
    else:
        point=random.randint(0,len(chrom2))
        print(point)
        for i in range(len(chrom2)):
            if i<point:
                child1.append(chrom1[i])
                child2.append(chrom2[i])
            else:
                child1.append(chrom2[i])
                child2.append(chrom1[i])

    return child1, child2



if __name__ == '__main__':
    print('Welcome to Tic Tac Toe!')
    while True:
        # Reset the board
        board_visual = [' '] * 9
        playerLetter, computerLetter = inputPlayerLetter()
        turn = whoGoesFirst()
        # turn="computer"
        print('The ' + turn + ' will go first.')
        gameIsPlaying = True
        level=1
        while gameIsPlaying:

            if turn == 'player':
                # Player’s turn.
                drawBoard(board_visual)
                move = getPlayerMove(board_visual)
                makeMove(board_visual, playerLetter, move)
                drawBoard(board_visual)
                if isWinner(board_visual, playerLetter):
                    drawBoard(board_visual)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(board_visual):
                        drawBoard(board_visual)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'
                level+=1
            else:
                # Computer’s turn.
                # print("board_visual  is ",board_visual)
                board=shape2num(board_visual,playerLetter,computerLetter)
                # print("board is ",board)
                print("level",level)
                new_board = getComputerMove(board,level)
                # print("new board is",new_board)
                board_visual=num2shape(new_board,playerLetter,computerLetter)
                if isWinner(board_visual, computerLetter):
                    drawBoard(board_visual)
                    print('The computer has beaten you! You lose.')
                    gameIsPlaying = False
                else:
                    if isBoardFull(board_visual):
                        drawBoard(board_visual)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'
                level += 1
        if not playAgain():
            break

