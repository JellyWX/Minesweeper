import uuid
from random import randint

class Grid():
  def __init__(self,gui,im,pix=25):
    ## rendering components ##
    self.images = im
    self.gui = gui
    self.pix = pix

    ## metadata ##
    self.mines  = 0
    self.size_x = 0
    self.size_y = 0

    ## data ##
    self.array    = []
    self.cursor_x = 0
    self.cursor_y = 0

  def drawGrid(self,x,y):
    self.size_x = x
    self.size_y = y

    for row in range(size_y):
      self.array.append([])
      for item in range(size_x):
        self.array[row].append(Tile(self,row,item,0))

  def drawMines(self,mines):
    self.mines = mines

    for _ in range(0,mines):
      randRow = randint(0,self.size_y - 1)
      randCol = randint(0,self.size_x - 1)
      while self.array[randRow][randCol].getMine or not self.array[randRow][randCol].getCovered:
        randRow = randint(0,self.size_y - 1)
        randCol = randint(0,self.size_x - 1)
      self.array[randRow][randCol].mine = True

  def getCursorPos(self,c_x,c_y):
    y = 0
    for row in self.array:
      x = 0
      for item in row:
        if x < c_x <= x + self.pix:
          if y < c_y <= y + self.pix:
            self.cursor_x = item
            self.cursor_y = row
            return
        x += self.pix
      y += self.pix

class Tile():
  def __init__(self,array,pos_x,pos_y,data):
    ## id for comparisons ##
    self.id = uuid.uuid4()

    ## metadata ##
    self.row = pos_x
    self.column = pos_y
    self.array = array

    ## data ##
    self.data = data
    self.covered = True
    self.mine = False

  def getCovered(self):
    return self.covered

  def getMine(self):
    return self.mine

  def getBombNeighbours(self):
    if self.mine:
      return -1
    else:
      bombs = 0
      for y_diff in range(-1,2):
        for x_diff in range(-1,2):
          if self.pos_x + x_diff == -1 or self.pos_y + y_diff == -1:
            continue
          else:
            if self.array[self.pos_x + x_diff][self.pos_y + y_diff].getMine: bombs += 1
      self.data = bombs
      return bombs

  def __eq__(self,comparitor):
    return self.id == comparitor.id

  def __hash__(self):
    return self.id

  def __str__(self):
    if isinstance(self.data,self):
      return str(self.id)
    else:
      return str(self.data)
