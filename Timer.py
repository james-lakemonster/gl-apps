import time
class Timer:

  def __init__(self):
    self.initialTime = time.time()
    self.markerTime = self.initialTime

  def reset(self):
    self.initialTime = time.time()
    self.markerTime = self.initialTime

  def getElapsedTime(self):
    return time.time() - self.initialTime

  def mark(self):
    t = time.time()
    dt = t - self.markerTime;
    self.markerTime = t
    return dt
