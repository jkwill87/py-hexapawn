#!/usr/bin/env python3

"""hexapawn_core.py

This script stores the common logic used to run both the reto and graphical 
versions of this game.

"""


import random
import sys
from copy import deepcopy

# ensure python version is adequate before proceeding
if sys.version_info < (3, 1):
    print('hexapawn can only run under Python 3.1+')
    raise SystemExit

WRAP = 55
WHITE = 1
BLACK = -1
EMPTY = 0


class HexpawnException(Exception):
    pass


class IllegalCoordinate(HexpawnException):
    pass


class IllegalMove(HexpawnException):
    pass


class Game:
    _initial_moves = (
        [24, 25, 36, 0],
        [14, 15, 35, 36],
        [15, 35, 36, 47],
        [36, 58, 59, 0],
        [15, 35, 36, 0],
        [24, 25, 26, 0],
        [26, 57, 58, 0],
        [26, 35, 0, 0],
        [47, 48, 0, 0],
        [35, 36, 0, 0],
        [35, 36, 0, 0],
        [36, 0, 0, 0],
        [47, 58, 0, 0],
        [15, 0, 0, 0],
        [26, 47, 0, 0],
        [47, 58, 0, 0],
        [35, 36, 47, 0],
        [24, 58, 0, 0],
        [15, 47, 0, 0]
    )

    _initial_board = [
        BLACK, BLACK, BLACK,
        EMPTY, EMPTY, EMPTY,
        WHITE, WHITE, WHITE
    ]

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.winner = None
        self.message = None
        self.board = deepcopy(self._initial_board)
        self.moves = deepcopy(self._initial_moves)
        self.x = self.y = 0
        self.configs = (
            (-1, -1, -1, 1, 0, 0, 0, 1, 1),
            (-1, -1, -1, 0, 1, 0, 1, 0, 1),
            (-1, 0, -1, -1, 1, 0, 0, 0, 1),
            (0, -1, -1, 1, -1, 0, 0, 0, 1),
            (-1, 0, -1, 1, 1, 0, 0, 1, 0),
            (-1, -1, 0, 1, 0, 1, 0, 0, 1),
            (0, -1, -1, 0, -1, 1, 1, 0, 0),
            (0, -1, -1, -1, 1, 1, 1, 0, 0),
            (-1, 0, -1, -1, 0, 1, 0, 1, 0),
            (0, -1, -1, 0, 1, 0, 0, 0, 1),
            (0, -1, -1, 0, 1, 0, 1, 0, 0),
            (-1, 0, -1, 1, 0, 0, 0, 0, 1),
            (0, 0, -1, -1, -1, 1, 0, 0, 0),
            (-1, 0, 0, 1, 1, 1, 0, 0, 0),
            (0, -1, 0, -1, 1, 1, 0, 0, 0),
            (-1, 0, 0, -1, -1, 1, 0, 0, 0),
            (0, 0, -1, -1, 1, 0, 0, 0, 0),
            (0, -1, 0, 1, -1, 0, 0, 0, 0),
            (-1, 0, 0, -1, 1, 0, 0, 0, 0)
        )

    def reset(self):
        """
        resets the state of the board between games
        """

        self.board = deepcopy(self._initial_board)
        self.winner = None
        self.message = None

    def game_over(self, winner, message=None):
        """
        sets the win message and removes losing strategies
        :param winner:
        :param message:
        """

        # If the white won...
        if winner is WHITE:
            self.wins += 1

            if message:
                self.message = message
            else:
                self.message = 'You win.'

            # Remove losing strategy from moves list
            self.moves[self.x][self.y] = 0

        # If black won...
        elif winner is BLACK:

            self.losses += 1

            if message:
                self.message += '\n' + message
            else:
                self.message += '\nI win.'


        # Winner should only ever be white or black
        else:
            raise HexpawnException

        self.winner = winner

    def overview(self):
        """
        produces an overview of the game and returns it as a string
        :return: the overview string
        """

        return 'I have won {} and you {} out of {} games.'.format(
            self.losses, self.wins, self.losses + self.wins
        )


def fnr(x):
    """
    mirrors gameboard on the vertical axis
    :param x:
    :return:
    """

    rval = {
        1: 3, 3: 1,
        4: 6, 6: 4,
        7: 9, 9: 7
    }
    return rval.get(x, x)


