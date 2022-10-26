import numpy as np
from scipy import signal


WIN_KERNELS = [np.eye(4, dtype=int),
               np.flip(np.eye(4, dtype=int),1),
               np.ones((4,1) dtype=int),
               np.ones((1,4) dtype=int)]

class ConnectFour:
    """
    Player starts off red, models board plays and wins


    get_board_state: passes matrix which has 1s for red, -1s for blue, 0 
    otherwise. Board is int datatypes

    place_token:
    Places the current color token (hopefully) properly on the board
    and swtitches turn if it can in the given column.


    """
    def __init__(self):
        self.board = np.zeros((5,7), dtype=int)
        self.is_red = True
        self.turn_count = 0


    def get_board_state(self):
        return self.board
    
    def get_is_red(self):
        return self.is_red
    
    def get_turn_count(self):
        return self.get_turn_count

    def place_token(self, column):
        row_spaces = self.board[column]==0
        if 1 in row_spaces:
            top_pos = np.where(row_spaces)[-1]
            self.board[column, top_pos] = -1*not self.is_red + self.is_red
            self.is_red = not self.is_red
            self.turn_count += 1

        else:
            #Illegal move
            pass
            
    def check_win(self):
        # Checks if current color has won
        for kernel in WIN_KERNELS:
            convolution = signal.convolve2d(self.board,kernel)
            if (4*self.is_red + -4*self.is_red) in convolution:
                return True

        return False