import math

class Model:
  def __init__(self):
    self._time = 0.0
    self._states = {}

  def getStates(self):
    return dict(self._states)

  def setup(self):
    pass

  def update(self, dt, controls: dict):
    self._time += dt
