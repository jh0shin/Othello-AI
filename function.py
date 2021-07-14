from config import *

#========================================================
#                    Functions
#========================================================

def drawboard(node):
  # board : othello game board with black and white and empty
  print(BOARD_HEADLINE)
  print(BOARD_LINE)
  for x in range(8):
    line = f' {x} |'
    for y in range(8):
      if (x, y) in node.available: line += ' \u26AC |'
      elif node.board[x][y] == 0: line += '   |'
      elif node.board[x][y] == -1: line += '\u274C |'
      elif node.board[x][y] == BLACK: line += '\u26AB |'
      elif node.board[x][y] == WHITE: line += '\u26AA |'
      # elif node.board[x][y] == -1: line += ' \u2716 |'
      # elif node.board[x][y] == BLACK: line += ' \u25CF |'
      # elif node.board[x][y] == WHITE: line += ' \u25CB |'
    print(line)
    print(BOARD_LINE)

def endWithResult(current_game):
  # end game with printing game result
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