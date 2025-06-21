import pygame

class Controller:

    def __init__(self):
        self.run = True
        self.fullscreen = False

        self.outputs = {
            "force": 0.0,
            "torque": 0.0
            }

    def update(self):

        # handle all discrete events
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

        self.outputs["force"] = 0.0
        self.outputs["torque"] = 0.0

        # handle pressed (and held) keys
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_UP]:
            self.outputs["force"] += 1.0
        if pressedKeys[pygame.K_DOWN]:
            self.outputs["force"] -= 1.0
        if pressedKeys[pygame.K_RIGHT]:
            self.outputs["torque"] += 1.0
        if pressedKeys[pygame.K_LEFT]:
            self.outputs["torque"] -= 1.0


    def getOutputs(self):
        return self.outputs

    def checkRunRequest(self):
        return self.run

    def checkFullScreenRequest(self):
        return self.fullscreen
