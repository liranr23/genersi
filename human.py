import random
from game import getScoreOfBoard, isValidMove
from constants import PLAYER_X, PLAYER_O

def drawBoard(board):
    HLINE = '  +---+---+---+---+---+---+---+---+'
    
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print (y+1),
        for x in range(8):
            print ('| %s' % (board[x][y])),
        print('|')
        print(VLINE)
        print(HLINE)

def enterPlayerTile():
    # Lets the player type which tile they want to be.
    tile = ''
    while not (tile == PLAYER_X or tile == PLAYER_O):
        print('Do you want to be X or O?')
        tile = raw_input().upper()

    # the first element in the tuple is the player's tile, the second is the computer's tile.
    if tile == PLAYER_X:
        return [PLAYER_X, PLAYER_O]
    else:
        return [PLAYER_O, PLAYER_X]

def showPoints(playerTile, computerTile, mainBoard):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))



def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = raw_input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]



def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return raw_input().lower().startswith('y')
