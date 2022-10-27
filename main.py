from model import ConnectFour
from view import ConnectFourView
from controller import PlayerController


def main():
    board = ConnectFour()
    view = ConnectFourView(board)
    p1 = PlayerController(board, True)
    p2 = PlayerController(board, False)

    view.print_board()
    while True:
        p1.move()
        view.print_board()

        if board.check_win() == 1:
            print('Player 1 Won!')
            break

        p2.move()
        view.print_board()

        if board.check_win() == -1:
            print('Player 2 Won!')
            break


if __name__ == '__main__':
    main()
