import pygame
from Timer import Timer
from Model import *
from Viewer import *

class Controller:
  # The Controller class handles
  #   Frame updates / time stepping
  #   pygame.events and keypresses

  def __init__(self):
    self.controls = {
      'run': True,
      'show_triads': False,
      'force': 0.0,
      'torque': 0.0
      }

    self.timer = Timer()

    self.model = None
    self.viewer = None

  def check(self, name: str):
    try:
      value = self.controls[name]
    except KeyError:
      value = False

    if not isinstance(value, bool):
      value = False
    return value

  def setModel(self, model):
    self.model = model

  def setViewer(self, viewer):
    self.viewer = viewer

  def setup(self):
    if self.viewer != None:
      self.viewer.setup();
    if self.model != None:
      self.model.setup();

    self.timer.reset();

  def processEvents(self, dt):
    for event in pygame.event.get():
      # special events
      if event.type == pygame.QUIT:
        self.controls['run'] = False

      # key strokes
      elif event.type == pygame.KEYDOWN:
        # alpha numeric keys
        if event.key == pygame.K_f:
          self.viewer.toggleFullScreen()
        elif event.key == pygame.K_t:
          # toggle triad visibility
          self.controls['show_triads'] = not self.controls['show_triads']
        elif event.key == pygame.K_q:
          self.controls['run'] = False

        # special keys
        elif event.key == pygame.K_ESCAPE:
          self.controls['run'] = False

  def processKeys(self, dt):
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_UP]:
      self.controls["force"] += 1.0
    if pressedKeys[pygame.K_DOWN]:
      self.controls["force"] -= 1.0
    if pressedKeys[pygame.K_RIGHT]:
      self.controls["torque"] += 1.0
    if pressedKeys[pygame.K_LEFT]:
      self.controls["torque"] -= 1.0

  def update(self):
    # get the delta time
    deltaTime = self.timer.mark()

    # without any input there are no applied forces/torques
    self.controls["force"] = 0.0
    self.controls["torque"] = 0.0

    # process input and system events
    self.processEvents(deltaTime)
    self.processKeys(deltaTime)

    # update the model
    if self.model != None:
      self.model.update(deltaTime, self.controls)

    # update the view for default drawing mode
    if self.viewer != None:
      self.viewer.preDrawUpdate()

  def finalizeFrame(self):
    # publish the new view
    self.viewer.publishView()

    # pad runtime as desired
    pygame.time.wait(10)

  def shutdown(self):
    # proper shutdown
    pygame.quit()
    # strong exit avoids quit confirmation dialogue in OS X
    sys.exit()
