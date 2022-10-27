import numpy as np
from scipy import signal


WIN_KERNELS = [np.eye(4, dtype=int),
               np.flip(np.eye(4, dtype=int),1),
               np.ones((4,1), dtype=int),
               np.ones((1,4), dtype=int)]

class ConnectFour:
    """
    Player starts off red. Models board plays and wins.

    Methods:
    get_board_state{}:
        Passes integer array which has 1s for red, -1s for blue, 0 
    otherwise. 

    place_token():
        If the column has space, places the current color token (hopefully)
    properly on the board and switches turn. Returns true if successful, false
    if illegal move.

    check_win():
        Returns 1 if red won, -1 if blue won, and 0 if nobody won
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
        return self.turn_count

    def place_token(self, column):
        row_spaces = self.board[:,column]==0
        if 1 in row_spaces:
            top_pos = np.where(row_spaces)[0][-1]
            self.board[top_pos, column] = -1*(not self.is_red) + self.is_red
            self.is_red = not self.is_red
            self.turn_count += 1
            return True
        else:
            #Illegal move
            print("Illegal Move")
            return False
            
    def check_win(self):
        # Checks if either color has won
        # Question: what datatype should this be?
        for kernel in WIN_KERNELS:
            convolution = signal.convolve2d(self.board,kernel, mode="valid")
            if 4 in convolution:
                return 1
            elif -4 in convolution:
                return -1
        return 0