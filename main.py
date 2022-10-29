"""
Main run script
"""

from model import ConnectFour
from view import TextView
from controller import PlayerController, MinimaxController


def main():
    """
    The main algorithm for Connect Four
    """

    # Initialize MVC
    board = ConnectFour()
    view = TextView(board)
    p1 = PlayerController(board, True)
    p2 = MinimaxController(board, False)

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


if __name__ == '__main__':
    main()
