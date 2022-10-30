"""
Main run script to play against the AI
"""
import itertools

from model import ConnectFour
from view import TextView
from controller import PlayerController, MinimaxController, MinimaxABController


def main():
    """
    The main algorithm for Connect Four
    """

    # Initialize MVC
    board = ConnectFour()
    view = TextView(board)
    p1 = MinimaxABController(board, True)
    p2 = MinimaxABController(board, False)

    view.draw()
    while True:
        # P1 Move
        p1.move()
        view.draw()
        if board.check_win() == 1:
            break

        # P2 Move
        p2.move()
        view.draw()
        if board.check_win() == -1:
            break

        if board.turn_count == 42:
            break

    print(f'P1 had {p1.total_calls} calls, P2 has {p2.total_calls} calls')


if __name__ == '__main__':
    main()
