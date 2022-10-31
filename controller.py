"""
Module to contain all the controllers for the Connect Four game.
"""

from abc import ABC, abstractmethod
from model import ConnectFour
from minimax import minimax, minimaxab


class Controller(ABC):
    """
    An Abstract Base Class for controllers.

    Handles either players or AI playing the game

    Attributes:
        red: a boolean, True if this controller is for the Red player (P1),
            and False for Black player (P2).
    """
    def __init__(self, board: ConnectFour, red: bool):
        """
        Initializes an instance of a controller

        :param board: the ConnectFour board this controller operates
        :param red: a boolean, True if P1, False if P2
        """
        self._board = board
        self.red = red

    @abstractmethod
    def move(self):
        """
        Performs one move for this controller's player on their turn.
        """
        pass


class PlayerController(Controller):
    """
    A Controller which uses text input from the user to determine moves.
    """
    def move(self):
        """
        Asks the user for a move and performs it
        """
        while True:
            # Get move
            move_str = input('Where would you like to play your piece (1-7)? ')

            # Attempt to convert to integer
            try:
                move = int(move_str)
            except ValueError:
                print('Please enter a number.')
                continue

            # Ensure given int is in bounds
            if move < 1 or move > self._board.board.shape[1]:
                print('Please enter a number between 1 and 7')
                continue

            # Make the move, if invalid try again
            if not self._board.place_token(move - 1):
                print('Invalid move')
                continue

            # If got this far, made a valid move, can exit
            return


class DummyController(Controller):
    """
    A Controller for testing purposes, which plays the leftmost available move.
    """
    def move(self):
        """
        Performs the leftmost available move.
        """
        for col in range(self._board.board.shape[1]):
            if self._board.place_token(col):
                return


class MinimaxController(Controller):
    """
    A minimax controller.

    Attributes:
        depth: an int, how many moves ahead the minimax algorithm should look
        total_calls: an int, the total number of calls
    """
    def __init__(self, board: ConnectFour, red: bool, depth: int = 6):
        """
        Initializes an instance of a controller

        :param board: the ConnectFour board this controller operates on
        :param red: a boolean, True if P1, False if P2
        :param depth: an int that describes the maximum look depth
        """
        super().__init__(board, red)
        self.depth = depth
        self.total_calls = 0

    def move(self):
        """
        Performs a move using minimax
        """
        col, calls = minimax(self.depth, self._board, self.red)
        self.total_calls += calls
        self._board.place_token(col)


class MinimaxABController(MinimaxController):
    """
    A minimax controller that uses alpha-beta pruning
    """

    def move(self):
        """
        Performs a move using minimax with alpha-beta pruning
        """
        col, calls = minimaxab(self.depth, self._board, self.red)
        self.total_calls += calls
        self._board.place_token(col)
