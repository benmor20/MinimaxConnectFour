from model import ConnectFour
from view import ConnectFourView
from controller import PlayerController


def main():
    board = ConnectFour()
    view = ConnectFourView(board)
    p1 = PlayerController(board, 1)
    p2 = PlayerController(board, 2)

    while True:
        view.print_board()
        p1.move()

        if board.player_won() == 1:
            print('Player 1 Won!')
            break

        view.print_board()
        p2.move()

        if board.player_won() == 1:
            print('Player 1 Won!')
            break


if __name__ == '__main__':
    main()
