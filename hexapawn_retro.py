#!/usr/bin/env python3

"""hexapawn_retro.py

This script provides a command line interface for the game.

"""


import textwrap

import hexapawn_core as core


def main():
    """
    program entry point
    """

    print_intro()
    game = core.Game()

    # Begin main game loop
    while True:

        # Process white (player) move
        print_board(game.board)
        if not player_move(game):
            return  # Exit if player enters 'quit'

        # Print game overview if the player wins
        if game.winner:
            print(game.message.upper())
            print(game.overview())
            game.reset()
            continue

        # Process black (cpu) move
        print_board(game.board)
        core.black_move(game)
        print(game.message.upper())

        if game.winner:
            print(game.overview())
            game.reset()
            continue


def player_move(game):
    """
    prompts user for move directive, checks for exit condition
    :param game: an instance of hexapawn_core's Game class; stores game state
    :return: False if user enters 'quit', else True
    """
    while True:

        print('YOUR MOVE?', end=' ')
        response = input()

        if response.upper() == 'QUIT':
            return False

        try:
            move = response.split(',')
            m1 = int(move[0])
            m2 = int(move[1])
        except:
            print('ILLEGAL MOVE')
            continue

        try:
            core.white_move(m1, m2, game)
            break
        except core.IllegalMove:
            print('ILLEGAL MOVE')
        except core.IllegalCoordinate:
            print('ILLEGAL CO-ORDINATES.')
    print()
    return True


def print_intro():
    """
    displays the game's introduction and instructions
    """
    show_instructions = None
    print("\033c")  # clear terminal window
    print('HEXAPAWN'.center(42))
    print('CREATIVE COMPUTING MORRISTOWN, NEW JERSEY')

    # Prompt user for instructions
    while show_instructions is None:
        print('\nINSTRUCTIONS (Y-N)?', end=' ')
        response = input().upper()
        if response == 'Y' or response == 'YES':
            show_instructions = True
        elif response == 'N' or response == 'NO':
            show_instructions = False

    # Print instructions if requested
    if show_instructions:
        print('\nTHIS PROGRAM PLAYS THE GAME OF HEXAPAWN.\n')
        print(textwrap.fill(
            'HEXAPAWN IS PLAYED WITH CHESS PAWNS ON A 3 BY 3 BOARD. THE '
            'PAWNS ARE MOVED AS IN CHESS - ONE SPACE FORWARD TO AN EMPTY '
            'SPACE OR ONE SPACE FORWARD AND DIAGONALLY TO CAPTURE AN '
            'OPPOSING MAN. ON THE BOARD, YOUR PAWNS ARE \'O\', THE '
            'COMPUTER\'S PAWNS ARE \'X\', AND EMPTY SQUARES ARE \'.\'. '
            'TO ENTER A MOVE, TYPE THE NUMBER OF THE SQUARE YOU ARE '
            'MOVING FROM, FOLLOWED BY THE NUMBER OF THE SQUARE YOU WILL '
            'MOVE TO. THE NUMBERS MUST BE SEPARATED BY A COMMA.',
            width=core.WRAP), '\n'
        )

        print(textwrap.fill(
            'THE COMPUTER STARTS A SERIES OF GAMES KNOWING ONLY WHEN THE '
            'THE GAME IS WON (A DRAW IS IMPOSSIBLE) AND HOW TO MOVE. IT '
            'HAS NO STRATEGY AT FIRST AND JUST MOVES RANDOMLY. HOWEVER, '
            'IT LEARNS FROM EACH GAME. THUS, WINNING BECOMES MORE AND '
            'MORE DIFFICULT. ALSO, TO HELP OFFSET YOUR INITIAL ADVANTAGE '
            'YOU WILL NOT BE TOLD HOW TO WIN THE GAME BUT MUST LEARN THIS '
            'BY PLAYING.',
            width=core.WRAP), '\n'
        )

        print(
            'THE NUMBERING OF THE BOARD IS AS FOLLOWS:\n'
            '\t123\n'
            '\t456\n'
            '\t789\n'
        )

        print(textwrap.fill(
            'FOR EXAMPLE, TO MOVE YOUR RIGHTMOST PAWN FORWARD, YOU WOULD '
            'TYPE 9,6 IN RESPONSE TO THE QUESTION \'YOUR MOVE?\'. SINCE '
            'I\'M A GOOD SPORT, YOU\'LL ALWAYS GO FIRST.',
            width=core.WRAP)
        )


def print_board(gameboard):
    """
    prints the current state of the board to stdout
    :param gameboard: a list of ints containing the state of the game board
    """

    out = '\n'
    for i in range(9):
        val = gameboard[i]
        if i % 3 == 0: out += '\t'
        if val == -1:
            out += 'X'
        elif val == 0:
            out += '.'
        else:
            out += 'O'
        if (i + 1) % 3 == 0: out += '\n'
    print(out)


# If the script is run directly, start game
if __name__ == "__main__":
    main()
