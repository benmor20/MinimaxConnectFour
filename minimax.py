"""
Module that implements the Minimax algorithm
"""

from model import ConnectFour, WIN_KERNELS
from scipy import signal
import numpy as np
from typing import *
import networkx as nx
import matplotlib.pyplot as plt


class Tree:
    """
    Class to represent the tree-like structure of minimax

    Attributes:
        gamestate: the ConnectFour state this branch of the tree represents
        score: an int, the score of the gamestate, or None if no score is calculated
        children: a list of Trees, the possible children of this gamestate, each index corresponding to placing a token
            in the corresponding column.
    """
    def __init__(self, gamestate: ConnectFour, score: Optional[int] = None):
        self.gamestate = gamestate
        self.score = score
        self.children: List[Optional[Tree]] = [None for _ in range(self.gamestate.board.shape[1])]

    def nodes(self) -> Iterable['Tree']:
        """
        :return: a Generator of all the Trees at or below this, starting with self, then continuing depth-first
        """
        yield self
        for c in self.children:
            if c is not None:
                yield from c.nodes()

    def connect_graph(self, graph: nx.Graph):
        """
        Makes the connections in a networkx Graph between this node and its children

        :param graph: the Graph to make the connections on
        """
        for c in self.children:
            if c is not None:
                graph.add_edge(self, c)
                c.connect_graph(graph)

    def make_graph(self) -> nx.Graph:
        """
        Create a graph representing this tree

        :return: a Graph representation of this Tree, where each node is an instance of Tree
        """
        graph = nx.Graph()
        graph.add_nodes_from(self.nodes())
        self.connect_graph(graph)
        return graph

    def display(self):
        """
        Displays this tree
        """
        graph = self.make_graph()
        nx.draw(graph)
        plt.show()

    def __setitem__(self, key: int, value: 'Tree'):
        """
        Sets the given child to the given Tree

        :param key: an int, the index of the child to set
        :param value: a Tree, the value to set the child to
        """
        self.children[key] = value

    def __getitem__(self, item) -> Optional['Tree']:
        """
        Gets the given child

        :param item: an int, the index of the child to get
        :return: a Tree, the child at the given index
        """
        return self.children[item]


def minimax(depth: int, gamestate: ConnectFour, maximize: bool, make_tree: bool = False) -> int:
    """
    Performs the minimax algorithm on the current gamestate

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :param make_tree: a bool, whether to create and display the minimax Tree
    :return: The optimal column to play according to minimax
    """
    tree = Tree(gamestate) if make_tree else None
    column = _minimax(depth, gamestate, None, maximize, tree)[1]
    if make_tree:
        tree.display()
    return column


def minimaxab(depth: int, gamestate: ConnectFour, alpha: int, beta: int, maximize: bool, make_tree: bool = False)\
        -> int:
    """
    Performs the minimax algorithm on a given gamestate, with Alpha-Beta pruning

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param alpha: the Alpha parameter for AB pruning
    :param beta: the Beta parameter for AB pruning
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :param make_tree: a bool, whether to create and display the minimax Tree
    :return: The optimal column to play according to minimax with AB pruning
    """
    tree = Tree(gamestate) if make_tree else None
    column = _minimax(depth, gamestate, (alpha, beta), maximize, tree)[1]
    if make_tree:
        tree.display()
    return column


def _minimax(depth: int, gamestate: ConnectFour, ab: Optional[Tuple[int, int]], maximize: bool, tree: Optional[Tree])\
        -> Tuple[int, int]:
    """
    Performs the minimax algorithm on a given gamestate, with Alpha-Beta pruning

    :param depth: an int that describes the maximum look depth
    :param gamestate: an instance of ConnectFour
    :param ab: a tuple containing the alpha and beta parameters for AB pruning, or None to perform regular minimax
    :param maximize: a bool representing the maximizing (True) or minimizing (False) player.
    :param tree: the Tree of the given gamestate, or None to not create a Tree
    :return: A tuple of ints containing first the score then the column to get that score.
    """
    # Base case - reached minimum depth or someone has won
    if depth == 0 or gamestate.check_win() != 0:
        score = static_eval(gamestate)
        if tree is not None:
            tree.score = score
        return score, -1

    # Generate all possible next moves
    children = [gamestate.create_child(i) for i in range(7)]
    best = 0, -1

    # For each child, perform minimax
    for i, child in enumerate(children):
        if child is not None:
            if tree is not None:
                tree[i] = Tree(child)
            score = _minimax(depth - 1, child, ab, not maximize, None if tree is None else tree[i])[0]
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
    if tree is not None:
        tree.score = best[0]
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
