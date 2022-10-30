"""
Module to hold the model of the ConnectFour game
"""

import numpy as np
from scipy import signal
from typing import *


# The kernels used in convolution to identify wins
WIN_KERNELS = [np.eye(4, dtype=int),
               np.flip(np.eye(4, dtype=int), 1),
               np.ones((4, 1), dtype=int),
               np.ones((1, 4), dtype=int)]


class ConnectFour:
    """
    Internal model of the Connect Four game, storing board state, player turn, and turn count

    Attributes:
        board: a 6x7 ndarray of 0, 1, and -1. 0: empty. 1: P1: -1: P2
        is_red: a bool, whether the next player to play should be P1
        turn_count: an int, the number of elapsed turns
    """
    def __init__(self):
        """
        Initialize a Connect Four game from the beginning
        """
        self.board = np.zeros((6, 7), dtype=int)
        self.is_red = True
        self.turn_count = 0

    def get_board_state(self) -> np.ndarray:
        """
        :return: a 6x7 ndarray, the current state of the board
        """
        return self.board
    
    def get_is_red(self) -> bool:
        """
        :return: a bool, whether the next player to play should be P1
        """
        return self.is_red
    
    def get_turn_count(self) -> int:
        """
        :return: an int, the number of elapsed turns
        """
        return self.turn_count

    def place_token(self, column: int) -> bool:
        """
        Performs one turn by placing a token in the given column

        :param column: an int between 0 and 6, the column to place the token
        :return: a bool, whether the move was valid (False if the column was full)
        :raises: ValueError if the given column is out of bounds
        """
        if column < 0 or column > 6:
            raise ValueError(f'Column out of bounds. Expected between 0 and 6 (inclusive), received {column}.')

        # Find the empty spaces in the column
        row_spaces = self.board[:, column] == 0

        if 1 in row_spaces:
            # If there is an empty space, find the bottomost one (new top)
            top_pos = np.where(row_spaces)[0][-1]

            # Set the new top to the correct color
            self.board[top_pos, column] = 1 if self.is_red else -1

            # Update tracking variables
            self.is_red = not self.is_red
            self.turn_count += 1
            return True
        # Illegal move - no empty spaces in the column
        return False

    def copy(self) -> 'ConnectFour':
        """
        Create a copy of this game state
        :return: A copy of this ConnectFour state
        """
        copy = ConnectFour()
        copy.board = self.board.copy()
        copy.is_red = self.is_red
        copy.turn_count = self.turn_count
        return copy

    def create_child(self, column: int) -> Optional['ConnectFour']:
        """
        Create a new model with an extra token placed in the given column.

        :param column: an int, the column to place a new token, between 0 and 6 inclusive
        :return: a copy of this game with the performed move, or None if the move is not possible
        :raise: ValueError if the given column is out of bounds
        """
        # Copy the current state
        child = self.copy()

        # If we can place a token in the column, return the child
        if child.place_token(column):
            return child

        # Else return none
        return None

    def check_win(self) -> int:
        """
        Finds if a player has won

        :return: 1 if P1 won, -1 if P2 won, or 0 if there is no winner yet
        """
        for kernel in WIN_KERNELS:
            convolution = signal.convolve2d(self.board,kernel, mode="valid")
            if 4 in convolution:
                return 1
            elif -4 in convolution:
                return -1
        return 0

    def __hash__(self) -> int:
        """
        :return: an int, the hash for this board state
        """
        total = 0
        for col in range(self.board.shape[1]):
            col_total = 0
            for row in range(self.board.shape[0]):
                if self.board[row, col] == 0:
                    continue
                col_total *= 2
                col_total += 0 if self.board[row, col] == 1 else 1
            total *= 2 ** 7 - 1
            total += col_total
        return total

    def __int__(self) -> int:
        """
        :return: an integer representation of this board, equivalent to __hash__
        """
        return hash(self)
