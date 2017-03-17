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
        self.array[row].append(Tile(self.array,row,item,0))

  def drawMines(self,mines=40):
    self.mines = mines

    for i in range(0,mines):
      randRow = randint(0,self.size_y - 1)
      randCol = randint(0,self.size_x - 1)
      while not self.array[randRow][randCol].getMine or not self.array[randRow][randCol].getCovered:
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

  def open(self):
    return self.cursor.reveal()

  def render(self):
    y = 0
    for row in self.array:
      x = 0
      for item in row:
        self.gui.Image(self.images['background'],self.pix,self.pix,x,y)
        if item.getCovered():
          self.gui.Image(self.images['tile'],self.pix,self.pix,x,y)
        else:
          if item.getMine():
            self.gui.Image(self.images['mine'],self.pix,self.pix,x,y)
          else:
            self.gui.Image(self.images[str(item)],self.pix,self.pix,x,y)
        x += self.pix
      y += self.pix

    try:
      if self.cursor.getCovered():
        self.gui.Image(self.images['overlay'],self.pix,self.pix,self.pix*self.cursor.column,self.pix*self.cursor.row)
      else:
        self.gui.Image(self.images['overlay_2'],self.pix*3,self.pix*3,self.pix*(self.cursor.column-1),self.pix*(self.cursor.row-1))
    except:
      pass

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
      #print('mine')
      self.data = -1
      return -1
    else:
      if self.row == 0:
        row_r = range(0,2)
      elif self.row == len(self.array) - 1:
        row_r = range(-1,1)
      else:
        row_r = range(-1,2)

      if self.column == 0:
        col_r = range(0,2)
      elif self.column == len(self.array[0]) - 1:
        col_r = range(-1,1)
      else:
        col_r = range(-1,2)

      local_arr = []

      for i in row_r:
        for j in col_r:
          local_arr.append(self.array[self.row+i][self.column+j])

      mine_count = 0

      for item in local_arr:
        if item.getMine():
          mine_count += 1

      self.data = mine_count
      return mine_count

  def reveal(self):
    self.covered = False
    if self.mine:
      return True
    else:
      return False

  def __eq__(self,comparitor):
    try:
      return self.id == comparitor.id
    except:
      return False

  def __hash__(self):
    return self.id

  def __str__(self):
    return str(self.data)
