import time

class Timer():
  def __init__(self,interval=0.01):
    self.count = 0.0
    self.paused = False
    self.interval = interval

  def Time(self):
    while not self.paused:
      time.sleep(self.interval)
      self.count += self.interval

  def stop(self):
    self.paused = True
    temp_count = self.count
    self.count = 0.0
    return temp_count
