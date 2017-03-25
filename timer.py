import time

class Timer():
  def __init__(self,paused=False):
    self.count = 0.0
    self.paused = paused
    self.start_time = time.time()
    self.time = time.time() - self.start_time
    self.bookmarks = {}

  def Time(self):
    if not self.paused:
      self.time = time.time() - self.start_time
    return self.time

  def Reset(self,ALTPAUSE=False):
    self.start_time = time.time()
    self.time = time.time() - self.start_time
    if ALTPAUSE:
      self.paused = not self.paused

  def Bookmark(self,code):
    self.bookmarks[code] = self.Time()

  def get(self,code):
    return self.bookmarks[code]
