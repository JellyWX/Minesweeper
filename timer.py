import time

class Timer():
  def __init__(self,interval=0.01):
    self.count = 0.0
    self.paused = False
    self.interval = 0.01

  def Time(self):
    while not paused:
      time.sleep(interval)
      self.count += interval

  def stop(self):
    self.paused = True
    temp_count = self.count
    self.count = 0.0
    return temp_count
