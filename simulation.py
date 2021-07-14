import copy
import random

from config import *
from function import *
from mcts import *
from othello import *
from player import *

GAME_NUM = 100
BLACK_WIN_CNT = 0
WHITE_WIN_CNT = 0
DRAW_CNT = 0

IS_BLOCKED = False

OUTPUT_LOG = './result/mcts_random_100.txt'

if __name__ == '__main__':
  # Simulate mcts othello ai performance
  # black : random walk
  # white : mcts moving

  # open log file
  
  with open(OUTPUT_LOG, 'w') as output:

    for i in range(GAME_NUM):
      # initial settings
      tree = copy.deepcopy(TREE)
      if IS_BLOCKED:
        # get random block position
        blocks = []
        while len(blocks) < 5:
          x, y = random.randint(0, 7), random.randint(0, 7)
          if (x, y) not in blocks and (x, y) not in NOT_ALLOWED_BLOCKS:
            blocks.append((x, y))

        # create blocked board
        board_blocked = copy.deepcopy(INIT_BOARD)
        for block in blocks:
          board_blocked[block[0]][block[1]] = -1

        output.write(f"{blocks}\n")
        print(blocks)

        current_game = Node(board_blocked)
      else:
        current_game = copy.deepcopy(Node(INIT_BOARD))
      
      # if pass turn sequentially twice, game ends
      turn_pass = 0 

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
          # ret, current_game = heuristicPlayer(current_game)
          # ret, current_game = randomPlayer(current_game)
          ret, current_game = MCTSPlayer(tree, current_game)

        # computer turn
        elif current_game.turn is WHITE:
          # ret, current_game = MCTSPlayer(tree, current_game)
          ret, current_game = randomPlayer(current_game)
          # ret, current_game = heuristicPlayer(current_game)

        # recompute turn_pass
        turn_pass = turn_pass * ret + ret

      if (i+1) % 10 == 0:
        output.write(f"{i+1}th iteration - MCTS({BLACK_WIN_CNT}) : RANDOM({WHITE_WIN_CNT}) , DRAW({DRAW_CNT})\n")
        print(f"{i+1}th iteration - MCTS({BLACK_WIN_CNT}) : RANDOM({WHITE_WIN_CNT}) , DRAW({DRAW_CNT})")

      del(current_game)
      del(tree)