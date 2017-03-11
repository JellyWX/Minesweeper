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
        self.array[i].append(['tile','c',0])

    for i in range(0,mines):
      r  = randint(0,size_y - 1)
      r2 = randint(0,size_x - 1)
      while self.array[r][r2][0] == 'mine':
        r  = randint(0,size_y - 1)
        r2 = randint(0,size_x - 1)
      self.array[r][r2][0] = 'mine'


  def release(self):
    y = 0
    for row in self.array:
      x = 0
      for item in row:
        if x < self.cursor_x <= x + 25:
          if y < self.cursor_y <= y + 25:
            if item[1] == 'c':
              item[1] = 'u'
              if item[0] == 'mine':
                return True
              else:
                self.release_proc(row,item)

        x += self.pix
      y += self.pix

  def release_proc(self,x,y):
    pass

  def render(self):
    y = 0
    for i in self.array:
      x = 0
      for j in i:
        if j[1] == 'c':
          self.gui.Image(self.im['tile'],self.pix,self.pix,x,y)
        elif j[1] == 'u':
          self.gui.Image(self.im['background'],self.pix,self.pix,x,y)
        if x < self.cursor_x <= x + 25:
          if y < self.cursor_y <= y + 25:
            self.gui.Image(self.im['overlay'],self.pix,self.pix,x,y)
        x += self.pix
      y += self.pix
