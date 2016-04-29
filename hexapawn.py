#!/usr/bin/env python3

"""hexapawn.py

This file serves as the entry point for the program, prompting the user to 
either launch either the retro or graphical offering of the game.

"""


import sys
import textwrap
from hexapawn_core import WRAP
import hexapawn_graphical
import hexapawn_retro

argv = sys.argv
argc = len(argv)
graphical_mode = None

# Check that command line arguments are sane before proceeding
if argc > 2:
    print('hexapawn: invalid command line arguments')
    print('usage:\nhexapawn [g|r]')
    raise SystemExit

# If a game mode has been specified, set appropriately
if argc == 2:
    if argc == 2 and argv[1] == 'g':
        graphical_mode = True
    elif argv[1] == 'r':
        graphical_mode = False
    else:
        print('usage:\nhexapawn [g|r]')
        raise SystemExit

# If no game mode has been specified, prompt user
else:
    print('Welcome to Hexapawn.\n')
    print(textwrap.fill(
        'This game offers two modes of play, "graphical" and "retro". '
        'Graphical mode will run the game in a GUI using Tkinter and '
        'provides a more contemporary offering of the game, while retro '
        'mode will run the game in its original format via the command '
        'line.', WRAP)
    )

    # Prompt user for game mode
    while graphical_mode is None:
        print('\nWhich version would you like to play? (G-R)?', end=' ')
        response = input().upper()
        if response == 'G' or response == 'GRAPHICAL':
            graphical_mode = True
        elif response == 'R' or response == 'RETRO':
            graphical_mode = False

# Begin Game
if graphical_mode:
    hexapawn_graphical.main()
else:
    hexapawn_retro.main()

print('Thanks for playing!')
