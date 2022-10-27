"""
Module to contain the view for Connect Four game.
"""

from abc import ABC, abstractmethod
from model import ConnectFour

class View(ABC):
    """
    View Discrete Group Deep Dive

    Attrbitues:
        _gameboard: the active Connect4 instance.
    """

    def __init__(self, gameboard):
        """
        Initialize gameboard.

        Args:
            gameboard: a Connect4 instance.
        """
        self._gameboard = gameboard
    
    @property
    def gameboard(self):
        """
        Return the Connect4 instance being represented by this view.
        """
        return self._gameboard

    @abstractmethod
    def draw(self):
        """
        Draw the gameboard Connect4 instance.
        """

class ConnectFourView(View):
    """
    An ASCII viewer for Connect4

    Attributes:
    """

    def __init__(self, gameboard):
        """
        Initialize PyGameView

        Args:
            gameboard: a Factory instance.
        """
        super().__init__(gameboard)

    def win(self): 
        """
        Returns the win condition
        """
        pass

    def draw(self):
        """
        Updates the view to include ASCII board & win condition.
        """
        # Draw initial line
        self.draw_line()
        for row in self._gameboard.board:
            for value in row:
                if value == -1:
                    print(f'X|', end='')
                elif value == 0:
                    print(' |', end='')
                else:
                    print(f'O|', end='')
            self.draw_line()
        
    def draw_line(self,last=False):
        print("\n+", end='')
        for i in range(self._gameboard.board.shape[1]):
            print("-+", end='')
        if last != True: 
            print("\n|", end='')

        