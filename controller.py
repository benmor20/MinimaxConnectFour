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
    """
    def __init__(self, board: ConnectFour, red: bool, depth: int = 4):
        """
        Initializes an instance of a controller

        :param board: the ConnectFour board this controller operates on
        :param red: a boolean, True if P1, False if P2
        :param depth: an int that describes the maximum look depth
        """
        super().__init__(board, red)
        self.depth = depth

    def move(self):
        """
        Performs a move using minimax
        """
        self._board.place_token(minimax(self.depth, self._board, self.red, True))


class MinimaxABController(MinimaxController):
    """
    A minimax controller that uses alpha-beta pruning

    Attributes:
        alpha: an int, the alpha parameter for AB pruning
        beta: an int, the beta parameter for AB pruning
    """
    def __init__(self, board: ConnectFour, red: bool, depth: int = 4, alpha: int = 1000000000, beta: int = 1000000000):
        """
        Initialize an instance of this controller

        :param board: the ConnectFour board this controller operates on
        :param red: a bool, whether this controller controls the red player
        :param depth: an int, the number moves ahead minimax should look
        :param alpha: an int, the alpha parameter for AB pruning
        :param beta: an int, the beta parameter for AB pruning
        """
        super().__init__(board, red, depth)
        self.alpha = alpha
        self.beta = beta

    def move(self):
        """
        Performs a move using minimax with alpha-beta pruning
        """
        self._board.place_token(minimaxab(self.depth, self._board, self.alpha, self.beta, self.red))
