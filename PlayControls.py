import time
import pygame

class PlayControls:

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

class FixedDelayPC(PlayControls):

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

class FixedStepPC(PlayControls):

  def __init__(self):
    self._timer = Timer()
    self._stepSize = 0.02;
    self._simTime = -self._stepSize
    self._realtime = True
  
  def start(self):
    self._timer.reset()

  def getModelStep(self):
    self._simTime += self._stepSize
    return self._stepSize

  def syncViewTask(self):
    extraTimeMS = (self._simTime - self._timer.getElapsedTime()) * 1000
    if extraTimeMS > 10:
      pygame.time.wait(round(extraTimeMS - 0.5))
    if extraTimeMS < -50:
      if self._realtime == True:
        print("*** Real time violation encountered at " + str(self._simTime) + " seconds")
        self._realtime = False
    elif self._realtime == False:
        print("*** Real time has been restored at " + str(self._simTime) + " seconds")
        self._realtime = True

  def postViewTask(self):
    pass
