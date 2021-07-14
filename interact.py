import copy

from config import *
from function import *
from mcts import *
from othello import *
from player import *
    
if __name__ == '__main__':
  print('Othello')
  print('BLACK : PLAYER / WHITE : COMPUTER')

  print('SELECT MODE (NONE / BLOCK) : ', end='')
  othello_mode = input()

  if othello_mode == 'BLOCK':
    # Setting for BLOCK mode

    # get block position from user input
    blocks = []
    while len(blocks) < 5:
      try:
        print('Enter block position - ex) 3 5 : ', end='')
        x, y = map(int, input().split(' '))
        blocks.append((x, y))
      except:
        print('Wrong input encountered')
        exit()

    # create blocked board
    board_blocked = copy.deepcopy(INIT_BOARD)
    for block in blocks:
      board_blocked[block[0]][block[1]] = -1

    current_game = Node(board_blocked)

  else:
    # Setting for NON-BLOCK mode
    current_game = Node(INIT_BOARD)

  # Common initial settings
  tree = copy.deepcopy(TREE)
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