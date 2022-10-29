"""
Module to contain the view for Connect Four game.
"""

from abc import ABC, abstractmethod
from model import ConnectFour


class View(ABC):
    """
    An ABC to represent a View of the game

    Attrbitues:
        _gameboard: the active Connect4 instance.
    """

    def __init__(self, gameboard: ConnectFour):
        """
        Initialize the view.

        Args:
            gameboard: a ConnectFour instance to draw
        """
        self._gameboard = gameboard
    
    @property
    def gameboard(self) -> ConnectFour:
        """
        Return the Connect4 instance being represented by this view.
        """
        return self._gameboard

    @abstractmethod
    def draw(self):
        """
        Draw the gameboard Connect4 instance.
        """
        pass


class TextView(View):
    """
    An ASCII viewer for Connect4
    """
    def draw(self):
        """
        Draws the current state of the board to the console
        """
        for row in self._gameboard.board:
            # Draw separation line
            self.draw_line()
            # Draw each square in the row
            for value in row:
                if value == -1:
                    print(f'X|', end='')
                elif value == 0:
                    print(' |', end='')
                else:
                    print(f'O|', end='')
        # Draw bottom line
        self.draw_line(True)

        # If someone won, print out their win
        winner = self.gameboard.check_win()
        if winner == 1:
            print('Player 1 won!')
        elif winner == -1:
            print('Player 2 won!')
        
    def draw_line(self, last=False):
        """
        Draws a separation line

        :param last: a bool, whether this is the last separation line
        """
        print("\n+", end='')
        for i in range(self._gameboard.board.shape[1]):
            print("-+", end='')
        if last:
            print()
        else:
            print("\n|", end='')

        