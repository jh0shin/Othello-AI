import math
import copy
import time

from config import *
from function import *
from mcts import *
from othello import *
    
if __name__ == '__main__':
  print('Othello')
  print('BLACK : PLAYER / WHITE : COMPUTER')

  # initial settings
  tree = copy.deepcopy(TREE)
  current_game = Node(INIT_BOARD)
  turn_pass = 0                   # if pass turn sequentially twice, game ends

  # game turn
  while 1:
    drawboard(current_game)

    # pass*2 - game ends
    if turn_pass >= 2:
      black = 0
      white = 0

      # when game ends
      for row in current_game.board:
        black += row.count(BLACK)
        white += row.count(WHITE)

      # print game result
      print("Game ends !")
      print(f"BLACK ({black}) : WHITE ({white}) ; ", end='')
      if black == white:  print("DRAW !")
      elif black > white: print("BLACK WIN !")
      elif black < white: print("WHITE WIN !")

      break

    # player turn
    elif current_game.turn is BLACK:
      print("BLACK TURN")

      # no available place
      if current_game.available == []:
        turn_pass += 1

        current_game.passturn()
      
      else:
        # init turn_pass
        turn_pass = 0

        # get next pos input from user
        while 1:
          print('Enter next position: ex) 3, 2')
          x, y = map(int, input().split(','))
          if (x, y) in current_game.available:
            break
          else: # invalid input
            print('Invalid input encountered')
        
        # move to next pos
        current_game.move((x, y))

    # computer turn
    elif current_game.turn is WHITE:
      print("WHITE TURN")

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
      print(f"compute {it_cnt} times")

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