from title import Title
import pygame

class StartScreen(Title):
  def post_init(self):
    self.active_box = None
    self.vars = {'width':'16','height':'16','mines':'40'}

  def key_hit(self,k):
    if self.active_box != None:
      if k[pygame.K_0]:
        self.vars[self.active_box] += '0'
      elif k[pygame.K_1]:
        self.vars[self.active_box] += '1'
      elif k[pygame.K_2]:
        self.vars[self.active_box] += '2'
      elif k[pygame.K_3]:
        self.vars[self.active_box] += '3'
      elif k[pygame.K_4]:
        self.vars[self.active_box] += '4'
      elif k[pygame.K_5]:
        self.vars[self.active_box] += '5'
      elif k[pygame.K_6]:
        self.vars[self.active_box] += '6'
      elif k[pygame.K_7]:
        self.vars[self.active_box] += '7'
      elif k[pygame.K_8]:
        self.vars[self.active_box] += '8'
      elif k[pygame.K_9]:
        self.vars[self.active_box] += '9'
      elif k[pygame.K_BACKSPACE]:
        self.vars[self.active_box] = self.vars[self.active_box][:-1]

  def click(self):
    if 60 < self.cursor_x < 190:
      if 100 < self.cursor_y < 120:
        self.active_box = 'width'
      elif 125 < self.cursor_y < 145:
        self.active_box = 'height'
      elif 150 < self.cursor_y < 170:
        self.active_box = 'mines'
      elif 50 < self.cursor_y < 78:
        self.gui.page.fill((0,0,0))
        return True
    if 80 < self.cursor_x < 170:
      if 180 < self.cursor_y < 200:
        exit()
    return False

  def render(self):
    self.gui.Color('FFFFFF')
    self.gui.Text('Minesweeper',48,True)
    self.gui.showText(0,0)
    self.gui.Image(self.im['tile'],130,28,60,50)

    self.gui.Rect(60,100,130,20)

    self.gui.Rect(60,125,130,20)

    self.gui.Rect(60,150,130,20)

    self.gui.Rect(80,180,90,20)

    self.gui.Color('000000')
    self.gui.Text('New Game',22,True)
    self.gui.showText(74,52)

    self.gui.Text('Width :',16,True)
    self.gui.showText(60,100)

    self.gui.Text(self.vars['width'],16,True)
    self.gui.showText(130,100)

    self.gui.Text('Height:',16,True)
    self.gui.showText(60,125)

    self.gui.Text(self.vars['height'],16,True)
    self.gui.showText(130,125)

    self.gui.Text('Mines :',16,True)
    self.gui.showText(60,150)

    self.gui.Text(self.vars['mines'],16,True)
    self.gui.showText(130,150)

    self.gui.Text('Exit',16,True)
    self.gui.showText(80,180)

    if len(self.vars['width']) > 2:
      self.vars['width'] = self.vars['width'][:2]
    if len(self.vars['height']) > 2:
      self.vars['height'] = self.vars['height'][:2]
    if len(self.vars['mines']) > 3:
      self.vars['mines'] = self.vars['mines'][:3]
    try:
      if int(self.vars['mines']) > ((int(self.vars['width']) * int(self.vars['height'])) - 9):
        self.vars['mines'] = str(int(self.vars['width'])*int(self.vars['height']) - 9)
    except ValueError:
      pass

    try:
      if int(self.vars['height']) < 4:
        self.vars['height'] = '4'
    except ValueError:
      pass

    try:
      if int(self.vars['width']) < 4:
        self.vars['width'] = '4'
    except ValueError:
      pass

    try:
      if int(self.vars['mines']) < 1:
        self.vars['mines'] = '1'
    except ValueError:
      pass

class WinScreen(Title):
  def click(self):
    if 60 < self.cursor_y < 80:
      if 0 < self.cursor_x < 100:
        return True
      elif 105 < self.cursor_x < 145:
        exit()
  def render(self):
    self.gui.Color('FFFFFF')
    self.gui.Rect(60,0,100,20)

    self.gui.Rect(0,60,100,20)
    self.gui.Rect(105,60,40,20)

    self.gui.Color('000000')
    self.gui.Text('Well Done!',16,True)
    self.gui.showText(60,0)

    self.gui.Text('Play Again',16,True)
    self.gui.showText(0,60)

    self.gui.Text('Exit',16,True)
    self.gui.showText(105,60)

class LossScreen(Title):
  def click(self):
    if 60 < self.cursor_y < 80:
      if 0 < self.cursor_x < 100:
        return True
      elif 105 < self.cursor_x < 145:
        exit()
  def render(self):
    self.gui.Color('FFFFFF')
    self.gui.Rect(60,0,100,20)

    self.gui.Rect(0,60,100,20)
    self.gui.Rect(105,60,40,20)

    self.gui.Color('000000')
    self.gui.Text('   RIP   ',16,True)
    self.gui.showText(60,0)

    self.gui.Text('Play Again',16,True)
    self.gui.showText(0,60)

    self.gui.Text('Exit',16,True)
    self.gui.showText(105,60)
