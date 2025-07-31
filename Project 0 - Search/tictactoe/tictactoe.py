"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

# All the possible choices for player.
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board. Defined as 3 rows with 3 columns each
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If the provided board is a terminal board. Any value is acceptable
    if terminal(board):
        return EMPTY
    else:
        xCount = sum(row.count(X) for row in board)
        oCount = sum(row.count(O) for row in board)
        return X if xCount == oCount else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    i -> the row of the move, 0, 1 or 2
    j -> the column in said row of the move, 0, 1 or 2
    """
    # If the provided board is a terminal board. Any value is acceptable, we return an empty set
    if terminal(board):
        return set()

    # Initialize the set to return
    possibleActions = set()

    # Otherwise we want to return all the possible playable positions,ie, Where there isn't an X or O.
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                possibleActions.add((row, col))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Action -> (i, j)
    """
    # Check if i and j are within bounds
    if action[0] >= len(board) or action[1] >= len(board[0]):
        raise Exception("Invalid action")
    elif action[0] < 0 or action[1] < 0:
        raise Exception("Invalid action")
    # Check if the action is valid, ie, the cell is empty
    elif board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action.")

    # Copy the board, avoiding changes made from referencing
    boardCopy = deepcopy(board)

    # Change the copy to the new board resulting from the move
    boardCopy[action[0]][action[1]] = player(boardCopy)

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check if any has won horizontally
    for row in range(len(board)):
        numberX = 0
        numberO = 0
        for col in range(len(board[0])):
            if board[row][col] == X:
                numberX = numberX + 1
            elif board[row][col] == O:
                numberO = numberO + 1

        result = handleCountPlayer(numberX, numberO)
        if result is not None:
            return result

    # Check if any has won vertically. Fixing a column number and modifying the row.
    for col in range(len(board[0])):
        numberX = 0
        numberO = 0
        for row in range(len(board)):
            if board[row][col] == X:
                numberX = numberX + 1
            elif board[row][col] == O:
                numberO = numberO + 1

        result = handleCountPlayer(numberX, numberO)
        if result is not None:
            return result

    # Check if any has won on the main diagonal
    numberX = 0
    numberO = 0
    for i in range(len(board)):
        if board[i][i] == X:
            numberX = numberX + 1
        elif board[i][i] == O:
            numberO = numberO + 1

    result = handleCountPlayer(numberX, numberO)
    if result is not None:
        return result

    # Check if any has won on the secondary diagonal
    numberX = 0
    numberO = 0
    for i in range(len(board)):
        j = len(board) - 1 - i
        if board[i][j] == X:
            numberX = numberX + 1
        elif board[i][j] == O:
            numberO = numberO + 1

    result = handleCountPlayer(numberX, numberO)
    if result is not None:
        return result

    # If we reach this deep then no winner has yet been declared
    return None


def handleCountPlayer(numberX, numberO):
    if numberX == 3:
        return X
    elif numberO == 3:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # We can call the winner function and if we get None then the game is not over
    if winner(board) is not None:
        return True
    else:
        return not any (EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    playerWinner = winner(board)
    if playerWinner == O:
        return -1
    elif playerWinner == X:
        return 1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Do a loop that sees into the future for all possible moves
    # optimalResult -> (value, action)
    optimalResult = minimaxValue(board, alpha=-math.inf, beta=math.inf)
    return optimalResult[1]


""" 
Calculates the best value and action for the minimax function 
Returns a tuple of (value, action) representing the value obtained from following said action
"""
def minimaxValue(board, alpha, beta):
    # Define the players. X is max, O is min
    currentPlayer = player(board)

    # If the game is over then we end the recursive call, unwinding one stack-frame and returning the value of the board
    if terminal(board):
        return utility(board), None

    # For the max player. We want to find the biggest value we can
    # optimalResult -> (bestValue, bestAction) so it's easy to understand and pass as a "node"
    # For alpha-beta pruning we just want to check if beta <= alpha. If this happens alpha has better options -> Skip sub-branches.
    if currentPlayer == X:
        bestValue = -math.inf
        bestAction = None
        # Iterate through every possible scenario
        for action in actions(board):
            # Get the new board as the result from the action
            newBoard = result(board, action)
            # Calculate the best action and best value. No depth limit means the AI will check all possible options -> Hard to beat
            value, _ = minimaxValue(newBoard, alpha, beta)
            # Get the new best value and action
            if value > bestValue:
                bestValue = value
                bestAction = action
            # Alpha will become the max value obtained between the current alpha and all possible scenarios explored
            alpha = max(alpha, bestValue)
            # If in anytime beta <= alpha then we know the maximizing player would never choose this option. Abort branch
            if beta <= alpha:
                break
        return bestValue, bestAction
    else:
        bestValue = math.inf
        bestAction = None
        for action in actions(board):
            newBoard = result(board, action)
            value, _ = minimaxValue(newBoard, alpha, beta)
            if value < bestValue:
                bestValue = value
                bestAction = action
            beta = min(beta, bestValue)
            if beta <= alpha:
                break
        return bestValue, bestAction