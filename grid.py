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
    self.last_click = 0
    self.x_shift = 0
    self.y_shift = 0

  def drawGrid(self,x=16,y=16):
    self.size_x = x
    self.size_y = y

    for row in range(y):
      self.array.append([])
      for item in range(x):
        self.array[row].append(Tile(self,self.array,row,item,0))

  def key_hit(self,k):
    print('Key actions have no effect in grid mode')

  def drawMines(self,mines=40):
    self.mines = mines

    for i in range(0,mines):
      randRow = randint(0,self.size_y - 1)
      randCol = randint(0,self.size_x - 1)
      local_arr = []
      checks = False

      if self.mines < ((self.size_x * self.size_y) - 9):
        checks = True
        for i in range(-1,2):
          for j in range(-1,2):
            try:
              local_arr.append(self.array[randRow+i][randCol+j].getCovered())
            except IndexError:
              pass
      else:
        local_arr = [self.array[randRow][randCol].getCovered()]

      while False in local_arr or self.array[randRow][randCol].getMine():
        randRow = randint(0,self.size_y - 1)
        randCol = randint(0,self.size_x - 1)
        local_arr = []
        if checks:
          for i in range(-1,2):
            for j in range(-1,2):
              try:
                local_arr.append(self.array[randRow+i][randCol+j].getCovered())
              except IndexError:
                pass
        else:
          local_arr = [self.array[randRow][randCol].getCovered()]
      self.array[randRow][randCol].mine = True

    for row in self.array:
      for item in row:
        item.getBombNeighbours()

  def getCursorVariation(self,c_x,c_y):
      if self.cursor == self.last_click:
        return False
      else:
        return True

  def setClickPos(self,c_x,c_y):
    y = self.y_shift
    for row in self.array:
      x = self.x_shift
      for item in row:
        if x < c_x <= x + self.pix:
          if y < c_y <= y + self.pix:
            self.last_click = item
        x += self.pix
      y += self.pix

  def setCursorPos(self,c_x,c_y):
    y = self.y_shift
    for row in self.array:
      x = self.x_shift
      for item in row:
        if x < c_x <= x + self.pix:
          if y < c_y <= y + self.pix:
            self.cursor = item
            return
        x += self.pix
      y += self.pix

  def open(self,cell,auto=False):
    if cell.getCovered() and not cell.getMarked():
      return cell.reveal()
    elif not cell.getCovered() and cell.data > 0 and auto:
      if cell.row == 0:
        row_r = range(0,2)
      elif cell.row == len(self.array) - 1:
        row_r = range(-1,1)
      else:
        row_r = range(-1,2)

      if cell.column == 0:
        col_r = range(0,2)
      elif cell.column == len(self.array[0]) - 1:
        col_r = range(-1,1)
      else:
        col_r = range(-1,2)

      local_arr = []
      mark_li = 0

      for i in row_r:
        for j in col_r:
          if self.array[cell.row+i][cell.column+j].getMarked():
            mark_li += 1

      if mark_li >= self.array[cell.row][cell.column].data:
        for i in row_r:
          for j in col_r:
            local_arr.append(self.open(self.array[cell.row+i][cell.column+j]))

        if True in local_arr:
          return True
        else:
          return False
      else:
        return False
    else:
      return False

  def mark(self,cell,m):
    cell.marked = m

  def marked(self,cell):
    return cell.getMarked()

  def scale(self,zoomin=True):
    if zoomin:
      self.pix += 2
    elif not self.pix < 4:
      self.pix -= 2

  def shift(self,x_shift,y_shift):
    self.x_shift -= x_shift
    self.y_shift -= y_shift

  def Clock(self):
    marked = 0
    covered = 0
    for row in self.array:
      for item in row:
        if item.getMarked() and item.getMine():
          marked += 1
        if item.getCovered():
          covered += 1
    if marked == self.mines and covered == self.mines:
      return True
    else:
      return False

  def render(self,overlay=True,showMines=False):
    self.gui.page.fill((0,0,0))
    y = self.y_shift
    for row in self.array:
      x = self.x_shift
      for item in row:
        self.gui.Image(self.images['background'],self.pix,self.pix,x,y)
        if item.getCovered():
          self.gui.Image(self.images['tile'],self.pix,self.pix,x,y)
          if item.getMarked():
            self.gui.Image(self.images['mark'],self.pix,self.pix,x,y)
        else:
          if item.getMine():
            self.gui.Image(self.images['mine'],self.pix,self.pix,x,y)
          else:
            self.gui.Image(self.images[str(item)],self.pix,self.pix,x,y)
        if showMines:
          if item.getMine():
            self.gui.Image(self.images['mine'],self.pix,self.pix,x,y)
        x += self.pix
      y += self.pix

    if overlay:
      try:
        if self.cursor.getCovered():
          self.gui.Image(self.images['overlay'],self.pix,self.pix,(self.pix*self.cursor.column)+self.x_shift,(self.pix*self.cursor.row)+self.y_shift)
        else:
          self.gui.Image(self.images['overlay_2'],self.pix*3,self.pix*3,(self.pix*(self.cursor.column-1))+self.x_shift,(self.pix*(self.cursor.row-1))+self.y_shift)
      except:
        pass

class Tile():
  def __init__(self,grid,array,pos_x,pos_y,data):
    ## id for comparisons ##
    self.id = uuid.uuid4()

    ## metadata ##
    self.row = pos_x
    self.column = pos_y
    self.grid = grid
    self.array = array

    ## data ##
    self.data = data
    self.covered = True
    self.mine = False
    self.marked = False

  def getCovered(self):
    return self.covered

  def getMine(self):
    return self.mine

  def getMarked(self):
    return self.marked

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

  def mark(self):
    self.marked = not self.marked

  def reveal(self):
    self.covered = False
    if self.mine:
      return True
    else:
      if self.data == 0:
        if self.grid.mines > 0:
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

          for row in row_r:
            for col in col_r:
              self.grid.open(self.array[self.row+row][self.column+col])
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
