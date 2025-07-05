import math

class Model:
  def __init__(self):
    self.time = 0.0
    self.states = {}

  def getStates(self):
    return self.states

  def setup(self):
    pass

  def update(self, dt, controls):
    self.time += dt

  def draw(self, controller = None):
    pass
