import pygame
from Timer import Timer
from Model import *
from Viewer import *

class Controller:
  # The Controller class handles
  #   Frame updates / time stepping
  #   pygame.events and keypresses

  def __init__(self):
    self.model = None
    self.viewer = None

    self.controls = {
      'run': True,
      'show_hidden': False,
      'force': 0.0,
      'torque': 0.0
      }

    self.tappedKeyCallbacks = {
      pygame.K_f: lambda: self.viewer.toggleFullScreen(),
      pygame.K_h: lambda: self.toggleControl('show_hidden'),
      pygame.K_q: lambda: self.setControl('run', False),
      pygame.K_ESCAPE: lambda: self.setControl('run', False)
      }

    self.pressedKeyCallbacks = {
      pygame.K_UP: lambda: self.setControl('force', self.controls['force'] + 1.0),
      pygame.K_DOWN: lambda: self.setControl('force', self.controls['force'] - 1.0),
      pygame.K_RIGHT: lambda: self.setControl('torque', self.controls['torque'] + 1.0),
      pygame.K_LEFT: lambda: self.setControl('torque', self.controls['torque'] - 1.0)
      }

    self.timer = Timer()

  def setModel(self, model):
    self.model = model

  def setViewer(self, viewer):
    self.viewer = viewer

  def setup(self):
    if self.viewer != None:
      self.viewer.setup();
    if self.model != None:
      self.model.setup();

    self.timer.reset()

  def check(self, name: str):
    try:
      value = self.controls[name]
    except KeyError:
      value = False

    if not isinstance(value, bool):
      value = False
    return value

  def processEvents(self, dt):
    for event in pygame.event.get():
      # special events
      if event.type == pygame.QUIT:
        self.controls['run'] = False

      # key stroke events
      elif event.type == pygame.KEYDOWN:
        if event.key in self.tappedKeyCallbacks.keys():
          self.tappedKeyCallbacks[event.key]()

  def processKeys(self, dt):
    # Get the pressed state of all keys
    pressedKeys = pygame.key.get_pressed()

    # Check the list of available assigned callbacks against the pressed keys
    for key_name in self.pressedKeyCallbacks:
      if pressedKeys[key_name]:
        self.pressedKeyCallbacks[key_name]()

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

  #
  # Useful Functions for defining callbacks
  #
  def toggleControl(self, name: str):
    self.controls[name] = not self.controls[name]

  def setControl(self, name: str, value):
    self.controls[name] = value
