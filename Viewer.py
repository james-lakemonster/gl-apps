import pygame
from pygame.locals import *
from SimpleGL import *

class Viewer:
  # The Viewer class abstracts all pygame.display functions
  def __init__(self):
    self.windowSize = None
    self.minClipDist = 0.1
    self.maxClipDist = 50.0

  def setup(self):
    pygame.init()
    pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL|RESIZABLE)
    pygame.display.set_caption("SimpleGL Demo App")
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

  def publishView(self):
    pygame.display.flip()
