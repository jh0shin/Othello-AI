import math
import copy
import time

from config import *
from function import *
from mcts import *
from othello import *

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

      # RANDOM WALK
      elif current_game.turn is BLACK:

        # no available place
        if current_game.available == []:
          turn_pass += 1

          current_game.passturn()
        
        else:
          # init turn_pass
          turn_pass = 0

          # select random next pos
          rand = random.randint(0, len(current_game.available) - 1)
          x, y = current_game.available[rand]
          
          # move to next pos
          current_game.move((x, y))

      # MCTS
      elif current_game.turn is WHITE:

        # Select next child node with UCT(Upper Confidence Bound 1 applied to Trees)
        max_uct = -1
        next_turn = None

        # # MCTS - max iteration version
        # for _ in range(SIMUL_K):
        #   selection(tree, current_game)

        # MCTS - max compute time version
        time_limit = time.time() + SIMUL_TIMEOUT
        it_cnt = 0
        while time.time() < time_limit and it_cnt < SIMUL_N:
          selection(tree, current_game)
          it_cnt += 1

        if current_game not in tree.keys():
          turn_pass += 1

          current_game.passturn()

        else:
          # init turn_pass
          turn_pass = 0

          # select between child with max UCT value.
          for child in tree[current_game]:
            uct = child.w / (child.n + 1) + UCT_C * math.sqrt(math.log(current_game.n + 1)/(child.n + 1))
            if uct > max_uct:
              max_uct = uct
              next_turn = child

          # move to next pos
          current_game = copy.deepcopy(next_turn)
          current_game.nextposition()

    if (i+1) % 10 == 0:
      print(f"{i+1}th iteration - RANDOM({BLACK_WIN_CNT}) : MCTS({WHITE_WIN_CNT}) , DRAW({DRAW_CNT})")

    del(current_game)
    del(tree)