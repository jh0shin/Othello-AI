import random
import copy

from config import *
    
#========================================================
#                    MCTS Functions
#========================================================

def selection(tree, node):
  # tree  : dictionary (Hash table)
  # node  : Node class

  # Select child node with UCT(Upper Confidence Bound 1 applied to Trees)
  max_uct = -1
  max_uct_node = None

  if node.available != []:
    # if there is path that never has been visited,
    # expand to that path
    rand = random.randint(0, len(node.available) - 1)
    expansion(tree, node, node.available[rand])
    node.available.pop(rand)
  elif node not in tree.keys():
    return
    # TODO : game end implementation
  else:
    # if there is no path that never has been visited,
    # select between child with UCT value.
    for child in tree[node]:
      uct = child.w / (child.n + 1) + UCT_C * math.sqrt(math.log(node.n + 1)/(child.n + 1))
      if uct > max_uct:
        max_uct = uct
        max_uct_node = child
        
    # recursive selection call with maximum UCT node
    selection(tree, max_uct_node)
    

def expansion(tree, node, pos):
  # tree  : dictionary (Hash table)
  # node  : Node class
  # pos   : next action position

  # deepcopy child node
  child = copy.deepcopy(node)
  child.move(pos)
  if node not in tree.keys():
    tree[node] = [child]
  else:
    tree[node].append(child)

  simulation(tree, child)

def simulation(tree, node):
  # take random possible path without record
  # node  : Node class

  # local variables
  black = 0
  white = 0

  # deepcopy node for preserve original
  node_dc = copy.deepcopy(node)

  # go to random path until no available path left
  # (game ends)
  while node_dc.available != []:
    rand = random.randint(0, len(node_dc.available) - 1)
    node_dc.move(node_dc.available[rand])

  # when game ends
  for row in node_dc.board:
    black += row.count(BLACK)
    white += row.count(WHITE)

  # backpropagation call
  if black == white:
    backpropagation(tree, DRAW, node)
  elif black > white:
    backpropagation(tree, BLACK_WIN, node)
  elif black < white:
    backpropagation(tree, WHITE_WIN, node)

def backpropagation(tree, result, node):
  # result  : game simulation result
  # node    : Node class

  # count variable
  if result != node.turn: # TODO : check this
    node.w += 1
  node.n += 1

  parent = [parent_node
              for parent_node, child_node in tree.items()
                if child_node == node]

  if parent == []: return
  else: backpropagation(tree, result, parent[0])