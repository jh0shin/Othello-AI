import math

#========================================================
#                    Settings
#========================================================

# initial monte carlo tree
TREE = {}

# board cell status
EMPTY = 0
BLACK = 1
WHITE = 2

# board init
INIT_BOARD = [[EMPTY for _ in range(8)] for _ in range(8)]
INIT_BOARD[3][4] = BLACK
INIT_BOARD[4][3] = BLACK
INIT_BOARD[3][3] = WHITE
INIT_BOARD[4][4] = WHITE

DIRECTION = [(-1, -1), (-1, 0), (-1, 1),
             ( 0, -1),          ( 0, 1),
             ( 1, -1), ( 1, 0), ( 1, 1)]

BOARD_HEADLINE  = '     0   1   2   3   4   5   6   7  '
BOARD_LINE      = '   +---+---+---+---+---+---+---+---+'

# game result
DRAW = 0
BLACK_WIN = 1
WHITE_WIN = 2

# Constants
UCT_C = math.sqrt(2)
SIMUL_K = 10000       # simulation iteration
SIMUL_TIMEOUT = 5    # simulation max compute time

# expansion args
EXPANSION_NEW = 0     # add new node
EXPANSION_APPEND = 1  # add new path