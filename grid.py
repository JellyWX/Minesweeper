from random import randint


class Grid():
  def __init__(self,gui,im,size_x,size_y,mines,pixel=25):

    self.array = []
    self.gui = gui
    self.im = im
    self.pix = pixel

    self.cursor_x = 0
    self.cursor_y = 0

    for i in range(0,size_y):
      self.array.append([])
      for j in range(0,size_x):
        self.array[i].append(['tile','c',''])

    for i in range(0,mines):
      r  = randint(0,size_y - 1)
      r2 = randint(0,size_x - 1)
      while self.array[r][r2][0] == 'mine':
        r  = randint(0,size_y - 1)
        r2 = randint(0,size_x - 1)
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
    #print('starting release')
    y = 0
    for row in range(0,len(self.array)):
      x = 0
      for item in range(0,len(self.array[row])):
        if x < self.cursor_x <= x + 25:
          if y < self.cursor_y <= y + 25:
            if self.array[row][item][1] == 'c':
              #print('found covered tile. starting uncover.')
              self.array[row][item][1] = 'u'
              if self.array[row][item][0] == 'mine':
                print('gameover')
                return True
              else:
                return False

        x += self.pix
      y += self.pix

  def mark(self):
    y = 0
    for row in range(0,len(self.array)):
      x = 0
      for item in range(0,len(self.array[row])):
        if x < self.cursor_x <= x + 25:
          if y < self.cursor_y <= y + 25:
            if self.array[row][item][1] == 'c':
              self.array[row][item][1] = 'm'
            elif self.array[row][item][1] == 'm':
              self.array[row][item][1] = 'c'

        x += self.pix
      y += self.pix

  #def auto_release(self,row,col):
  #  try

  def render(self):
    y = 0
    for i in self.array:
      x = 0
      for j in i:
        if j[1] == 'c':
          self.gui.Image(self.im['tile'],self.pix,self.pix,x,y)
        #if j[0] == 'mine':
        #  self.gui.Text(str('M'),self.pix,True)
        #  self.gui.showText(x,y)
        elif j[1] == 'u':
          self.gui.Image(self.im['background'],self.pix,self.pix,x,y)
          self.gui.Text(str(j[2]),self.pix,True)
          self.gui.showText(x,y)
        elif j[1] == 'm':
          self.gui.Image(self.im['mark'],self.pix,self.pix,x,y)
        if x < self.cursor_x <= x + 25:
          if y < self.cursor_y <= y + 25:
            self.gui.Image(self.im['overlay'],self.pix,self.pix,x,y)
        x += self.pix
      y += self.pix
