from config import *

#========================================================
#                    Classes
#========================================================

class MonteCarloTreeSearch:
  def __init__(self):
    self.tree = {}

class Node:
  def __init__(self, board):
    self.w = 0          # winning case (w_i)
    self.n = 0          # visit case (n_i)
    self.turn = BLACK   # next player turn (black first)
    self.board = board  # othello board
    self.available = []  # available next board position list

    self.nextposition()

  def nextposition(self):
    # find all available next positions
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == self.turn:
          for d in DIRECTION:
            cnt = 0
            xpos, ypos = i+d[0], j+d[1]
            while xpos in range(0, 8) and ypos in range(0, 8):
              # Same color encounter  (break)
              if self.board[xpos][ypos] == self.turn:
                break
              # Other color encounter (valid)
              elif self.board[xpos][ypos] == 3 - self.turn:
                cnt += 1
                xpos, ypos = xpos+d[0], ypos+d[1]
              # Empty block : available block
              elif cnt > 0:
                if (xpos, ypos) not in self.available:
                  self.available.append((xpos, ypos))
                break
              # Empty block : unavailable block
              else:
                break

  def move(self, pos):
    # move
    try:
      if self.board[pos[0]][pos[1]] != EMPTY:
        raise NotImplementedError
        # TODO : custom error implementation
      self.board[pos[0]][pos[1]] = self.turn
    except:
      print("Error occured in moving")

    # flip
    flip = []
    for d in DIRECTION:
      xpos, ypos = pos[0]+d[0], pos[1]+d[1]
      subflip = []
      while xpos in range(0, 8) and ypos in range(0, 8):
        ### print(d, xpos, ypos)
        # Other color encounter (flip)
        if self.board[xpos][ypos] == 3 - self.turn:
          ### print(f"flip {xpos} {ypos}")
          subflip.append((xpos, ypos))
          xpos, ypos = xpos+d[0], ypos+d[1]
        # Same color encouter   (start flip)
        elif self.board[xpos][ypos] == self.turn:
          for sub in subflip:
            flip.append(sub)
          break
        # Empty block encounter (discard subfilp)
        else:
          break
    
    for xpos, ypos in flip:
      self.board[xpos][ypos] = self.turn

    # change turn and init node logs
    self.w = 0
    self.n = 0
    self.turn = 3 - self.turn   # change turn
    self.available = []
    self.nextposition()         # get available positions

  def passturn(self):
    # pass turn
    self.w = 0
    self.n = 0
    self.turn = 3 - self.turn
    self.available = []
    self.nextposition()