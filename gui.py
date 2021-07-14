import tkinter
import tkinter.ttk
import copy

from othello import *
from config import *
from player import *

#========================================================
#                  Default Settings
#========================================================
IS_BLOCKED = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900

GEOMETRY = "800x900"

COLUMN_WIDTH = 80
ROW_HEIGHT = 80

BOARD_SIZE = 8

GAME_TURN = ['', 'BLACK', 'WHITE']

#========================================================
#                         GUI
#========================================================
class GUI:
  def __init__(self):
    self._player = 'BLACK'
    self._ai = 'WHITE' if self._player == 'BLACK' else 'BLACK'
    self._tree = copy.deepcopy(TREE)
    self.current_game = Node(INIT_BOARD)
    self._turn_pass = 0

    # config
    self._mode = 'None'         # 0 if NONE / 1 if BLOCK
    self._blocks = [[-1, -1],
                    [-1, -1],
                    [-1, -1],
                    [-1, -1],
                    [-1, -1]]
    self._time_limit = 5

    self._root = tkinter.Tk()
    self._root.title("Reversi")
    self._root.geometry(GEOMETRY)

    # StringVar
    self._player_var = tkinter.StringVar()
    self._mode_var = tkinter.StringVar()
    self._blocks_var = []
    for _ in range(5):
      self._blocks_var.append((tkinter.StringVar(), tkinter.StringVar()))

    self._canvas = tkinter.Canvas(master = self._root, height = SCREEN_HEIGHT,
                                  width = SCREEN_WIDTH, background = 'green')
    self._canvas.pack(fill = tkinter.BOTH, expand = True)
    self._canvas.bind('<Configure>',self.draw_handler)

  def start(self):
    self._root.mainloop()

  def _restart(self):
    # save
    self._mode = self._mode_var.get()
    self._player = self._player_var.get()
    self._ai = 'WHITE' if self._player == 'BLACK' else 'BLACK'
    for i in range(5):
      self._blocks[i][0] = self._blocks_var[i][0].get()
      self._blocks[i][1] = self._blocks_var[i][1].get()

    # game board init
    self._tree = copy.deepcopy(TREE)

    # Non-block mode
    if self._mode == 'None':
      self.current_game = Node(INIT_BOARD)

    # Block mode
    else:
      board_blocked = copy.deepcopy(INIT_BOARD)
      for block in self._blocks:
        try:
          if int(block[0]) in range(0, 8) and int(block[1]) in range(0, 8):
            board_blocked[int(block[0])][int(block[1])] = -1
        except:
          pass

      self.current_game = Node(board_blocked)

    # redraw
    self.draw()


  def clicked(self,event: tkinter.Event):
    col = event.x // 80 - 1
    row = event.y // 80 - 1

    if (row, col) in self.current_game.available:
      self.current_game.move((row, col))
      self.draw()

  def _draw_board(self):
    for row in range(BOARD_SIZE):
      for col in range(BOARD_SIZE):
        col_start = (col+1) * COLUMN_WIDTH
        col_end = (col_start+1) + COLUMN_WIDTH
        row_start = (row+1) * ROW_HEIGHT
        row_end = (row_start+1) + ROW_HEIGHT
        self._canvas.create_rectangle(col_start, row_start, col_end, row_end)
        r = self._canvas.create_rectangle(col_start,row_start,col_end,row_end,fill = '#a0c3fa')

        # click activated only at player's turn
        if self._player == GAME_TURN[self.current_game.turn]:
          self._canvas.tag_bind(r, '<ButtonPress-1>', self.clicked)

        # draw disks
        if self.current_game.board[row][col] == BLACK:
          self._canvas.create_oval(col_start+5, row_start+5, col_end-5, row_end-5,
                                   width=2, fill='#000000', outline='#FFFFFF')
        elif self.current_game.board[row][col] == WHITE:
          self._canvas.create_oval(col_start+5, row_start+5, col_end-5, row_end-5,
                                   width=2, fill='#FFFFFF', outline='#000000')
        elif self.current_game.board[row][col] == BLOCK:
          self._canvas.create_rectangle(col_start,row_start,col_end,row_end,fill = '#663300')

    self._canvas.bind('<Configure>', self.draw_handler)

  def _config(self):
    gamemode_label = tkinter.Label(self._root, text="Game Mode", background='Green',
                                   fg='white')
    gamemode_label.place(x=20, y=730)
    gamemode_combo = tkinter.ttk.Combobox(self._root, values=["None", "Block"],
                                          state="readonly", textvariable=self._mode_var)
    gamemode_combo.current(0 if self._mode == 'None' else 1)
    gamemode_combo.place(x=20, y=750)

    player_turn_label = tkinter.Label(self._root, text="Player turn", background='Green',
                                   fg='white')
    player_turn_label.place(x=220, y=730)
    player_turn_combo = tkinter.ttk.Combobox(self._root, values=["BLACK", "WHITE"],
                                          state="readonly", textvariable=self._player_var)
    player_turn_combo.current(0 if self._player == 'BLACK' else 1)
    player_turn_combo.place(x=220, y=750)

    restart_button = tkinter.Button(self._root, width=15, command=self._restart,
                                    text='Restart')
    restart_button.place(x=420, y=750)

    blocks_input = []
    for i in range(5):
      blocks_input.append(
        tkinter.ttk.Entry(self._root, width = 3, textvariable=self._blocks_var[i][0])
      )
      blocks_input.append(
        tkinter.ttk.Entry(self._root, width = 3, textvariable=self._blocks_var[i][1])
      )
      blocks_input[i*2].place(x=20, y=790+i*20)
      blocks_input[i*2+1].place(x=60, y=790+i*20)

  def _turn(self):
    # no cell available
    if self.current_game.available == []:
      if self._turn_pass >= 2:
        pass
        # TODO : game end result
      
      else:
        self.current_game.passturn()
        self._turn_pass += 1
        self.draw()

    # available cell exists
    else:
      self._turn_pass = 0

      # player turn
      if self._player == GAME_TURN[self.current_game.turn]:
        # draw next available positions
        for av in self.current_game.available:
          col_start = (av[1]+1) * COLUMN_WIDTH
          col_end = (col_start+1) + COLUMN_WIDTH
          row_start = (av[0]+1) * ROW_HEIGHT
          row_end = (row_start+1) + ROW_HEIGHT

          self._canvas.create_oval(col_start+35, row_start+35, col_end-35, row_end-35,
                                  width=1, outline='#000000')

      # ai turn
      elif self._ai == GAME_TURN[self.current_game.turn]:
        # ret, self.current_game = randomPlayer(self.current_game)
        ret, self.current_game = MCTSPlayer(self._tree, self.current_game)
        self._turn_pass = self._turn_pass * ret + ret
        self.draw()
        
  def draw(self):
    self._canvas.delete(tkinter.ALL)
    self._draw_board()
    self._config()
    self._canvas.update_idletasks()
    self._turn()

  def draw_handler(self, event):
    self.draw()

#========================================================
#                        Game
#========================================================
if __name__ == '__main__':
  GUI().start()