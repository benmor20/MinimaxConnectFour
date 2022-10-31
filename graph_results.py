"""
Run the algorithm against itself and graph speed results
"""
import os

from model import ConnectFour
from controller import MinimaxController, MinimaxABController
import json


def main():
    folder = '\\'.join(__file__.split('\\')[:-1])
    filepath = '\\'.join((folder, 'game_results.json'))
    with open(filepath, 'r') as file:
        results = json.load(file)

    for d in range(7, 8):
        results[d] = {}
        print(f'Running regular game with a depth of {d}')

        # Initialize model and controllers
        board = ConnectFour()
        p1 = MinimaxController(board, True, depth=d)
        p2 = MinimaxController(board, False, depth=d)

        # Play game
        while board.turn_count < 42:
            p1.move()
            if board.check_win() == 1:
                break
            p2.move()
            if board.check_win() == -1:
                break

        # Save results
        results[d]['regular_count'] = p1.total_calls + p2.total_calls
        results[d]['regular_winner'] = board.check_win()
        results[d]['regular_turns'] = board.turn_count
        results[d]['regular_board'] = int(board)

        print(f'Running a AB game with a depth of {d}')
        # Re-init for AB version
        board = ConnectFour()
        p1 = MinimaxABController(board, True, depth=d)
        p2 = MinimaxABController(board, False, depth=d)

        # Re-run game with AB version
        while board.turn_count < 42:
            p1.move()
            if board.check_win() == 1:
                break
            p2.move()
            if board.check_win() == -1:
                break

        # Save results
        results[d]['ab_count'] = p1.total_calls + p2.total_calls
        results[d]['ab_winner'] = board.check_win()
        results[d]['ab_turns'] = board.turn_count
        results[d]['ab_board'] = int(board)

    with open(filepath, 'w') as file:
        json.dump(results, file)


if __name__ == '__main__':
    main()
