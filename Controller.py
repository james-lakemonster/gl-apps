import pygame
from Timer import Timer
from Model import *
from Viewer import *

class Controller:

    def __init__(self):
        self.run = True
        self.fullscreen = False
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

    def update(self):
        dt = self.timer.mark()

        #
        # handle all discrete events
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == pygame.KEYDOWN:
                # alpha numeric keys
                if event.key == pygame.K_q:
                    self.run = False

                elif event.key == pygame.K_f:
                    # toggle full screen
                    self.fullscreen = not self.fullscreen

                # special keys
                elif event.key == pygame.K_ESCAPE:
                    self.run = False

        #
        # handle continuous press hold key actions
        #
        self.modelControls["force"] = 0.0
        self.modelControls["torque"] = 0.0

        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_UP]:
            self.modelControls["force"] += 1.0
        if pressedKeys[pygame.K_DOWN]:
            self.modelControls["force"] -= 1.0
        if pressedKeys[pygame.K_RIGHT]:
            self.modelControls["torque"] += 1.0
        if pressedKeys[pygame.K_LEFT]:
            self.modelControls["torque"] -= 1.0

        # update the model
        if self.model != None:
            self.model.update(dt, self.modelControls)


    def checkRunRequest(self):
        return self.run

    def checkFullScreenRequest(self):
        return self.fullscreen
