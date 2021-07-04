import copy

from config import *
from function import *
from mcts import *
from othello import *
from player import *
    
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
      endWithResult(current_game)
      break

    # player turn
    elif current_game.turn is BLACK:
      print("BLACK TURN")
      ret, current_game = interactPlayer(current_game)

    # computer turn
    elif current_game.turn is WHITE:
      print("WHITE TURN")
      ret, current_game = MCTSPlayer(tree, current_game)

    # recompute turn_pass
    turn_pass = turn_pass * ret + ret