def white_move(m1, m2, game):
    """
    processes white (player) moves
    :param m1: from position
    :param m2: to position
    :param game: game state
    """

    assert game.winner is None
    game.message = None

    # Ensure move is on the board
    if m1 not in range(1, 10) or m2 not in range(1, 10):
        raise IllegalCoordinate

    # Ensure player is moving their own piece
    if game.board[m1 - 1] is not WHITE:
        raise IllegalCoordinate

    # Ensure player isn't moving onto their own piece
    if game.board[m2 - 1] is WHITE:
        raise IllegalMove

    # Ensure if moving diagonally its onto an opponents piece
    if m2 - m1 != -3 and game.board[m2 - 1] is not BLACK:
        raise IllegalMove

    # Ensure the user is not trying to move left, right, or down
    if m2 > m1:
        raise IllegalMove

    # Make sure if moving forward, destination is unoccupied
    if m2 - m1 == -3 and game.board[m2 - 1] is not EMPTY:
        raise IllegalMove

    # Enusre if the player is moving forward it is within allowable range
    if m2 - m1 < -4:
        raise IllegalMove

    # Ensure user isn't moving from bottom left of board to top right
    if m1 == 7 and m2 == 3:
        raise IllegalMove

    # Perform move
    game.board[m1 - 1] = EMPTY
    game.board[m2 - 1] = WHITE

    # Check if any white pieces have reached the far row
    if WHITE in (game.board[0], game.board[1], game.board[2]):
        game.game_over(WHITE)
        return

    # Check if all of black's pieces have been captured
    if BLACK not in game.board:
        game.game_over(WHITE)
        return

    # Check if black can move forward
    for i in range(6):
        if game.board[i] is BLACK:
            if game.board[i + 3] is EMPTY:
                return

    # Check if black can capture a piece
    for i in (0, 1, 3, 4):
        if game.board[i] is BLACK and game.board[i + 4] is WHITE:
            return

    for i in (1, 2, 4, 5):
        if game.board[i] is BLACK and game.board[i + 2] is WHITE:
            return

    # If black has no valid moves white wins
    game.game_over(WHITE)


def black_move(game):
    """
    processes black (cpu) move
    :param game: game state
    """

    assert game.winner is None
    game.message = None
    strategies = list()
    r = None

    for game.x in range(19):
        current_config = list(game.configs[game.x])
        mirrored_config = list(current_config)
        mirrored_config[0] = current_config[2]
        mirrored_config[3] = current_config[5]
        mirrored_config[6] = current_config[8]
        mirrored_config[2] = current_config[0]
        mirrored_config[5] = current_config[3]
        mirrored_config[8] = current_config[6]

        if game.board == current_config:
            r = False
            break
        elif game.board == mirrored_config:
            r = True
            break

    # Could not find board configuration-- should not be possible
    assert r is not None

    # Try and find a strategy in the moves list
    for i in range(4):
        if game.moves[game.x][i] != 0:
            strategies.append(i)

    # If a move cannot be found, black resigns
    if not strategies:
        game.game_over(WHITE, message='I resign.')
        return

    # Get black's move
    game.y = random.choice(strategies)
    move = divmod(game.moves[game.x][game.y], 10)
    if r:
        move = (fnr(move[0]), fnr(move[1]))

    # Perform move
    game.board[move[0] - 1] = EMPTY
    game.board[move[1] - 1] = BLACK
    game.message = 'I move from {} to {}'.format(move[0], move[1])

    # Check if any black pieces have reached the far row
    if BLACK in (game.board[6], game.board[7], game.board[8]):
        game.game_over(BLACK)
        return

    # Check if all of white's pieces have been captured
    if WHITE not in game.board:
        game.game_over(BLACK)
        return

    # Check if white can move forward
    for i in range(3, 9):
        if game.board[i] is WHITE:
            if game.board[i - 3] is EMPTY:
                return

    # Check if white can capture a piece
    for i in (4, 5, 7, 8):
        if game.board[i] is WHITE and game.board[i - 4] is BLACK:
            return

    for i in (3, 4, 6, 7):
        if game.board[i] is WHITE and game.board[i - 2] is BLACK:
            return

    game.game_over(BLACK, message='You can\'t move, so I win.')
