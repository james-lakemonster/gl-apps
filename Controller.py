import pygame
import sys
from Timer import Timer
from Model import Model
from Viewer import Viewer

class Controller:
  # The Controller class handles
  #   Frame updates / time stepping
  #   pygame.events and keypresses

  def __init__(self, model: Model, viewer: Viewer):
    self.model = model
    self.viewer = viewer
    self.deltaTime = 0.0

    self.loadControls()
    self.loadKeyCallbacks()

    self.viewer.setup()
    self.model.setup()

    self.timer = Timer()

  def getControls(self):
    return dict(self.controls)

  def run(self):
    while self.controls['run']:
      # Process the controls to update the model and the view
      self.update()

    # done - shutdown
    self.shutdown()

  # def check(self, name: str):
  #   if name in self.controls.keys():
  #     value = self.controls[name]
  #     if isinstance(value, bool):
  #       return value
  #   return False

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

    # some things may need to be reset every cycle prior to user input
    self.cyclicInit()

    # process input and system events
    self.processEvents()

    # update the model
    self.model.update(self.deltaTime, self.getControls())

    # update the view
    self.viewer.update(self.model.getStates(), self.getControls())

    # pad runtime as desired
    pygame.time.wait(10)

  def cyclicInit(self):
    pass

  def shutdown(self):
    # proper shutdown
    pygame.quit()
    sys.exit() # strong exit avoids quit confirmation dialogue in OS X

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

  #
  # Customizations
  #
  def loadControls(self):
    self.controls = {
      'run': True,
      }

  def loadKeyCallbacks(self):
    self.keyCallbacks = {
      pygame.K_f: {
        'key_help_name': 'F',
        'type': 'tap',
        'description': 'Toggle fullscreen mode',
        'callback': self.toggleFullScreen
        },
      pygame.K_h: {
        'key_help_name': 'H',
        'type': 'tap',
        'description': 'Help',
        'callback': self.showHelp
        },
      pygame.K_ESCAPE: {
        'key_help_name': 'ESC',
        'type': 'tap',
        'description': 'Quit',
        'callback': lambda: self.setControl('run', False)
        },
      }
