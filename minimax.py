"""
Module that implements the Minimax algorithm
"""

from model import ConnectFour, WIN_KERNELS
from scipy import signal
import numpy as np
from typing import *


def minimax(depth: int, gamestate: ConnectFour, maximize: bool) -> int:
    """
    Performs the minimax algorithm on the current gamestate

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :return: The optimal column to play according to minimax
    """
    return _minimax(depth, gamestate, None, maximize)[1]


def minimaxab(depth: int, gamestate: ConnectFour, alpha: int, beta: int, maximize: bool) -> int:
    """
    Performs the minimax algorithm on a given gamestate, with Alpha-Beta pruning

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param alpha: the Alpha parameter for AB pruning
    :param beta: the Beta parameter for AB pruning
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :return: The optimal column to play according to minimax with AB pruning
    """
    return _minimax(depth, gamestate, (alpha, beta), maximize)[1]


def _minimax(depth: int, gamestate: ConnectFour, ab: Optional[Tuple[int, int]], maximize: bool) -> Tuple[int, int]:
    """
    Performs the minimax algorithm on a given gamestate, with Alpha-Beta pruning

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param ab: a tuple containing the alpha and beta parameters for AB pruning, or None to perform regular minimax
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :return: A tuple of ints containing first the score then the column to get that score.
    """
    # Base case - reached minimum depth or someone has won
    if depth == 0 or gamestate.check_win() != 0:
        return static_eval(gamestate), 0

    # Generate all possible next moves
    children = [gamestate.create_child(i) for i in range(7)]
    best = 0, -1

    # For each child, perform minimax
    for i, child in enumerate(children):
        if child is not None:
            score = _minimax(depth - 1, child, ab, not maximize)[0]
            # If the score is less or we are trying to maximize (but not both) then found new good score
            # Or if best[1] is -1, then this is our first run and we need to set it
            if (score < best[0] ^ maximize) or best[1] == -1:
                best = score, i

            # Alpha-Beta pruning
            if ab is not None:
                alpha, beta = ab
                if maximize:
                    alpha = max(alpha, best[0])
                else:
                    beta = min(beta, best[0])
                ab = alpha, beta
                if beta < alpha:
                    break
    return best


def static_eval(gamestate: ConnectFour) -> int:
    """
    Calculates a score for the current game state

    :param gamestate: an instance of ConnectFour to evaluate
    :return: an int, the score for the state
    """
    total = 0
    for kernel in WIN_KERNELS:
        convolution = signal.convolve2d(gamestate.board, kernel, mode="valid")
        total += np.sum(convolution == 4) * 100000000
        total += np.sum(convolution == 3) * 1
        total += np.sum(convolution == -4) * -100000000
        total += np.sum(convolution == -3) * -1
    return total
