"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x, o = 0, 0
    for row in board:
        for p in row:
            if p == X:
                x += 1
            elif p == O:
                o += 1
    return X if x == o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action[0], action[1]
    if board[i][j] != EMPTY:
        raise Exception("Incorrect action for given board")
    new = copy.deepcopy(board)
    new[i][j] = player(board)
    return new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if EMPTY != board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if EMPTY != board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    for row in board:
        if EMPTY != row[0] == row[1] == row[2]:
            return row[0]

    for row in zip(board[0], board[1], board[2]):
        if EMPTY != row[0] == row[1] == row[2]:
            return row[0]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None:
        for row in board:
            for cell in row:
                if cell is EMPTY:
                    return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    return 1 if w == X else -1 if w == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def minval(state):
        if terminal(state):
            return utility(state), None
        v = float('inf')
        best = None
        for action in actions(state):
            max_result, _ = maxval(result(state, action))
            if v > max_result:
                v = max_result
                best = action
        return v, best

    def maxval(state):
        if terminal(state):
            return utility(state), None
        v = float('-inf')
        best = None
        for action in actions(state):
            min_result, _ = minval(result(state, action))
            if v < min_result:
                v = min_result
                best = action
        return v, best

    if player(board) == X:
        return maxval(board)[1]
    else:
        return minval(board)[1]