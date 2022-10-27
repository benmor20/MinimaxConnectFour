"""
Module to contain the view for the Connect Four game.
"""

import numpy as np
from scipy import signal

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

class PlayerView(View):
    """
    A viewer for Connect4

    Attributes:
        _successful_packages: a VisualText which shows the number of packages
                              that Tower instances have handled.
        _lives: a VisualText which shows the number of lives the player has
                left.
        _available_towers: a VisualText which shows the number of Tower
                           instances available to be placed.
    """

    def __init__(self, gameboard):
        """
        Initialize PyGameView

        Args:
            gameboard: a Factory instance.
        """
        super().__init__(gameboard)
        self._win_condition = 
        self._board = 

    def win(self): 
        """
        Returns the win condition
        """
        pass

    def draw(self):
        """
        Updates the view to include ASCII board & win condition.
        """

        print(f"+-+")
        for i in range(0,self._gameboard.board.shape)
        