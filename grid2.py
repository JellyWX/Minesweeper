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
    self.cursor = None

  def drawGrid(self,x=16,y=16):
    self.size_x = x
    self.size_y = y

    for row in range(y):
      self.array.append([])
      for item in range(x):
        self.array[row].append(Tile(self,row,item,0))

  def drawMines(self,mines=40):
    self.mines = mines

    for _ in range(0,mines):
      randRow = randint(0,self.size_y - 1)
      randCol = randint(0,self.size_x - 1)
      while self.array[randRow][randCol].getMine or not self.array[randRow][randCol].getCovered:
        randRow = randint(0,self.size_y - 1)
        randCol = randint(0,self.size_x - 1)
      self.array[randRow][randCol].mine = True

    for row in self.array:
      for item in row:
        item.getBombNeighbours()

  def setCursorPos(self,c_x,c_y):
    y = 0
    for row in self.array:
      x = 0
      for item in row:
        if x < c_x <= x + self.pix:
          if y < c_y <= y + self.pix:
            self.cursor = item
            return
        x += self.pix
      y += self.pix

  def render(self):
    y = 0
    for row in self.array:
      x = 0
      for item in row:
        self.gui.Image(self.images['background'],self.pix,self.pix,x,y)
        if item.getCovered:
          self.gui.Image(self.images['tile'],self.pix,self.pix,x,y)        else:
          if item.getMine():
            self.gui.Image(self.images['mine'],self.pix,self.pix,x,y)
          else:
            try:
              self.gui.Image(self.images[str(item)],self.pix,self.pix,x,y)
            except:
              pass

        if self.cursor == item:
          self.gui.Image(self.images['overlay'],self.pix,self.pix,x,y)

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

  def getBombNeighbours(self,quick=False):
    if quick:
      return self.data
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
    try:
      return self.id == comparitor.id
    except:
      return False

  def __hash__(self):
    return self.id

  def __str__(self):
    return str(self.data)
