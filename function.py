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
      elif node.board[x][y] == BLACK: line += '\u26AB |'
      elif node.board[x][y] == WHITE: line += '\u26AA |'
      # elif node.board[x][y] == BLACK: line += ' \u25CF |'
      # elif node.board[x][y] == WHITE: line += ' \u25CB |'
    print(line)
    print(BOARD_LINE)