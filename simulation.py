import math
import copy
import time

from config import *
from function import *
from mcts import *
from othello import *
from player import *

GAME_NUM = 100
BLACK_WIN_CNT = 0
WHITE_WIN_CNT = 0
DRAW_CNT = 0


if __name__ == '__main__':
  # Simulate mcts othello ai performance
  # black : random walk
  # white : mcts moving

  for i in range(GAME_NUM):
    # initial settings
    tree = copy.deepcopy(TREE)
    current_game = copy.deepcopy(Node(INIT_BOARD))
    turn_pass = 0                   # if pass turn sequentially twice, game ends

    # game turn
    while 1:

      # pass*2 - game ends
      if turn_pass >= 2:
        black = 0
        white = 0

        # when game ends
        for row in current_game.board:
          black += row.count(BLACK)
          white += row.count(WHITE)

        # print game result
        print(f"black : {black}, white : {white}")
        if black == white:  DRAW_CNT += 1
        elif black > white: BLACK_WIN_CNT += 1
        elif black < white: WHITE_WIN_CNT += 1

        break

      # player turn
      elif current_game.turn is BLACK:
        print("BLACK TURN")
        ret, current_game = randomPlayer(current_game)

      # computer turn
      elif current_game.turn is WHITE:
        print("WHITE TURN")
        ret, current_game = MCTSPlayer(tree, current_game)

      # recompute turn_pass
      turn_pass = turn_pass * ret + ret

    del(current_game)
    del(tree)