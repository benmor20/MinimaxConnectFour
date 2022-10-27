from model import ConnectFour
from view import ConnectFourView
from controller import PlayerController, MinimaxController


def main():
    board = ConnectFour()
    view = ConnectFourView(board)
    p1 = PlayerController(board, True)
    p2 = MinimaxController(board, False)

    view.draw()
    while True:
        p1.move()
        view.draw()

        if board.check_win() == 1:
            print('Player 1 Won!')
            break

        p2.move()
        view.draw()

        if board.check_win() == -1:
            print('Player 2 Won!')
            break


if __name__ == '__main__':
    main()
