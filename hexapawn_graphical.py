#!/usr/bin/env python3

"""hexapawn_graphical.py

This script provides a graphical interface for the game.

"""


import hexapawn_core as core
from tkinter import *

COLOUR1 = 'black',
COLOUR2 = 'white',
TILE_SIZE = 6


def main():
    """
    program entry point
    """
    game = core.Game()
    gui = GUI(game)
    gui.mainloop()


class GUI(Tk):
    def __init__(self, game):

        self.game = game
        self.m1 = None

        # Set up Tkinter Toplevel widget
        Tk.__init__(self)
        self.title("Hexapawn")
        self.resizable(0, 0)
        self.wpawn = PhotoImage(file='assets/white.gif')
        self.bpawn = PhotoImage(file='assets/black.gif')
        self.empty = PhotoImage(file='assets/empty.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.wpawn)

        # Create Score Labels
        self.notice = StringVar()
        Label(
            self, textvariable=self.notice, width=45, height=2,
            font="Sans 12 bold"
        ).pack(pady=10)

        # Create game board
        self.tiles = list()
        self.tile_frame = Frame()
        self.tile_frame.pack(padx=60, pady=(0, 60))
        self.new_game_button = Button(
            self, text='NEW GAME', command=self.enable
        )
        self.new_game_button.pack_forget()

        # Create game board tiles
        color = COLOUR1
        i = 0
        for row in range(3):
            for col in range(3):
                tile = Button(self.tile_frame)
                tile.config(
                    relief=FLAT,
                    bg=color,
                    activebackground=color,
                    command=lambda i=i: self.player_selected(i)
                )
                tile.grid(column=col, row=row)
                self.tiles.append(tile)
                color = COLOUR1 if color == COLOUR2 else COLOUR2
                i += 1
        self.set_pieces()

    def set_pieces(self):
        """
        moves pawns around the board
        """

        for i in range(9):
            piece = self.game.board[i]
            if piece is core.BLACK:
                self.tiles[i].config(image=self.bpawn)
                self.tiles[i].image = self.wpawn

            elif piece is core.WHITE:
                self.tiles[i].config(image=self.wpawn)
                self.tiles[i].image = self.bpawn

            else:
                self.tiles[i].config(image=self.empty)
                self.tiles[i].image = self.empty

    def player_selected(self, position):
        """
        determines which tile the player clicked on
        :param position:
        """

        if self.m1 is not None:
            self.move(self.m1, position)
            self.m1 = None
        else:
            if self.game.board[position] is core.WHITE:
                self.m1 = position

    def move(self, m1, m2):
        """
        communicates to the hexapawn_core suite of functions to calculate moves
        :param m1: move from
        :param m2: move to
        """

        try:
            core.white_move(m1 + 1, m2 + 1, self.game)
        except core.IllegalMove:
            self.notice.set('Illegal move.')
            return
        except core.IllegalCoordinate:
            self.notice.set('Illegal coordinates.')
            return

        self.set_pieces()
        if self.game.winner:
            self.notice.set(self.game.message.replace('\n', '-- '))
            self.notice.set(
                '{}\n{}'.format(self.notice.get(), self.game.overview()))
            self.disable()
            return

        core.black_move(self.game)
        self.set_pieces()
        self.notice.set(self.game.message.replace('\n', '-- '))

        if self.game.winner:
            self.notice.set(
                '{}\n{}'.format(self.notice.get(), self.game.overview()))
            self.disable()
            return

    def disable(self):
        """
        disables intaraction with the gameboard pieces
        """

        for tile in self.tiles:
            tile.config(state='disabled')
        self.new_game_button.pack(pady=16)
        self.tile_frame.pack(padx=60, pady=0)

    def enable(self):
        """
        enables intaraction with the gameboard pieces
        """

        for tile in self.tiles:
            tile.config(state='normal')
        self.game.reset()
        self.set_pieces()
        self.new_game_button.pack_forget()
        self.tile_frame.pack(padx=60, pady=(0, 60))


# If the script is run directly, start game
if __name__ == "__main__":
    main()
