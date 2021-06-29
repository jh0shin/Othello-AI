import random
import time

from config import *
from mcts import *

def interactPlayer(current_game):
  # get next position from user
  # return 1 if turn_pass and 0 if not turn_pass
  # no available place
  if current_game.available == []:
    current_game.passturn()

    return 1, current_game
  
  else:
    # get next pos input from user
    while 1:
      try:
        print('Enter next position: ex) 3, 2')
        x, y = map(int, input().split(','))
        if (x, y) in current_game.available:
          break
        else: # invalid input
          print('Invalid input encountered')
      except:
        print('Invalid input encountered')
    
    # move to next pos
    current_game.move((x, y))

    return 0, current_game

def randomPlayer(current_game):
  # completely random walk path selecting
  # return 1 if turn_pass and 0 if not turn_pass

  # no available place
  if current_game.available == []:
    current_game.passturn()
    return 1, current_game
  
  else:
    # select random next pos
    rand = random.randint(0, len(current_game.available) - 1)
    x, y = current_game.available[rand]
    
    # move to next pos
    current_game.move((x, y))

    return 0, current_game

def MCTSPlayer(tree, current_game):
  # MCTS based player
  # return 1 if turn_pass and 0 if not turn_pass

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
    current_game.passturn()

    return 1, current_game

  else:
    # select between child with max UCT value.
    for child in tree[current_game]:
      uct = child.w / (child.n + 1) + UCT_C * math.sqrt(math.log(current_game.n + 1)/(child.n + 1))
      if uct > max_uct:
        max_uct = uct
        next_turn = child

    # move to next pos
    current_game = copy.deepcopy(next_turn)
    current_game.nextposition()

    return 0, current_game

def heuristicPlayer(current_game):
  # MCTS based player
  # return 1 if turn_pass and 0 if not turn_pass

  # no available place
  if current_game.available == []:
    current_game.passturn()
    return 1, current_game
  
  else:
    # init
    max_heuristic = -99999
    next_x, next_y = 0, 0

    # select maximum heuristic value child
    for x, y in current_game.available:
      child = copy.deepcopy(current_game)
      child.move((x, y))

      heuristic = 0
      for i in range(8):
        for j in range(8):
          if child.turn == child.board[i][j]:
            heuristic += HEURISTIC_WEIGHT[i][j]
      
      if heuristic > max_heuristic:
        max_heuristic = heuristic
        next_x, next_y = x, y
    
    # move to next pos
    current_game.move((next_x, next_y))

    return 0, current_game