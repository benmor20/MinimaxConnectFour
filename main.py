"""
Main run script
"""
import itertools

from model import ConnectFour
from view import TextView
from controller import PlayerController, MinimaxController
from minimax import Tree, _minimax
import networkx as nx
import matplotlib.pyplot as plt


def main():
    """
    The main algorithm for Connect Four
    """

    # # Initialize MVC
    # board = ConnectFour()
    # view = TextView(board)
    # p1 = PlayerController(board, True)
    # p2 = MinimaxController(board, False)
    #
    # view.draw()
    # while True:
    #     # P1 Move
    #     p1.move()
    #     view.draw()
    #     if board.check_win() == 1:
    #         break
    #
    #     # P2 Move
    #     p2.move()
    #     view.draw()
    #     if board.check_win() == -1:
    #         break

    board = ConnectFour()
    tree = Tree(board)
    _minimax(2, board, None, True, tree)
    tree.display()


if __name__ == '__main__':
    main()
