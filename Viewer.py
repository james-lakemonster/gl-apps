import pygame
from pygame.locals import *
from SimpleGL import *

class Viewer:
  # The Viewer class abstracts all pygame.display functions
  def __init__(self, name : str = ""):
    self.name = name
    if self.name == "":
      self.name = "A SimpleGL App"
    self.windowSize = None
    self.minClipDist = 0.1
    self.maxClipDist = 50.0

  def setup(self):
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL|RESIZABLE)
    pygame.display.set_caption(self.name)
    sglInit()

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
    if newWindowSize != self.windowSize:
      self.windowSize = newWindowSize
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(45, (newWindowSize[0]/newWindowSize[1]), self.minClipDist, self.maxClipDist)
      sglReInit()

  def draw(self, modelStates, controlStates):
    pass

  def update(self, model, controller):
    # update the view for default drawing mode
    self.preDrawUpdate()

    # render the new scene
    self.draw(model, controller)

    # publish the new view
    pygame.display.flip()
