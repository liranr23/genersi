import random
import sys
from settings.constants import PLAYER_X, PLAYER_O

def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = PLAYER_X
    board[3][4] = PLAYER_O
    board[4][3] = PLAYER_O
    board[4][4] = PLAYER_X


def getNewBoard():
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == PLAYER_X:
        otherTile = PLAYER_O
    else:
        otherTile = PLAYER_X

    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction

        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue

            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break

            if not isOnBoard(x, y):
                continue

            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getComputerMove(board, computerTile, difficulty = 'Master'):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.

    possibleMoves = getValidMoves(board, computerTile)

    if difficulty.upper() == 'NOOB':
      return random.choice(possibleMoves)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    if difficulty.upper() == 'MASTER':
      for x, y in possibleMoves:
          if isOnCorner(x, y):
              return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
            dupeBoard = getBoardCopy(board)
            makeMove(dupeBoard, computerTile, x, y)
            score = getScoreOfBoard(dupeBoard)[computerTile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score

    return bestMove    

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys PLAYER_X and PLAYER_O.
    xscore = 0
    oscore = 0
    empty = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] == PLAYER_X:
                xscore += 1
            if board[x][y] == PLAYER_O:
                oscore += 1
            if board[x][y] == ' ':
                empty += 1

    return {PLAYER_X:xscore, PLAYER_O:oscore, ' ': empty}

def getScoreOfPlayer(board, player):
    otherPlayer = {PLAYER_X: PLAYER_O, PLAYER_O: PLAYER_X}[player]
    score = getScoreOfBoard(board)
    return score[player] - score[otherPlayer]


def gameOver(board):
    possibleMoves = getValidMoves(board, PLAYER_O) + getValidMoves(board, PLAYER_X)
    return len(possibleMoves) == 0

def winner(board):
    playerXScore = getScoreOfPlayer(board, PLAYER_X)
    if playerXScore == 0:
      return 'TIE'
    if playerXScore > 0:
      return PLAYER_X
    
    return PLAYER_O

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)
