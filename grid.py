from random import randint


class Grid():
  def __init__(self,gui,im,size_x=16,size_y=16,mines=40,pixel=25):

    self.array = []
    self.gui = gui
    self.im = im
    self.pix = pixel
    self.mines = mines
    self.size_x = size_x
    self.size_y = size_y

    self.cursor_pos = (0,0)

    for i in range(0,size_y):
      self.array.append([])
      for _ in range(0,size_x):
        self.array[i].append(['tile','c',''])

  def post_initial(self):

    for i in range(0,self.mines):
      r  = randint(0,self.size_y - 1)
      r2 = randint(0,self.size_x - 1)
      while self.array[r][r2][0] == 'mine' or self.array[r][r2][1] == 'u':
        r  = randint(0,self.size_y - 1)
        r2 = randint(0,self.size_x - 1)
      self.array[r][r2][0] = 'mine'

    for row in range(0,len(self.array)):
      for col in range(0,len(self.array[row])):
        if row == 0:
          row_r = range(0,2)
        elif row == len(self.array) - 1:
          row_r = range(-1,1)
        else:
          row_r = range(-1,2)

        if col == 0:
          col_r = range(0,2)
        elif col == len(self.array[row]) - 1:
          col_r = range(-1,1)
        else:
          col_r = range(-1,2)

        local_arr = []

        for i in row_r:
          for j in col_r:
            local_arr.append(self.array[row+i][col+j][0])

        mine_count = 0

        for item in local_arr:
          if item == 'mine':
            mine_count += 1

        if mine_count > 0:
          self.array[row][col][2] = mine_count
        if self.array[row][col][0] == 'mine':
          self.array[row][col][2] = 'M'


  def release(self):
    y = 0
    for row in range(0,len(self.array)):
      x = 0
      for item in range(0,len(self.array[row])):

        if self.cursor_pos[0] == row and self.cursor_pos[1] == item:

            if self.array[row][item][1] == 'c':
              self.array[row][item][1] = 'u'
              if self.array[row][item][0] == 'mine':
                print('gameover')
                return True
              else:
                if self.array[row][item][2] == '':
                  self.open(row,item)
                return False

        x += self.pix
      y += self.pix

  def open(self,row,col):
    self.array[row][col][1] = 'u'
    for i in range(-1,2):
      for j in range(-1,2):
        if row != 0 and col != 0 and col != self.size_x - 1 and row != self.size_y - 1:
          if self.array[row+i][col+j][1] == 'c' and self.array[row+i][col+j][2] != 'M':
            self.array[row+i][col+j][1] = 'u'

  def mark(self):
    y = 0
    for row in range(0,len(self.array)):
      x = 0
      for item in range(0,len(self.array[row])):
        if self.cursor_pos[0] == row and self.cursor_pos[1] == item:
          if self.array[row][item][1] == 'c':
            self.array[row][item][1] = 'm'
          elif self.array[row][item][1] == 'm':
            self.array[row][item][1] = 'c'

        x += self.pix
      y += self.pix

  def cursor(self,pos_x,pos_y):
    y = 0
    for row in range(0,len(self.array)):
      x = 0
      for item in range(0,len(self.array[row])):
        if x < pos_x <= x + self.pix:
          if y < pos_y <= y + self.pix:
            self.cursor_pos = (row,item)
            return
        x += self.pix
      y += self.pix

  def render(self):
    y = 0
    for i in range(0,len(self.array)):
      x = 0
      for j in range(0,len(self.array[i])):
        if self.array[i][j][1] == 'c':
          self.gui.Image(self.im['tile'],self.pix,self.pix,x,y)
        elif self.array[i][j][1] == 'u':
          self.gui.Image(self.im['background'],self.pix,self.pix,x,y)
          self.gui.Text(str(self.array[i][j][2]),self.pix,True)
          self.gui.showText(x,y)
        elif self.array[i][j][1] == 'm':
          self.gui.Image(self.im['mark'],self.pix,self.pix,x,y)
        if self.cursor_pos == (i,j):
          self.gui.Image(self.im['overlay'],self.pix,self.pix,x,y)
        x += self.pix
      y += self.pix
