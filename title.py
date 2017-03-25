class Title():
  def __init__(self,gui,im,extras=0):
    ## rendering components ##
    self.gui = gui
    self.im = im

    ## metadata ##
    self.cursor_x = 0
    self.cursor_y = 0
    self.post_init(extras)

  def post_init(self,extras):
    pass

  def setCursorPos(self,x,y):
    self.cursor_x = x
    self.cursor_y = y

  def key_hit(self,key_hit):
    pass

  def click(self):
    pass

  def render(self):
    pass
