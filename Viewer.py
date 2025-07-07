import pygame
from pygame.locals import *
from SimpleGL import *

class Viewer:
  # The Viewer class abstracts all pygame.display functions
  def __init__(self, name : str = ""):
    self._name = name
    if self._name == "":
      self._name = "A SimpleGL App"
    self._windowSize = None
    self._minClipDist = 0.1
    self._maxClipDist = 50.0

  def setup(self):
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL|RESIZABLE)
    pygame.display.set_caption(self._name)
    sglInit()
    print("\n\t" + self._name + "...  press 'H' for help.")

  def toggleFullScreen(self):
    pygame.display.toggle_fullscreen()

  def preDrawUpdate(self):
    # Check for:
    #     window resize
    #     perspective change
    #     clipping depth changes

    # if the window has changed size then:
    # compute the new perspective and
    # restore some basic intializations
    newWindowSize = pygame.display.get_window_size()
    if newWindowSize != self._windowSize:
      self._windowSize = newWindowSize
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(45, (newWindowSize[0]/newWindowSize[1]), self._minClipDist, self._maxClipDist)
      sglReInit()

  def draw(self, modelStates: dict, controlStates: dict):
    pass

  def update(self, modelStates: dict, controlStates: dict):
    # update the view for default drawing mode
    self.preDrawUpdate()

    # render the new scene
    self.draw(modelStates, controlStates)

    # publish the new view
    pygame.display.flip()
