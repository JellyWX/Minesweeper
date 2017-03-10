from random import randint


class Grid():
  def __init__(self,gui,size_x,size_y,mines,pixel=20):

    self.array = []
    self.gui = gui

    for i in range(0,size_y):
      self.array.append([])
      for j in range(0,size_x):
        self.array[i].append(['tile'])

    for i in range(0,mines):
      self.array[randint(0,size_y - 1)][randint(0,size_x - 1)][0] = 'mine'

  def hover(self,pos):


  def release(self,pos):

  def render(self):
