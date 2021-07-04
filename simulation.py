import copy
import os

from config import *
from function import *
from mcts import *
from othello import *
from player import *

GAME_NUM = 20
BLACK_WIN_CNT = 0
WHITE_WIN_CNT = 0
DRAW_CNT = 0

OUTPUT_LOG = './result/random_mcts.txt'

if __name__ == '__main__':
  # Simulate mcts othello ai performance
  # black : random walk
  # white : mcts moving

  # open log file
  
  with open(OUTPUT_LOG, 'w') as output:

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
          output.write(f"black : {black}, white : {white}\n")
          print(f"black : {black}, white : {white}")
          if black == white:  DRAW_CNT += 1
          elif black > white: BLACK_WIN_CNT += 1
          elif black < white: WHITE_WIN_CNT += 1

          break

        # player turn
        elif current_game.turn is BLACK:
          ret, current_game = randomPlayer(current_game)

        # computer turn
        elif current_game.turn is WHITE:
          ret, current_game = MCTSPlayer(tree, current_game)
          # ret, current_game = heuristicPlayer(current_game)

        # recompute turn_pass
        turn_pass = turn_pass * ret + ret

      if (i+1) % 10 == 0:
        output.write(f"{i+1}th iteration - RANDOM({BLACK_WIN_CNT}) : HEURISTIC({WHITE_WIN_CNT}) , DRAW({DRAW_CNT})\n")
        print(f"{i+1}th iteration - RANDOM({BLACK_WIN_CNT}) : HEURISTIC({WHITE_WIN_CNT}) , DRAW({DRAW_CNT})")

      del(current_game)
      del(tree)