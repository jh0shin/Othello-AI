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

NOT_ALLOWED_BLOCKS = [(3, 3), (3, 4),
                      (4, 3), (4, 4)]

# game result
BLOCK = -1
DRAW = 0
BLACK_WIN = 1
WHITE_WIN = 2

# Constants
UCT_C = math.sqrt(2)
SIMUL_N = 100        # number of iteration
SIMUL_K = 10         # number of simulation
SIMUL_TIMEOUT = 5    # simulation max compute time

# expansion args
EXPANSION_NEW = 0     # add new node
EXPANSION_APPEND = 1  # add new path

# heuristic weight
HEURISTIC_WEIGHT = [[100, -20, 10,  5,  5, 10, -20, 100],
                    [-20, -50, -2, -2, -2, -2, -50, -20],
                    [ 10,  -2, -1, -1, -1, -1,  -2,  10],
                    [  5,  -2, -1, -1, -1, -1,  -2,   5],
                    [  5,  -2, -1, -1, -1, -1,  -2,   5],
                    [ 10,  -2, -1, -1, -1, -1,  -2,  10],
                    [-20, -50, -2, -2, -2, -2, -50, -20],
                    [100, -20, 10,  5,  5, 10, -20, 100],]