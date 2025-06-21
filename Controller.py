import pygame
from Timer import Timer
from Model import *
from Viewer import *

class Controller:

    def __init__(self):
        self.run = True
        self.timer = Timer()

        self.modelControls = {
            "force": 0.0,
            "torque": 0.0
            }
        self.model = None

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
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == pygame.KEYDOWN:
                # alpha numeric keys
                if event.key == pygame.K_f:
                    self.viewer.toggleFullScreen()
                elif event.key == pygame.K_q:
                    self.run = False

                # special keys
                elif event.key == pygame.K_ESCAPE:
                    self.run = False

    def processKeys(self, dt):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_UP]:
            self.modelControls["force"] += 1.0
        if pressedKeys[pygame.K_DOWN]:
            self.modelControls["force"] -= 1.0
        if pressedKeys[pygame.K_RIGHT]:
            self.modelControls["torque"] += 1.0
        if pressedKeys[pygame.K_LEFT]:
            self.modelControls["torque"] -= 1.0

    def update(self):
        # get the delta time
        deltaTime = self.timer.mark()

        # without any input there are no applied forces/torques
        self.modelControls["force"] = 0.0
        self.modelControls["torque"] = 0.0

        self.processEvents(deltaTime)
        self.processKeys(deltaTime)

        # update the model
        if self.model != None:
            self.model.update(deltaTime, self.modelControls)

        # update the view for default drawing mode
        self.viewer.preDrawUpdate()

    def checkRunRequest(self):
        return self.run
