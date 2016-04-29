# py-hexapawn

Hexapawn is a two-player board game invented by Martin Gardner. It is played on
a 3x3 board with each player given 3 pawn pieces. To win a round a player must
either reach the oposite side of the gameboard or trap their opponents pieces by
preventing them from performing a legal move.



## Running the Program

  * With either `./hexapawn.py` or `python3 hexapawn.py`
  * Has two modes of play, retro and graphical, which are selectable through a prompt when running the game.
  * Runs usising **python3.1+**. Has no external module dependencies other than Tkinter for grahpical mode which is typically bundled with Python 3 in most distributions.


### Retro Mode

  * Retro mode intends to run the program in exactly the same format as the original to demonstrate the fidelity of the adaptation.
  * Can also be run directly by executing `./hexapawn-retro.py`.
  * The only difference from the BASIC version with respect to functionality is the option of exiting the program by returning `q` during a move prompt.

![](assets/screenshot-retro.png)


### Graphical Mode

  * Graphical mode is a modernized version of the game running in a GUI made with Tkinter, however runs off of the same game logic as retro.
  * Can also be run directly by executing `./hexapawn-graphical.py`.


![](assets/screenshot-graphical.png)


## Acknowledgements

This implementation was based off of Creative Computing's BASIC implementation 
as published in the 1978 book *BASIC Computer Games: Microcomputer Edition*. The motivation begind this project was to have fun modernizing legacy code. The original source for the 
BASIC version is available for viewing on the [atariarchives website](http://www.atariarchives.org/basicgames/showpage.php?page=83).

Pawn assets where sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Chess_plt45.svg) under the Creative Common license.