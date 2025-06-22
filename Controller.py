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
    self.deltaTime = 0.0

    self.loadControls()
    self.loadKeyCallbacks()

    self.timer = Timer()

  def loadControls(self):
    self.controls = {
      'run': True,
      'show_hidden': False,
      'force': 0.0,
      'torque': 0.0
      }

  def loadKeyCallbacks(self):
    self.keyCallbacks = {
      pygame.K_f: {
        'key_help_name': 'F',
        'type': 'tap',
        'description': 'Toggle fullscreen mode',
        'callback': lambda: self.toggleFullScreen()
        },
      pygame.K_h: {
        'key_help_name': 'H',
        'type': 'tap',
        'description': 'Help',
        'callback': lambda: self.showHelp()
        },
      pygame.K_p: {
        'key_help_name': 'P',
        'type': 'tap',
        'description': 'Show/Hide additional geometries',
        'callback': lambda: self.toggleControl('show_hidden')
        },
      pygame.K_q: {
        'key_help_name': 'Q',
        'type': 'tap',
        'description': 'Quit',
        'callback': lambda: self.setControl('run', False)
        },
      pygame.K_ESCAPE: {
        'key_help_name': 'ESC',
        'type': 'tap',
        'description': 'Quit',
        'callback': lambda: self.setControl('run', False)
        },
      pygame.K_UP: {
        'key_help_name': 'ARROW_UP/DOWN',
        'type': 'held',
        'description': 'Increase/Decrease linear motion speed',
        'callback': lambda: self.setControl('force', self.controls['force'] + 1.0)
        },
      pygame.K_DOWN: {
        'key_help_name': None, # this key is documented with the UP ARROW
        'type': 'held',
        'description': '',
        'callback': lambda: self.setControl('force', self.controls['force'] - 1.0)
        },
      pygame.K_RIGHT: {
        'key_help_name': 'ARROW_RIGHT/LEFT',
        'type': 'held',
        'description': 'Increase/Decrease angular rotation speed',
        'callback': lambda: self.setControl('torque', self.controls['torque'] + 1.0)
        },
      pygame.K_LEFT: {
        'key_help_name': None,
        'type': 'held',
        'description': '',  # this key is documented with the RIGHT ARROW
        'callback': lambda: self.setControl('torque', self.controls['torque'] - 1.0)
        },
      }

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
    if name in self.controls.keys():
      value = self.controls[name]
      if isinstance(value, bool):
        return value
    return False

  def processEvents(self):

    # Loop through published pyGame Events
    for event in pygame.event.get():
      # special events
      if event.type == pygame.QUIT:
        self.controls['run'] = False

      # key tap events
      elif event.type == pygame.KEYDOWN:
        if event.key in self.keyCallbacks.keys():
          keyCallback = self.keyCallbacks[event.key]
          if keyCallback['type'] == 'tap':
            keyCallback['callback']()

    # Check the held keys
    pressedKeys = pygame.key.get_pressed() # get the state of the keyboard
    for key_name in self.keyCallbacks:
      keyCallback = self.keyCallbacks[key_name]
      if keyCallback['type'] == 'held':
        if pressedKeys[key_name]:
          keyCallback['callback']()

  def update(self):
    # get the delta time
    self.deltaTime = self.timer.mark()

    # without any input there are no applied forces/torques
    self.controls["force"] = 0.0
    self.controls["torque"] = 0.0

    # process input and system events
    self.processEvents()

    # update the model
    if self.model is not None:
      self.model.update(self.deltaTime, self.controls)

    # update the view for default drawing mode
    if self.viewer is not None:
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

  def showHelp(self):
    print('\n\nThe following commands are availble:')
    for key in self.keyCallbacks:
      callback = self.keyCallbacks[key]
      if callback['key_help_name'] is not None:
        print('\t' + callback['key_help_name'] + ' : ' + callback['description'])

  def toggleFullScreen(self):
    if self.viewer is not None:
      self.viewer.toggleFullScreen()

  #
  # Useful Functions for defining callbacks
  #
  def toggleControl(self, name: str):
    self.controls[name] = not self.controls[name]

  def setControl(self, name: str, value):
    self.controls[name] = value
