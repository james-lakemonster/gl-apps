import time
import pygame

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
    dt = t - self.markerTime
    self.markerTime = t
    return dt

class TimeManager:

  def __init__(self):
    pass
  
  def start(self):
    pass

  def getModelStep(self):
    return 0.02

  def syncViewTask(self):
    pass

  def postViewTask(self):
    pass

class FixedDelayTimeManager(TimeManager):

  def __init__(self):
    self._delayMs = 10
    self._timer = Timer()
  
  def setDelayMilliseconds(self, delay):
    self._delayMs = delay

  def start(self):
    self._timer.reset()

  def getModelStep(self):
    return self._timer.mark()

  def syncViewTask(self):
    pass

  def postViewTask(self):
    pygame.time.wait(10)

class FixedStepTimeManager(TimeManager):

  def __init__(self):
    self._timer = Timer()
  
  def start(self):
    self._timer.reset()

  def getModelStep(self):
    return 0.0

  def syncViewTask(self):
    pass

  def postViewTask(self):
    pass

    # extraTimeMS = (self.simTime - self.timer.getElapsedTime()) * 1000
    # if extraTimeMS > 10:
    #   pygame.time.wait(round(extraTimeMS - 0.5))
    # if extraTimeMS < -50:
    #   if self.realtime == True:
    #     print("*** Real time violation encountered at " + str(self.simTime) + " seconds")
    #     self.realtime = False
    # elif self.realtime == False:
    #     print("*** Real time has been restored at " + str(self.simTime) + " seconds")
    #     self.realtime = True

