"""
Module to contain all the controllers for the Connect Four game.
"""

from abc import ABC, abstractmethod
from model import ConnectFour, WIN_KERNELS
from scipy import signal
import numpy as np

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
    """
    def __init__(self, board: ConnectFour, red: bool, depth: int=4):
        """
        Initializes an instance of a controller

        :param board: the ConnectFour board this controller operates
        :param red: a boolean, True if P1, False if P2
        :param depth: an int that describes the maximum look depth
        """
        super().__init__(board, red)
        self.depth = depth

    def move(self):
        """
        Performs a move using minimax
        """
        self._board.place_token(self.minimax(self.depth, self._board, self.red)[1])
        
    def minimax(self, depth, gamestate, maximize):
        """
        depth: an int that describes the maximum look depth

        gamestate: an instance of ConnectFour

        maximize: a bool representing the maximizing (True) or minimizing (False) player. 
        """
        if depth == 0 or gamestate.check_win() != 0:
            return self.static_eval(gamestate), 0
        children = [gamestate.create_child(i) for i in range(7)]
        best = 0, -1
        if maximize:
            # such readable much wow
            # TODO: Investigate draw states
            for i, child in enumerate(children):
                if child is not None:
                    score = self.minimax(depth - 1, child, not maximize)[0]
                    if score > best[0] or best[1] == -1:
                        best = score, i
        else:
            for i, child in enumerate(children):
                if child is not None:
                    score = self.minimax(depth - 1, child, not maximize)[0]
                    if score < best[0] or best[1] == -1:
                        best = score, i
        return best

    def static_eval(self, gamestate):
        """
        gamestate: an instance of ConnectFour
        """
        total = 0
        for kernel in WIN_KERNELS:
            convolution = signal.convolve2d(gamestate.board,kernel, mode="valid")
            total += np.sum(convolution==4) * 100000000
            total += np.sum(convolution==3) * 1
            total += np.sum(convolution==-4) * -100000000
            total += np.sum(convolution==-3) * -1
        return total

class MinimaxABController(MinimaxController):
    def move(self):
        """
        Performs a move using minimax
        """
        self._board.place_token(self.minimax(self.depth, self._board, \
        -99999999999, 9999999999, self.red)[1])

    def minimaxAB(self, depth, gamestate, alpha, beta, maximize):
        """
        depth: an int that describes the maximum look depth

        gamestate: an instance of ConnectFour

        maximize: a bool representing the maximizing (True) or minimizing (False) player. 
        """
        if depth == 0 or gamestate.check_win() != 0:
            return self.static_eval(gamestate), 0
        children = [gamestate.create_child(i) for i in range(7)]
        best = 0, -1
        if maximize:
            # such readable much wow
            # TODO: Investigate draw states
            for i, child in enumerate(children):
                if child is not None:
                    score = self.minimaxAB(depth - 1, child, not maximize)[0]
                    if score > best[0] or best[1] == -1:
                        best = score, i
                    alpha = max(alpha, best[0])
                    if beta <= alpha:
                        break
        else:
            for i, child in enumerate(children):
                if child is not None:
                    score = self.minimaxAB(depth - 1, child, not maximize)[0]
                    if score < best[0] or best[1] == -1:
                        best = score, i
                    beta = min(beta, best[0])
                    if beta <= alpha:
                        break
        return best



