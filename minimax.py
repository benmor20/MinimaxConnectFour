"""
Module that implements the Minimax algorithm
"""

from model import ConnectFour, WIN_KERNELS
from scipy import signal
import numpy as np
from typing import *


def minimax(depth: int, gamestate: ConnectFour, maximize: bool) -> Tuple[int, int]:
    """
    Performs the minimax algorithm on the current gamestate

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :return: A tuple of ints containing first the score then the column to get that score.
    """
    if depth == 0 or gamestate.check_win() != 0:
        return static_eval(gamestate), 0
    children = [gamestate.create_child(i) for i in range(7)]
    best = 0, -1
    if maximize:
        # such readable much wow
        # TODO: Investigate draw states
        for i, child in enumerate(children):
            if child is not None:
                score = minimax(depth - 1, child, not maximize)[0]
                if score > best[0] or best[1] == -1:
                    best = score, i
    else:
        for i, child in enumerate(children):
            if child is not None:
                score = minimax(depth - 1, child, not maximize)[0]
                if score < best[0] or best[1] == -1:
                    best = score, i
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




def minimaxAB(depth: int, gamestate: ConnectFour, alpha:int, beta:int, maximize: bool) -> Tuple[int, int]:
    """
    depth: an int that describes the maximum look depth

    gamestate: an instance of ConnectFour

    maximize: a bool representing the maximizing (True) or minimizing (False) player. 
    """
    if depth == 0 or gamestate.check_win() != 0:
        return static_eval(gamestate), 0
    children = [gamestate.create_child(i) for i in range(7)]
    best = 0, -1
    if maximize:
        # such readable much wow
        # TODO: Investigate draw states
        for i, child in enumerate(children):
            if child is not None:
                score = minimaxAB(depth - 1, child, not maximize)[0]
                if score > best[0] or best[1] == -1:
                    best = score, i
                alpha = max(alpha, best[0])
                if beta <= alpha:
                    break
    else:
        for i, child in enumerate(children):
            if child is not None:
                score = minimaxAB(depth - 1, child, not maximize)[0]
                if score < best[0] or best[1] == -1:
                    best = score, i
                beta = min(beta, best[0])
                if beta <= alpha:
                    break
    return best